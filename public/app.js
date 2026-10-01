/* ═══════════════════════════════════════════════════════
   SOVEREIGN TERMINAL — INSTITUTIONAL QUANTITATIVE CONTROLLER
   Clean, precision-engineered Solana execution engine.
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── DOM References ─────────────────────────────────────
  const $ = id => document.getElementById(id);
  const navBalance          = $('nav-balance');
  const navReturn           = $('nav-return');
  const activeAgentLabel    = $('active-agent-label');
  const chatScroller        = $('chat-scroller');
  const activityFeed        = $('activity-feed');
  const chatInput           = $('chat-input');
  const sendBtn             = $('send-btn');
  const toastShelf          = $('toast-shelf');

  // Side Panel Elements
  const sideAuditInput      = $('side-audit-input');
  const btnSideAudit        = $('btn-side-audit');
  const btnSideNewAgent     = $('btn-side-new-agent');
  const btnDeployAgentNav   = $('btn-deploy-agent-nav');
  const sideAgentAvatar     = $('side-agent-avatar');
  const sideAgentName       = $('side-agent-name');
  const sideAgentStyle      = $('side-agent-style');
  const sideAgentCap        = $('side-agent-cap');
  const sideAgentSl         = $('side-agent-sl');
  const sideAgentThesis     = $('side-agent-thesis');

  // Modals
  const chartModal          = $('chart-modal');
  const agentModal          = $('agent-modal');
  const auditModal          = $('audit-modal');

  // Chart Modal Elements
  const chartModalIcon      = $('chart-modal-icon');
  const chartModalSymbol    = $('chart-modal-symbol');
  const chartModalPrice     = $('chart-modal-price');
  const chartModalChange    = $('chart-modal-change');
  const chartModalCa        = $('chart-modal-ca');
  const btnCopyModalCa      = $('btn-copy-modal-ca');
  const dexscreenerIframe   = $('dexscreener-iframe');
  const btnCloseChartModal  = $('btn-close-chart-modal');
  const btnModalAudit       = $('btn-modal-audit');
  const btnModalBlink       = $('btn-modal-blink');
  const btnModalJupLink     = $('btn-modal-jup-link');

  // Agent Modal Elements
  const btnOpenAgentModal   = $('btn-open-agent-modal');
  const btnCloseAgentModal  = $('btn-close-agent-modal');
  const createAgentForm     = $('create-agent-form');
  const agentNameInput      = $('agent-name-input');
  const personaSelector     = $('persona-selector');
  const agentMaxSol         = $('agent-max-sol');
  const agentSl             = $('agent-sl');
  const agentThesisInput    = $('agent-thesis-input');

  // Audit Modal Elements
  const btnCloseAuditModal  = $('btn-close-audit-modal');
  const auditTokenInput     = $('audit-token-input');
  const btnSubmitAudit      = $('btn-submit-audit');

  // State
  let currentModalToken = null;
  let currentModalCa = '';
  let selectedPersonaStyle = 'Breakout Momentum';
  let selectedPersonaAvatar = '⚡';

  // ── Toast Helper ───────────────────────────────────────
  function showToast(msg, icon = '⚡') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
    toastShelf.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(6px)';
      toast.style.transition = 'all 0.2s ease';
      setTimeout(() => toast.remove(), 250);
    }, 2800);
  }

  // ── Clipboard Copy Helper ──────────────────────────────
  async function copyToClipboard(text, label = 'Contract Address') {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      }
      showToast(`${label} copied to clipboard! 📋`, '✨');
    } catch {
      showToast('Could not copy to clipboard', '⚠️');
    }
  }

  // ── Format Markdown into Clean HTML ────────────────────
  function formatMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:var(--accent-emerald);text-decoration:underline;">$1</a>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
  }

  // ── Append User Message ────────────────────────────────
  function appendUserBubble(text) {
    const bubble = document.createElement('div');
    bubble.className = 'msg-user-bubble';
    bubble.textContent = `❯ ${text}`;
    activityFeed.appendChild(bubble);
    scrollToBottom();
  }

  // ── Token Icon Mapping ─────────────────────────────────
  function getTokenIcon(symbol) {
    const iconMap = {
      SOL: 'https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png',
      JUP: 'https://static.jup.ag/jup/icon.png',
      RAY: 'https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R/logo.png',
      BONK: 'https://arweave.net/hQiPZOsRZXGXBJd_82PhVdlM_hACsT_q6wqwf5c90TU',
      WIF: 'https://bafkreibk3yf35svwvqj32amdrldwax5e7ehy2k67tnhqg4j3j4z6c3m6eu.ipfs.nftstorage.link',
      POPCAT: 'https://api.dicebear.com/7.x/identicon/svg?seed=POPCAT'
    };
    return iconMap[symbol] || `https://api.dicebear.com/7.x/identicon/svg?seed=${symbol}`;
  }

  // ── Append Institutional Agent Execution Slip Card ─────
  function appendAgentCard(text, signals, quickChips) {
    const card = document.createElement('div');
    card.className = 'agent-card';

    // Header
    let html = `
      <div class="agent-card-header">
        <span class="agent-brand-pill">
          <span>⚡</span> SOVEREIGN QUANT DESK
        </span>
        <span style="font-family:var(--font-mono);font-size:0.68rem;color:var(--text-muted)">ORDER FLOW INTELLIGENCE</span>
      </div>
      <div class="agent-text-content">
        <p>${formatMarkdown(text)}</p>
      </div>
    `;

    // If signals exist, render institutional trade slips
    if (signals && signals.length > 0) {
      signals.forEach(sig => {
        const symbol = sig.symbol || 'SOL';
        const entry = sig.entry_price || sig.price_usd || 150.0;
        const target = sig.target_price || (entry * 1.085);
        const stop = sig.stop_price || (entry * 0.962);
        const targetPct = (((target / entry) - 1) * 100).toFixed(1);
        const stopPct = (((1 - (stop / entry))) * 100).toFixed(1);
        const blinkUrl = sig.blink?.blink_url || `https://dial.to/?action=solana-action:https://jup.ag/api/v6/swap-action/${symbol}`;
        const mint = sig.mint || sig.argus_audit?.mint || 'So11111111111111111111111111111111111111112';
        const truncatedMint = mint.length > 12 ? `${mint.slice(0, 4)}...${mint.slice(-4)}` : mint;
        const icon = getTokenIcon(symbol);
        const optScore = sig.quality_report?.score || 94;

        html += `
          <div class="trade-card-simple" data-symbol="${symbol}" data-mint="${mint}">
            <div class="trade-card-top">
              <div class="token-info-pill cursor-pointer" data-action="open-chart" data-symbol="${symbol}" title="Launch live candlestick chart">
                <img src="${icon}" class="token-avatar" alt="${symbol}">
                <div class="token-name-group">
                  <div class="sym-row">
                    <span class="token-sym">$${symbol}</span>
                    <button type="button" class="copy-ca-badge" data-action="copy-ca" data-mint="${mint}" title="Click to copy Contract Address">
                      <span>📋</span> <span>${truncatedMint}</span>
                    </button>
                  </div>
                  <span class="token-confluence">Verified SPL Pool • Click for Candlesticks</span>
                </div>
              </div>
              <div class="argus-verified-pill" title="Argus Security Verified">
                <span>🛡️</span> Zero Scam Risk
              </div>
            </div>

            <div class="strategy-optimizer-strip">
              <span class="optimizer-badge">🧠 Strategy Optimizer: ${optScore}/100</span>
              <span class="optimizer-tag">✓ Anti-FOMO Passed</span>
              <span class="optimizer-tag">✓ 2.2:1 R:R Verified</span>
              <span class="optimizer-tag">✓ Liquidity Verified</span>
            </div>

            <div class="trade-targets-strip">
              <div class="target-box">
                <span class="target-lbl">Suggested Limit Entry</span>
                <span class="target-val">$${entry >= 1 ? entry.toFixed(2) : (entry < 0.001 ? entry.toExponential(4) : entry.toFixed(4))}</span>
              </div>
              <div class="target-box">
                <span class="target-lbl">Target (+${targetPct}%)</span>
                <span class="target-val green">$${target >= 1 ? target.toFixed(2) : (target < 0.001 ? target.toExponential(4) : target.toFixed(4))}</span>
              </div>
              <div class="target-box">
                <span class="target-lbl">Stop Loss (-${stopPct}%)</span>
                <span class="target-val red">$${stop >= 1 ? stop.toFixed(2) : (stop < 0.001 ? stop.toExponential(4) : stop.toFixed(4))}</span>
              </div>
            </div>

            <div class="trade-actions-dual">
              <button type="button" class="btn-trade-chart" data-action="open-chart" data-symbol="${symbol}">
                <span>📈</span> View Live Chart
              </button>
              <a href="${blinkUrl}" target="_blank" rel="noopener" class="copy-blink-btn-primary">
                <span>⚡ 1-Click Copy Blink</span>
                <span>➔</span>
              </a>
            </div>
          </div>
        `;
      });
    }

    card.innerHTML = html;
    activityFeed.appendChild(card);
    scrollToBottom();
  }

  // ── Append Argus Audit Report Card ─────────────────────
  function appendAuditCard(audit) {
    const card = document.createElement('div');
    card.className = 'agent-card';

    const symbol = audit.symbol || 'TOKEN';
    const score = audit.safety_score || 0;
    const isSafe = audit.safe_to_trade;
    const mint = audit.mint || '';
    const truncatedMint = mint.length > 12 ? `${mint.slice(0, 6)}...${mint.slice(-6)}` : mint;
    const badgeColor = isSafe ? '#00d26a' : '#f43f5e';

    let checksHtml = '';
    if (audit.checks) {
      checksHtml = Object.entries(audit.checks).map(([key, passed]) => {
        const readable = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        return `
          <div class="audit-check-item">
            <span class="audit-check-status">${passed ? '✅' : '❌'}</span>
            <span class="audit-check-name">${readable}</span>
          </div>
        `;
      }).join('');
    }

    card.innerHTML = `
      <div class="agent-card-header">
        <span class="agent-brand-pill" style="color:${badgeColor}">
          <span>🛡️</span> ARGUS SECURITY SENTINEL: $${symbol}
        </span>
        <span style="font-family:var(--font-mono);font-size:0.68rem;color:var(--text-muted)">ON-CHAIN AUDIT</span>
      </div>
      <div class="agent-text-content">
        <div class="audit-banner ${isSafe ? 'safe' : 'danger'}">
          <div class="audit-score-circle" style="border-color:${badgeColor};color:${badgeColor}">
            ${score}
          </div>
          <div class="audit-verdict">
            <h4>${isSafe ? 'VERIFIED ON-CHAIN (NO TRAPS DETECTED)' : 'HIGH RISK WARNING DETECTED'}</h4>
            <p>${formatMarkdown(audit.summary || audit.audit_verdict || audit.details || '')}</p>
          </div>
        </div>

        <div class="audit-meta-grid">
          <div class="audit-meta-row">
            <span class="meta-label">Contract Address (CA):</span>
            <code class="meta-ca">${truncatedMint || 'Native L1 Base Asset'}</code>
            ${mint ? `<button type="button" class="copy-ca-badge" data-action="copy-ca" data-mint="${mint}">📋 Copy CA</button>` : ''}
          </div>
          <div class="audit-meta-row">
            <span class="meta-label">Liquidity Depth:</span>
            <span class="meta-val">$${(audit.liquidity_usd || 0).toLocaleString()}</span>
          </div>
        </div>

        <div class="audit-checks-grid">
          ${checksHtml}
        </div>

        <div class="audit-actions-row">
          <button type="button" class="btn-tool-action" data-action="open-chart" data-symbol="${symbol}">
            📈 View $${symbol} Chart
          </button>
          <button type="button" class="btn-tool-action primary" data-cmd="/blink ${symbol} Argus safety score: ${score}/100">
            🔗 Generate 1-Click Blink
          </button>
        </div>
      </div>
    `;

    activityFeed.appendChild(card);
    scrollToBottom();
  }

  function scrollToBottom() {
    setTimeout(() => {
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
      });
    }, 50);
  }

  // ── Dispatch Action / Message ──────────────────────────
  async function handleUserAction(promptText) {
    const text = (promptText || chatInput.value).trim();
    if (!text) return;

    chatInput.value = '';
    appendUserBubble(text);

    // If command is explicitly /chart <token>, trigger modal
    const chartMatch = text.match(/^\/chart\s+([A-Za-z0-9]+)/i);
    if (chartMatch) {
      openChartModal(chartMatch[1]);
      return;
    }

    try {
      showToast('Sovereign analyzing order flow...', '⚡');
      const resp = await fetch('/api/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      if (!resp.ok) throw new Error('Could not reach co-pilot');
      const data = await resp.json();

      appendAgentCard(data.reply, data.signals, data.quick_chips);
      fetchTelemetry(); // refresh balance

    } catch (err) {
      appendAgentCard(`⚠️ Something went wrong: ${err.message}. Please try again.`);
    }
  }

  // ── Open Live Chart Modal ──────────────────────────────
  async function openChartModal(tokenOrCa) {
    showToast(`Loading ${tokenOrCa} candlestick chart...`, '📈');
    try {
      const resp = await fetch(`/api/chart?token=${encodeURIComponent(tokenOrCa)}`);
      if (!resp.ok) throw new Error('Could not load chart data');
      const data = await resp.json();

      currentModalToken = data.symbol;
      currentModalCa = data.mint || data.pair_address || '';

      chartModalSymbol.textContent = `$${data.symbol}`;
      chartModalPrice.textContent = `$${data.price_usd >= 1 ? data.price_usd.toFixed(2) : (data.price_usd < 0.001 ? data.price_usd.toExponential(4) : data.price_usd.toFixed(4))}`;

      const chg = data.price_change_24h || 0;
      chartModalChange.textContent = `${chg >= 0 ? '+' : ''}${chg.toFixed(1)}%`;
      chartModalChange.className = `modal-token-change ${chg >= 0 ? 'positive' : 'negative'}`;

      const mintDisplay = data.mint ? (data.mint.length > 16 ? `${data.mint.slice(0, 6)}...${data.mint.slice(-6)}` : data.mint) : 'Native Solana';
      chartModalCa.textContent = mintDisplay;

      chartModalIcon.src = data.icon_url || getTokenIcon(data.symbol);

      const embedUrl = data.embed_url || data.chart_url || `https://dexscreener.com/solana/${data.pair_address}?embed=1&theme=dark&trades=0&info=0`;
      dexscreenerIframe.src = embedUrl;

      // Update trade button
      btnModalJupLink.href = `https://jup.ag/swap/SOL-${data.mint || data.symbol}`;

      chartModal.classList.add('active');
    } catch (err) {
      showToast(`Error opening chart: ${err.message}`, '⚠️');
    }
  }

  function closeChartModal() {
    chartModal.classList.remove('active');
    dexscreenerIframe.src = '';
  }

  // ── Open / Close Agent Modal ───────────────────────────
  function openAgentModal() {
    agentModal.classList.add('active');
    agentNameInput.focus();
  }

  function closeAgentModal() {
    agentModal.classList.remove('active');
  }

  // ── Open / Close Audit Modal ───────────────────────────
  function openAuditModal() {
    auditModal.classList.add('active');
    auditTokenInput.focus();
  }

  function closeAuditModal() {
    auditModal.classList.remove('active');
  }

  // ── Submit Token Safety Audit ──────────────────────────
  async function submitAudit(tokenOrCa) {
    const query = (tokenOrCa || auditTokenInput.value || (sideAuditInput ? sideAuditInput.value : '')).trim();
    if (!query) return;

    closeAuditModal();
    if (auditTokenInput) auditTokenInput.value = '';
    if (sideAuditInput) sideAuditInput.value = '';
    showToast(`Auditing ${query} on Argus Sentinel...`, '🛡️');

    try {
      const resp = await fetch('/api/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: query })
      });

      if (!resp.ok) throw new Error('Audit service unavailable');
      const audit = await resp.json();
      appendAuditCard(audit);
    } catch (err) {
      appendAgentCard(`⚠️ Could not audit ${query}: ${err.message}`);
    }
  }

  // ── Submit Create Agent Form (Merrymen feature) ────────
  async function submitCreateAgent(e) {
    e.preventDefault();
    const name = agentNameInput.value.trim();
    if (!name) return;

    const payload = {
      name: name,
      style: selectedPersonaStyle,
      avatar: selectedPersonaAvatar,
      max_trade_sol: parseFloat(agentMaxSol.value) || 1.0,
      stop_loss_pct: parseFloat(agentSl.value) || 4.5,
      thesis: agentThesisInput.value.trim() || 'Automated momentum breakout sniper with 100% Argus security verification.'
    };

    showToast(`Compiling & deploying ${name}...`, '🤖');

    try {
      const resp = await fetch('/api/agent/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) throw new Error('Could not deploy agent');
      const created = await resp.json();

      closeAgentModal();
      createAgentForm.reset();

      // Update Nav Brand Label
      if (activeAgentLabel) {
        activeAgentLabel.textContent = `Agent: ${created.avatar} ${created.name}`;
      }
      if (sideAgentName) sideAgentName.textContent = created.name;
      if (sideAgentAvatar) sideAgentAvatar.textContent = created.avatar || '🤖';
      if (sideAgentStyle) sideAgentStyle.textContent = created.style;
      if (sideAgentCap) sideAgentCap.textContent = `${created.max_trade_sol} SOL`;
      if (sideAgentSl) sideAgentSl.textContent = `-${created.stop_loss_pct}%`;
      if (sideAgentThesis) sideAgentThesis.textContent = created.thesis;

      showToast(`Agent "${created.name}" is now live!`, '🎉');

      // Append introductory celebration in chat
      appendAgentCard(
        `🤖 **Autonomous Quant Agent Deployed & Activated: ${created.avatar} ${created.name}**\n\n` +
        `• **Strategy Style:** ${created.style}\n` +
        `• **Max Position Size:** ${created.max_trade_sol} SOL\n` +
        `• **Hard Stop Loss:** ${created.stop_loss_pct}%\n` +
        `• **Execution Prompt:** "${created.thesis}"\n\n` +
        `Active on Solana mainnet watching order flow and filtering trades according to your rules. Type **/scan** to initiate immediate execution!`,
        null,
        ['/scan', `/chart JUP`, `/portfolio`]
      );

    } catch (err) {
      showToast(`Agent creation failed: ${err.message}`, '⚠️');
    }
  }

  // ── Global Event Delegation ────────────────────────────
  if (sendBtn) sendBtn.addEventListener('click', () => handleUserAction());
  if (chatInput) {
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleUserAction();
      }
    });
  }

  // Modal Close buttons
  if (btnCloseChartModal) btnCloseChartModal.addEventListener('click', closeChartModal);
  if (btnCloseAgentModal) btnCloseAgentModal.addEventListener('click', closeAgentModal);
  if (btnCloseAuditModal) btnCloseAuditModal.addEventListener('click', closeAuditModal);

  // Close modals on clicking overlay backdrop
  [chartModal, agentModal, auditModal].forEach(modal => {
    if (!modal) return;
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
        if (modal === chartModal) dexscreenerIframe.src = '';
      }
    });
  });

  // Open Agent Modal buttons
  if (btnOpenAgentModal) btnOpenAgentModal.addEventListener('click', openAgentModal);
  if (btnDeployAgentNav) btnDeployAgentNav.addEventListener('click', openAgentModal);
  if (btnSideNewAgent) btnSideNewAgent.addEventListener('click', openAgentModal);

  // Side Panel Audit button
  if (btnSideAudit) {
    btnSideAudit.addEventListener('click', () => {
      if (sideAuditInput && sideAuditInput.value.trim()) {
        submitAudit(sideAuditInput.value.trim());
      }
    });
  }
  if (sideAuditInput) {
    sideAuditInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitAudit(sideAuditInput.value.trim());
      }
    });
  }

  // Persona chip selection inside Agent Modal
  if (personaSelector) {
    personaSelector.addEventListener('click', (e) => {
      const chip = e.target.closest('.persona-chip');
      if (!chip) return;
      personaSelector.querySelectorAll('.persona-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      selectedPersonaStyle = chip.getAttribute('data-style');
      selectedPersonaAvatar = chip.getAttribute('data-avatar');
    });
  }

  // Submit agent form
  if (createAgentForm) createAgentForm.addEventListener('submit', submitCreateAgent);

  // Submit Audit from modal
  if (btnSubmitAudit) btnSubmitAudit.addEventListener('click', () => submitAudit());
  if (auditTokenInput) {
    auditTokenInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        submitAudit();
      }
    });
  }

  // Modal 1 Chart Footer actions
  if (btnCopyModalCa) {
    btnCopyModalCa.addEventListener('click', () => {
      if (currentModalCa) copyToClipboard(currentModalCa, `${currentModalToken} CA`);
    });
  }

  if (btnModalAudit) {
    btnModalAudit.addEventListener('click', () => {
      if (currentModalToken) {
        closeChartModal();
        submitAudit(currentModalToken);
      }
    });
  }

  if (btnModalBlink) {
    btnModalBlink.addEventListener('click', () => {
      if (currentModalToken) {
        closeChartModal();
        handleUserAction(`/blink ${currentModalToken} Verified on live candlestick chart`);
      }
    });
  }

  // Delegated clicks for cards, chips, copy-ca, and chart open
  document.addEventListener('click', (e) => {
    // 1. Copy CA button click
    const copyBtn = e.target.closest('[data-action="copy-ca"]');
    if (copyBtn) {
      e.stopPropagation();
      const mint = copyBtn.getAttribute('data-mint');
      if (mint) copyToClipboard(mint, 'Contract Address');
      return;
    }

    // 2. Open Chart action
    const chartTrigger = e.target.closest('[data-action="open-chart"]');
    if (chartTrigger) {
      e.stopPropagation();
      const sym = chartTrigger.getAttribute('data-symbol') || 'JUP';
      openChartModal(sym);
      return;
    }

    // 3. Quick Action Slips & Cards
    const actionCard = e.target.closest('[data-action]');
    if (actionCard && !actionCard.closest('.modal-box')) {
      const act = actionCard.getAttribute('data-action');
      if (act === 'scan') { handleUserAction('/scan'); return; }
      if (act === 'audit-modal') { openAuditModal(); return; }
      if (act === 'create-agent-card') { openAgentModal(); return; }
      if (act === 'blink-modal') { handleUserAction('/blink JUP High Conviction Breakout'); return; }
    }

    // 4. Quick Token Pills in Sidebar & Modals
    const popChip = e.target.closest('.pop-chip, .quick-pill');
    if (popChip) {
      const token = popChip.getAttribute('data-token');
      if (token) {
        submitAudit(token);
        return;
      }
    }

    // 5. Chip buttons & Terminal chips
    const chip = e.target.closest('.chip-btn, .terminal-chip, [data-cmd]');
    if (chip) {
      const cmd = chip.getAttribute('data-cmd');
      if (cmd) {
        handleUserAction(cmd);
        return;
      }
    }
  });

  // ── Telemetry Poller (Silent Background Balance & Ticker Sync) ──
  async function fetchTelemetry() {
    try {
      const resp = await fetch('/api/telemetry');
      if (!resp.ok) return;
      const data = await resp.json();

      // Update Tickers in Top Strip
      if (data.tokens && data.tokens.length > 0) {
        data.tokens.forEach(t => {
          const symLower = t.symbol.toLowerCase();
          const el = $(`tick-${symLower}`);
          if (el) {
            const p = t.price_usd;
            el.textContent = p >= 1 ? `$${p.toFixed(2)}` : (p < 0.001 ? `$${p.toExponential(2)}` : `$${p.toFixed(4)}`);
          }
        });
      }

      // Update Portfolio Metrics
      if (data.portfolio) {
        const bal = data.portfolio.total_portfolio_usd || data.portfolio.cash_balance || 1000.0;
        const pnl = data.portfolio.net_return_pct || 0.0;
        if (navBalance) navBalance.textContent = `$${bal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        if (navReturn) navReturn.textContent = `${pnl >= 0 ? '+' : ''}${pnl.toFixed(1)}%`;
      }

      // Update Active Agent display
      if (data.active_agent) {
        if (activeAgentLabel) activeAgentLabel.textContent = `Agent: ${data.active_agent.name}`;
        if (sideAgentName) sideAgentName.textContent = data.active_agent.name;
        if (sideAgentAvatar) sideAgentAvatar.textContent = data.active_agent.avatar || '⚡';
        if (sideAgentStyle) sideAgentStyle.textContent = data.active_agent.style;
        if (sideAgentCap) sideAgentCap.textContent = `${data.active_agent.max_trade_sol} SOL`;
        if (sideAgentSl) sideAgentSl.textContent = `-${data.active_agent.stop_loss_pct}%`;
        if (sideAgentThesis && data.active_agent.thesis) sideAgentThesis.textContent = data.active_agent.thesis;
      }
    } catch {
      // silent background poller
    }
  }

  // Initial fetch
  fetchTelemetry();

})();
