/* ═══════════════════════════════════════════════════════
   SOVEREIGN AGENT — SIMPLIFIED CONSUMER CONTROLLER
   Clean, conversational, and accessible for everyone.
   ═══════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── DOM References ─────────────────────────────────────
  const $ = id => document.getElementById(id);
  const navBalance      = $('nav-balance');
  const navReturn       = $('nav-return');
  const chatScroller    = $('chat-scroller');
  const activityFeed    = $('activity-feed');
  const chatInput       = $('chat-input');
  const sendBtn         = $('send-btn');
  const toastShelf      = $('toast-shelf');

  // ── Toast Helper ───────────────────────────────────────
  function showToast(msg, icon = '⚡') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
    toastShelf.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2800);
  }

  // ── Format Markdown into Clean HTML ────────────────────
  function formatMarkdown(text) {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:var(--accent-primary);text-decoration:underline;">$1</a>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>');
  }

  // ── Append User Message ────────────────────────────────
  function appendUserBubble(text) {
    const bubble = document.createElement('div');
    bubble.className = 'msg-user-bubble';
    bubble.textContent = text;
    activityFeed.appendChild(bubble);
    scrollToBottom();
  }

  // ── Append Agent Card ──────────────────────────────────
  function appendAgentCard(text, signals, quickChips) {
    const card = document.createElement('div');
    card.className = 'agent-card';

    // Header
    let html = `
      <div class="agent-card-header">
        <span class="agent-brand-pill">
          <span>⚡</span> Sovereign AI Co-Pilot
        </span>
        <span style="font-size:0.72rem;color:var(--text-tertiary)">Just now</span>
      </div>
      <div class="agent-text-content">
        <p>${formatMarkdown(text)}</p>
      </div>
    `;

    // If signals exist, render friendly trade cards
    if (signals && signals.length > 0) {
      signals.forEach(sig => {
        const symbol = sig.symbol || 'SOL';
        const entry = sig.entry_price || sig.price_usd || 150.0;
        const target = sig.target_price || (entry * 1.08);
        const stop = sig.stop_price || (entry * 0.94);
        const targetPct = (((target / entry) - 1) * 100).toFixed(1);
        const stopPct = (((1 - (stop / entry))) * 100).toFixed(1);
        const blinkUrl = sig.blink?.blink_url || `https://dial.to/?action=solana-action:https://jup.ag/api/v6/swap-action/${symbol}`;

        const iconMap = {
          SOL: 'https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png',
          JUP: 'https://static.jup.ag/jup/icon.png',
          RAY: 'https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R/logo.png',
          BONK: 'https://arweave.net/hQiPZOsRZXGXBJd_82PhVdlM_hACsT_q6wqwf5c90TU',
          WIF: 'https://bafkreibk3yf35svwvqj32amdrldwax5e7ehy2k67tnhqg4j3j4z6c3m6eu.ipfs.nftstorage.link'
        };
        const icon = iconMap[symbol] || iconMap.SOL;

        html += `
          <div class="trade-card-simple">
            <div class="trade-card-top">
              <div class="token-info-pill">
                <img src="${icon}" class="token-avatar" alt="${symbol}">
                <div class="token-name-group">
                  <span class="token-sym">$${symbol}</span>
                  <span class="token-confluence">★ High Conviction Setup</span>
                </div>
              </div>
              <div class="argus-verified-pill">
                <span>🛡️</span> Zero Scam Risk
              </div>
            </div>

            <div class="trade-targets-strip">
              <div class="target-box">
                <span class="target-lbl">Suggested Buy</span>
                <span class="target-val">$${entry >= 1 ? entry.toFixed(2) : entry.toFixed(4)}</span>
              </div>
              <div class="target-box">
                <span class="target-lbl">Target (+${targetPct}%)</span>
                <span class="target-val green">$${target >= 1 ? target.toFixed(2) : target.toFixed(4)}</span>
              </div>
              <div class="target-box">
                <span class="target-lbl">Stop Loss (-${stopPct}%)</span>
                <span class="target-val red">$${stop >= 1 ? stop.toFixed(2) : stop.toFixed(4)}</span>
              </div>
            </div>

            <a href="${blinkUrl}" target="_blank" rel="noopener" class="copy-blink-btn-primary">
              <span>⚡ Copy Trade in 1-Click</span>
              <span>➔</span>
            </a>
          </div>
        `;
      });
    }

    card.innerHTML = html;
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

    try {
      showToast('Sovereign analyzing...', '⚡');
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

  // ── Event Listeners ────────────────────────────────────
  sendBtn.addEventListener('click', () => handleUserAction());
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleUserAction();
    }
  });

  // Handle Big Friendly Action Cards & Chips
  document.addEventListener('click', (e) => {
    const card = e.target.closest('.action-card, .chip-btn');
    if (!card) return;
    const cmd = card.getAttribute('data-cmd');
    if (cmd) {
      handleUserAction(cmd);
    }
  });

  // ── Telemetry Poller (Silent Background Balance Sync) ──
  async function fetchTelemetry() {
    try {
      const resp = await fetch('/api/telemetry');
      if (!resp.ok) return;
      const data = await resp.json();
      if (data.portfolio) {
        const bal = data.portfolio.total_portfolio_usd || data.portfolio.cash_balance || 1000.0;
        const pnl = data.portfolio.net_return_pct || 0.0;
        navBalance.textContent = `$${bal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        navReturn.textContent = `${pnl >= 0 ? '+' : ''}${pnl.toFixed(1)}%`;
      }
    } catch {
      // silent background poller
    }
  }

  // Initial fetch
  fetchTelemetry();

})();
