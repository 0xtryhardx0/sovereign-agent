document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const statPortfolio = document.getElementById("stat-portfolio");
  const statReturn = document.getElementById("stat-return");
  const statWinrate = document.getElementById("stat-winrate");
  const statClosed = document.getElementById("stat-closed");
  const statOpen = document.getElementById("stat-open");
  const statExposure = document.getElementById("stat-exposure");
  const scanNowBtn = document.getElementById("scan-now-btn");
  const tokensStrip = document.getElementById("tokens-strip");
  const calloutsContainer = document.getElementById("callouts-container");
  const calloutCounter = document.getElementById("callout-counter");
  const positionsContainer = document.getElementById("positions-container");

  // Initial Fetch & Start Polling
  fetchTelemetry();
  const pollInterval = setInterval(fetchTelemetry, 10000);

  // Manual Scan Button
  scanNowBtn.addEventListener("click", async () => {
    scanNowBtn.disabled = true;
    const btnText = scanNowBtn.querySelector(".scan-text");
    btnText.textContent = "Analyzing Confluences...";

    try {
      const res = await fetch("/api/scan", { method: "POST" });
      const data = await res.json();
      await fetchTelemetry();
    } catch (err) {
      console.error("Scan error:", err);
    } finally {
      scanNowBtn.disabled = false;
      btnText.textContent = "Scan Live DEX Now";
    }
  });

  async function fetchTelemetry() {
    try {
      const res = await fetch("/api/telemetry");
      if (!res.ok) return;
      const data = await res.json();

      updateStats(data.portfolio);
      renderTokensStrip(data.tokens);
      renderCallouts(data.callouts);
      renderPositions(data.open_positions);
    } catch (err) {
      console.error("Fetch telemetry failed:", err);
    }
  }

  function updateStats(p) {
    if (!p) return;
    statPortfolio.textContent = `$${p.total_portfolio_usd.toLocaleString("en-US", { minimumFractionDigits: 2 })}`;
    
    const sign = p.net_pnl_usd >= 0 ? "+" : "";
    statReturn.textContent = `${sign}${p.net_return_pct}% ($${sign}${p.net_pnl_usd.toFixed(2)})`;
    statReturn.className = p.net_pnl_usd >= 0 ? "stat-sub positive" : "stat-sub negative";

    statWinrate.textContent = `${p.win_rate_pct}%`;
    statClosed.textContent = `${p.closed_count} Closed Trades`;
    statOpen.textContent = p.open_count;
    statExposure.textContent = `$${p.open_positions_value.toFixed(2)} At Risk`;
  }

  function renderTokensStrip(tokens) {
    if (!tokens) return;
    tokensStrip.replaceChildren();

    tokens.forEach((t) => {
      const card = document.createElement("div");
      card.className = "token-pill-card";

      const left = document.createElement("div");
      left.className = "token-pill-left";
      const sym = document.createElement("span");
      sym.className = "token-sym";
      sym.textContent = t.symbol;
      const vol = document.createElement("span");
      vol.className = "token-vol";
      vol.textContent = `24h Vol: $${(t.volume_24h / 1e6).toFixed(1)}M (${t.volume_multiplier}x avg)`;
      left.appendChild(sym);
      left.appendChild(vol);

      const right = document.createElement("div");
      right.className = "token-pill-right";
      const price = document.createElement("span");
      price.className = "token-price";
      price.textContent = t.price_usd >= 0.01 ? `$${t.price_usd.toFixed(4)}` : `$${t.price_usd.toFixed(8)}`;
      
      const chg = document.createElement("span");
      const isPos = t.price_change_1h >= 0;
      chg.className = `token-chg ${isPos ? "pos" : "neg"}`;
      chg.textContent = `${isPos ? "+" : ""}${t.price_change_1h.toFixed(2)}% (1h)`;
      right.appendChild(price);
      right.appendChild(chg);

      card.appendChild(left);
      card.appendChild(right);
      tokensStrip.appendChild(card);
    });
  }

  function renderCallouts(callouts) {
    if (!callouts || callouts.length === 0) return;
    calloutCounter.textContent = `${callouts.length} Signals Emitted`;
    calloutsContainer.replaceChildren();

    callouts.forEach((c) => {
      const card = document.createElement("div");
      card.className = "callout-card";

      // Top Row with ID, Tier Badge & Confidence
      const top = document.createElement("div");
      top.className = "callout-top";
      
      const idRow = document.createElement("div");
      idRow.className = "callout-id-row";
      const idSpan = document.createElement("span");
      idSpan.className = "callout-id";
      idSpan.textContent = `⚡ ${c.callout_id || "ALPHA"}`;
      
      const tierBadge = document.createElement("span");
      const isTier1 = (c.confluence_score || 4) >= 4;
      tierBadge.className = `tier-badge ${isTier1 ? "tier-1" : "tier-2"}`;
      tierBadge.textContent = c.tier || (isTier1 ? "Tier 1: High Conviction" : "Tier 2: Tactical");
      idRow.appendChild(idSpan);
      idRow.appendChild(tierBadge);

      const confSpan = document.createElement("span");
      confSpan.className = "callout-conf";
      confSpan.textContent = `${c.confidence_score}% Confidence`;

      top.appendChild(idRow);
      top.appendChild(confSpan);

      // Action Banner
      const actionBanner = document.createElement("div");
      actionBanner.className = "callout-action-banner";
      const actionText = document.createElement("span");
      actionText.className = "callout-action";
      actionText.textContent = `${c.action} ${c.pair}`;
      const entryText = document.createElement("span");
      entryText.className = "callout-entry";
      entryText.textContent = `@ $${c.entry_price.toFixed(4)}`;
      actionBanner.appendChild(actionText);
      actionBanner.appendChild(entryText);

      // Targets Grid (Take Profit & Stop Loss)
      const targetsGrid = document.createElement("div");
      targetsGrid.className = "callout-targets-grid";

      const tpBox = document.createElement("div");
      tpBox.className = "target-box";
      const tpLbl = document.createElement("span");
      tpLbl.className = "target-label";
      tpLbl.textContent = `Target Profit (+${c.take_profit_pct}%)`;
      const tpVal = document.createElement("span");
      tpVal.className = "target-val tp";
      tpVal.textContent = `$${c.target_price.toFixed(4)}`;
      tpBox.appendChild(tpLbl);
      tpBox.appendChild(tpVal);

      const slBox = document.createElement("div");
      slBox.className = "target-box";
      const slLbl = document.createElement("span");
      slLbl.className = "target-label";
      slLbl.textContent = `Stop Loss (-${c.stop_loss_pct}%)`;
      const slVal = document.createElement("span");
      slVal.className = "target-val sl";
      slVal.textContent = `$${c.stop_price.toFixed(4)}`;
      slBox.appendChild(slLbl);
      slBox.appendChild(slVal);

      targetsGrid.appendChild(tpBox);
      targetsGrid.appendChild(slBox);

      // Confluence Checklist Box
      const confBox = document.createElement("div");
      confBox.className = "confluence-box";
      
      const confHeader = document.createElement("div");
      confHeader.className = "confluence-header";
      confHeader.textContent = "🔍 5-Pillar Confluence Verification:";
      const scoreHigh = document.createElement("span");
      scoreHigh.className = "confluence-score-highlight";
      scoreHigh.textContent = `${c.confluence_score || 4} / 5 Passed`;
      confHeader.appendChild(scoreHigh);
      confBox.appendChild(confHeader);

      const checklistList = document.createElement("div");
      checklistList.className = "checklist-list";

      const checklistItems = c.confluence_checklist || [];
      checklistItems.forEach((item) => {
        const itemRow = document.createElement("div");
        itemRow.className = "checklist-item";

        const icon = document.createElement("span");
        icon.className = `check-icon ${item.passed ? "pass" : "fail"}`;
        icon.textContent = item.passed ? "[✓]" : "[✗]";

        const txt = document.createElement("span");
        txt.textContent = `${item.pillar}: ${item.detail}`;

        itemRow.appendChild(icon);
        itemRow.appendChild(txt);
        checklistList.appendChild(itemRow);
      });
      confBox.appendChild(checklistList);

      // Analytical Rationale Box
      const rationaleBox = document.createElement("div");
      rationaleBox.className = "callout-rationale";
      rationaleBox.textContent = c.rationale;

      // Footer Row
      const footer = document.createElement("div");
      footer.className = "callout-footer";
      const copyBtn = document.createElement("button");
      copyBtn.type = "button";
      copyBtn.className = "blink-copy-btn";
      copyBtn.textContent = "⚡ Copy Trade (Solana Blink)";
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(c.formatted_card).then(() => {
          copyBtn.textContent = "✓ Callout Copied!";
          setTimeout(() => {
            copyBtn.textContent = "⚡ Copy Trade (Solana Blink)";
          }, 2000);
        });
      });

      const timeSpan = document.createElement("span");
      timeSpan.className = "callout-time";
      timeSpan.textContent = c.readable_time;

      footer.appendChild(copyBtn);
      footer.appendChild(timeSpan);

      card.appendChild(top);
      card.appendChild(actionBanner);
      card.appendChild(targetsGrid);
      card.appendChild(confBox);
      card.appendChild(rationaleBox);
      card.appendChild(footer);

      calloutsContainer.appendChild(card);
    });
  }

  function renderPositions(positions) {
    if (!positions || positions.length === 0) {
      positionsContainer.replaceChildren();
      const empty = document.createElement("div");
      empty.className = "empty-pos";
      empty.textContent = "No active open positions.";
      positionsContainer.appendChild(empty);
      return;
    }

    positionsContainer.replaceChildren();
    positions.forEach((p) => {
      const card = document.createElement("div");
      card.className = "pos-card";

      const top = document.createElement("div");
      top.className = "pos-top";
      const sym = document.createElement("span");
      sym.textContent = `${p.symbol} (${p.tier || "Active"})`;
      const pnl = document.createElement("span");
      const isPos = p.unrealized_pnl_usd >= 0;
      pnl.className = `pos-pnl ${isPos ? "pos" : "neg"}`;
      pnl.style.color = isPos ? "var(--accent-emerald)" : "var(--accent-rose)";
      pnl.textContent = `${isPos ? "+" : ""}${p.unrealized_pnl_pct}% ($${p.unrealized_pnl_usd.toFixed(2)})`;
      top.appendChild(sym);
      top.appendChild(pnl);

      const details = document.createElement("div");
      details.className = "stat-sub";
      details.textContent = `Entry: $${p.entry_price.toFixed(4)} | Size: $${p.size_usd.toFixed(2)}`;

      card.appendChild(top);
      card.appendChild(details);
      positionsContainer.appendChild(card);
    });
  }
});
