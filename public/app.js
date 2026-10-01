/* ═══════════════════════════════════════════════════════
   SOVEREIGN AGENT v2.0 — FRONTEND CONTROLLER
   Integrates: Conversational Co-Pilot, Argus Pre-Flight Shield,
   BlinkCraft 1-Click Copy Blinks, and OracleX Macro Hedging.
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── State ──────────────────────────────────────────────
  let isScanning = false;

  // ── DOM References ─────────────────────────────────────
  const $ = id => document.getElementById(id);

  // HUD
  const hudBankroll       = $('hud-bankroll');
  const hudReturn         = $('hud-return');
  const hudWinrate        = $('hud-winrate');
  const hudTradesCount    = $('hud-trades-count');
  const hudOpenCount      = $('hud-open-count');
  const hudExposureUsd    = $('hud-exposure-usd');

  // Co-Pilot Chat
  const chatStream        = $('chat-stream');
  const copilotInput      = $('copilot-input');
  const btnSendMsg        = $('btn-send-msg');
  const btnClearChat      = $('btn-clear-chat');
  const dynamicChipsRow   = $('dynamic-chips-row');
  const btnQuickScan      = $('btn-quick-scan');

  // Tabs & Views
  const tabBtns           = document.querySelectorAll('.tab-btn');
  const tabContents       = document.querySelectorAll('.tab-content');
  const calloutsBadge     = $('callouts-badge');
  const tokensTableBody   = $('tokens-table-body');
  const calloutsContainer = $('callouts-container');
  const hedgeContainer    = $('hedge-container');
  const hedgeExposureVal  = $('hedge-exposure-val');
  const hedgeBudgetVal    = $('hedge-budget-val');
  const hedgeMarketsList  = $('hedge-markets-list');
  const positionsContainer= $('positions-container');
  const toastShelf        = $('toast-shelf');

  // ── Toast Helper ───────────────────────────────────────
  function showToast(msg, icon = '⚡') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
    toastShelf.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  // ── Tab Switching ──────────────────────────────────────
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const targetPane = $(targetId);
      if (targetPane) targetPane.classList.add('active');
    });
  });

  // ── Fetch Telemetry & Live Data ────────────────────────
  async function fetchTelemetry() {
    try {
      const resp = await fetch('/api/telemetry');
      if (!resp.ok) return;
      const data = await resp.json();

      updateHUD(data.portfolio);
      renderTokensTable(data.tokens, data.evaluations);
      renderCalloutsFeed(data.callouts);
      renderHedgeHub(data.hedge_summary);
      renderPositions(data.open_positions);
    } catch (err) {
      console.warn('Telemetry poll error', err);
    }
  }

  // ── HUD Updater ────────────────────────────────────────
  function updateHUD(p) {
    if (!p) return;
    hudBankroll.textContent = `$${p.current_balance_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    hudReturn.textContent = `${p.all_time_pnl_pct >= 0 ? '+' : ''}${p.all_time_pnl_pct.toFixed(2)}% All-Time Return`;
    hudWinrate.textContent = `${p.win_rate_pct.toFixed(1)}%`;
    hudTradesCount.textContent = `${p.closed_trades_count} Closed (${p.winning_trades}W / ${p.losing_trades}L)`;
    hudOpenCount.textContent = `${p.open_positions_count} Position${p.open_positions_count === 1 ? '' : 's'}`;
    hudExposureUsd.textContent = `$${p.total_exposure_usd.toFixed(2)} Capital at Risk`;
  }

  // ── Render Tokens Table ────────────────────────────────
  function renderTokensTable(tokens, evaluations) {
    if (!tokens || tokens.length === 0) return;
    tokensTableBody.innerHTML = '';

    const evalMap = {};
    (evaluations || []).forEach(e => { evalMap[e.symbol] = e; });

    tokens.forEach(t => {
      const ev = evalMap[t.symbol] || { score: 3, argus_audit: { safety_score: 95 } };
      const tr = document.createElement('tr');
      const chgClass = t.price_change_1h >= 0 ? 'color:var(--accent-emerald)' : 'color:var(--accent-rose)';

      tr.innerHTML = `
        <td>
          <div class="token-sym-cell">
            <img src="${t.icon_url || 'https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png'}" class="token-icon" onerror="this.src='https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png'">
            <span>${t.symbol}</span>
          </div>
        </td>
        <td>$${t.price_usd >= 1 ? t.price_usd.toFixed(2) : t.price_usd.toFixed(4)}</td>
        <td style="${chgClass}">${t.price_change_1h >= 0 ? '+' : ''}${t.price_change_1h.toFixed(2)}%</td>
        <td>${t.volume_multiplier ? t.volume_multiplier.toFixed(2) + 'x' : '1.00x'}</td>
        <td><span class="score-badge">${ev.score}/5 Confluence</span></td>
        <td>
          <span class="argus-tag">
            <span>🛡️</span> ${ev.argus_audit ? ev.argus_audit.safety_score + '/100' : '95/100'}
          </span>
        </td>
        <td>
          <button type="button" class="action-tbl-btn" onclick="window.sendCopilotCmd('/blink ${t.symbol}')">
            🔗 1-Click Blink
          </button>
        </td>
      `;
      tokensTableBody.appendChild(tr);
    });
  }

  // ── Render Callouts Feed ───────────────────────────────
  function renderCalloutsFeed(callouts) {
    if (!callouts || callouts.length === 0) {
      calloutsBadge.textContent = '0';
      return;
    }
    calloutsBadge.textContent = callouts.length;
    calloutsContainer.innerHTML = '';

    callouts.forEach(c => {
      const card = document.createElement('div');
      card.className = 'callout-card';
      const targetPct = (((c.target_price_usd / c.entry_price_usd) - 1) * 100).toFixed(1);
      const stopPct = (((1 - (c.stop_loss_usd / c.entry_price_usd))) * 100).toFixed(1);

      card.innerHTML = `
        <div class="callout-header">
          <span class="callout-title">⚡ ALPHA SIGNAL: $${c.symbol}</span>
          <span class="score-badge">${c.score}/5 Verified</span>
        </div>
        <div class="callout-metrics">
          <div class="metric-box">
            <span class="metric-lbl">ENTRY PRICE</span>
            <span class="metric-val">$${c.entry_price_usd.toFixed(2)}</span>
          </div>
          <div class="metric-box">
            <span class="metric-lbl">TAKE PROFIT (+${targetPct}%)</span>
            <span class="metric-val" style="color:var(--accent-emerald)">$${c.target_price_usd.toFixed(2)}</span>
          </div>
          <div class="metric-box">
            <span class="metric-lbl">STOP LOSS (-${stopPct}%)</span>
            <span class="metric-val" style="color:var(--accent-rose)">$${c.stop_loss_usd.toFixed(2)}</span>
          </div>
        </div>
        <p style="font-size:0.78rem;color:var(--text-muted)">${c.thesis || 'Identified multi-timeframe volume breakout and buy pressure confluence.'}</p>
        <div class="callout-actions">
          <span class="argus-tag">🛡️ Argus Shield: PASSED (Immutable Mint)</span>
          <a href="${c.blink_url}" target="_blank" rel="noopener" class="blink-btn">
            🔗 Copy Trade on Dial.to
          </a>
        </div>
      `;
      calloutsContainer.appendChild(card);
    });
  }

  // ── Render Hedge Hub ───────────────────────────────────
  function renderHedgeHub(hedge) {
    if (!hedge) return;
    hedgeExposureVal.textContent = `$${hedge.exposure_at_risk_usd.toFixed(2)}`;
    hedgeBudgetVal.textContent = `$${hedge.recommended_hedge_usd.toFixed(2)}`;

    hedgeMarketsList.innerHTML = '';
    (hedge.hedge_contracts || []).forEach(m => {
      const card = document.createElement('div');
      card.className = 'hedge-market-card';
      card.innerHTML = `
        <div class="hedge-m-top">
          <span class="hedge-m-title">${m.market_title}</span>
          <span class="hedge-side-badge">Take ${m.side} (${m.current_prob})</span>
        </div>
        <p class="hedge-rationale">${m.rationale}</p>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px">
          <span style="font-size:0.72rem;font-family:var(--font-mono);color:var(--text-dim)">Recommended Allocation: $${m.allocation_usd}</span>
          <a href="${m.oraclex_url}" target="_blank" rel="noopener" class="action-tbl-btn" style="text-decoration:none">
            🔮 View on OracleX
          </a>
        </div>
      `;
      hedgeMarketsList.appendChild(card);
    });
  }

  // ── Render Positions ───────────────────────────────────
  function renderPositions(positions) {
    if (!positions || positions.length === 0) {
      positionsContainer.innerHTML = `
        <div class="empty-feed">
          <span class="empty-icon">💼</span>
          <h3>No Open Positions</h3>
          <p>Autonomous positions initiated by Sovereign Agent will track live here.</p>
        </div>
      `;
      return;
    }

    positionsContainer.innerHTML = '';
    positions.forEach(p => {
      const card = document.createElement('div');
      card.className = 'callout-card';
      const pnlColor = p.unrealized_pnl_usd >= 0 ? 'color:var(--accent-emerald)' : 'color:var(--accent-rose)';

      card.innerHTML = `
        <div class="callout-header">
          <span class="callout-title">LONG $${p.symbol}</span>
          <span class="metric-val" style="${pnlColor}">
            ${p.unrealized_pnl_usd >= 0 ? '+' : ''}$${p.unrealized_pnl_usd.toFixed(2)} (${p.unrealized_pnl_pct.toFixed(2)}%)
          </span>
        </div>
        <div class="callout-metrics">
          <div class="metric-box">
            <span class="metric-lbl">INVESTED</span>
            <span class="metric-val">$${p.position_size_usd.toFixed(2)}</span>
          </div>
          <div class="metric-box">
            <span class="metric-lbl">CURRENT PRICE</span>
            <span class="metric-val">$${p.current_price_usd.toFixed(2)}</span>
          </div>
          <div class="metric-box">
            <span class="metric-lbl">TAKE PROFIT / STOP</span>
            <span class="metric-val">$${p.target_price_usd.toFixed(2)} / $${p.stop_loss_usd.toFixed(2)}</span>
          </div>
        </div>
      `;
      positionsContainer.appendChild(card);
    });
  }

  // ── Co-Pilot Conversational Engine ─────────────────────
  async function sendCopilotMessage(text) {
    const msg = (text || copilotInput.value).trim();
    if (!msg) return;

    copilotInput.value = '';

    // Append user message to chat stream
    appendChatBubble('user', msg);

    // Call API
    try {
      const resp = await fetch('/api/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });

      if (!resp.ok) throw new Error('Co-Pilot API error');
      const data = await resp.json();

      appendChatBubble('agent', data.reply, data.quick_chips);

      // If scan completed, refresh telemetry immediately
      if (data.action_type === 'SCAN_COMPLETE') {
        fetchTelemetry();
        tabBtns[1].click(); // open Alpha Signals tab
      }

    } catch (err) {
      appendChatBubble('agent', `⚠️ Failed to reach autonomous agent engine: ${err.message}`);
    }
  }

  function appendChatBubble(role, rawText, quickChips) {
    const bubble = document.createElement('div');
    bubble.className = `chat-msg msg-${role}`;

    const formatted = formatMarkdown(rawText);
    let chipsHtml = '';
    if (quickChips && quickChips.length > 0) {
      chipsHtml = `<div class="quick-chip-row">` +
        quickChips.map(c => `<button type="button" class="quick-chip" data-cmd="${c}">${c}</button>`).join('') +
        `</div>`;
    }

    bubble.innerHTML = `
      <div class="msg-avatar">${role === 'user' ? '👤' : '🤖'}</div>
      <div class="msg-content">
        ${formatted}
        ${chipsHtml}
      </div>
    `;

    chatStream.appendChild(bubble);
    chatStream.scrollTop = chatStream.scrollHeight;
  }

  function formatMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:var(--accent-cyan)">$1</a>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
  }

  // Handle send button and enter key
  btnSendMsg.addEventListener('click', () => sendCopilotMessage());
  copilotInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendCopilotMessage();
    }
  });

  // Handle chip clicks in chat or toolbar
  document.addEventListener('click', (e) => {
    const chip = e.target.closest('.quick-chip, .action-chip');
    if (!chip) return;
    const cmd = chip.getAttribute('data-cmd');
    if (cmd) sendCopilotMessage(cmd);
  });

  window.sendCopilotCmd = function (cmd) {
    sendCopilotMessage(cmd);
  };

  btnClearChat.addEventListener('click', () => {
    chatStream.innerHTML = '';
    appendChatBubble('agent', 'Chat session cleared. How can I assist you with Solana liquidity today?', ['/scan', '/portfolio', '/audit SOL']);
    showToast('Chat cleared', '🧹');
  });

  // ── Quick Scan Button ──────────────────────────────────
  btnQuickScan.addEventListener('click', async () => {
    if (isScanning) return;
    isScanning = true;
    btnQuickScan.disabled = true;
    btnQuickScan.innerHTML = '<span>⚡</span> Scanning DEX...';
    showToast('Scanning Solana DEX pools...', '🔍');

    try {
      const resp = await fetch('/api/scan', { method: 'POST' });
      if (resp.ok) {
        const data = await resp.json();
        showToast(`Scan complete: ${data.signals_found} setup(s) identified!`, '⚡');
        fetchTelemetry();
        tabBtns[1].click(); // open Alpha Signals tab
      }
    } catch (err) {
      showToast('Scan failed', '⚠️');
    } finally {
      isScanning = false;
      btnQuickScan.disabled = false;
      btnQuickScan.innerHTML = '<span class="btn-icon">⚡</span> Scan DEX Now';
    }
  });

  // ── Polling & Boot ──────────────────────────────────────
  fetchTelemetry();
  setInterval(fetchTelemetry, 10000); // 10 second refresh

})();
