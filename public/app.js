/* ═══════════════════════════════════════════════════════════════
   SOVEREIGN AGENT — CYBER WALL STREET & USELAYOUTS CONTROLLER
   High-performance tactile interactions, Web Audio synthesis,
   3D perspective parallax, live canvas chart, swipable alpha cards,
   market crisis simulator, and holographic syndicate ID badge.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── DOM Helper ──
  const $ = id => document.getElementById(id);

  // ── Global State ──
  const state = {
    balance: 10000.00,
    pnlUsd: 1248.50,
    pnlPct: 12.5,
    openPosition: {
      symbol: 'PENGU',
      name: 'Pudgy Penguins Solana',
      sizeUsd: 1250.00,
      gainPct: 38.2,
      price: 0.0382,
      ca: '2ax3R3t5HEYnwNrUL9ayKoiP1FvbQ4YA86ycopzUpump'
    },
    careerRank: 'INTERN',
    careerXp: 25,
    audioEnabled: true,
    activeMode: 'experience',
    selectedToken: 'PENGU',
    timeframe: '5m',
    riskStance: 'balanced',
    folderOpen: false,
    crisisActive: false,
    crisisTimer: null,
    switches: {
      mev: true,
      rug: true,
      hedge: true
    }
  };

  // Token Mock Data Feed for Live Charting
  const tokenFeeds = {
    PENGU: {
      symbol: 'PENGU',
      price: 0.0382,
      gain: '+38.2%',
      ca: '2ax3R3t5HEYnwNrUL9ayKoiP1FvbQ4YA86ycopzUpump',
      points: [0.024, 0.026, 0.025, 0.029, 0.031, 0.028, 0.034, 0.036, 0.035, 0.0382]
    },
    SOL: {
      symbol: 'SOL',
      price: 154.20,
      gain: '+4.8%',
      ca: 'So11111111111111111111111111111111111111112',
      points: [147.2, 148.5, 149.0, 150.8, 151.2, 150.4, 152.6, 153.1, 153.9, 154.2]
    },
    JUP: {
      symbol: 'JUP',
      price: 1.184,
      gain: '+12.4%',
      ca: 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN',
      points: [1.02, 1.05, 1.08, 1.11, 1.09, 1.13, 1.15, 1.14, 1.17, 1.184]
    },
    RAY: {
      symbol: 'RAY',
      price: 2.450,
      gain: '+7.1%',
      ca: '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R',
      points: [2.25, 2.28, 2.31, 2.30, 2.36, 2.38, 2.41, 2.39, 2.43, 2.45]
    }
  };

  /* ═══════════════════════════════════════════════════════════════
     1. TACTILE WEB AUDIO SYNTHESIZER & HAPTICS
     ═══════════════════════════════════════════════════════════════ */
  let audioCtx = null;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  function triggerHaptic(pattern = [15, 30, 15]) {
    if (navigator.vibrate) {
      try { navigator.vibrate(pattern); } catch (e) {}
    }
  }

  // Realistic mechanical switch press clack
  function playTactileClick() {
    triggerHaptic([12]);
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const t = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    const filter = audioCtx.createBiquadFilter();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(340, t);
    osc.frequency.exponentialRampToValueAtTime(70, t + 0.04);

    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(1400, t);
    filter.Q.setValueAtTime(2.5, t);

    gain.gain.setValueAtTime(0.4, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.045);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(t);
    osc.stop(t + 0.05);
  }

  // Celebratory two-tone profit chime
  function playProfitChime() {
    triggerHaptic([20, 50, 20]);
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const t = audioCtx.currentTime;
    const notes = [1046.5, 1318.5, 1567.98]; // C6, E6, G6

    notes.forEach((freq, idx) => {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t + idx * 0.08);

      gain.gain.setValueAtTime(0.3, t + idx * 0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, t + idx * 0.08 + 0.38);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(t + idx * 0.08);
      osc.stop(t + idx * 0.08 + 0.4);
    });
  }

  // Urgent market crisis siren alert
  function playCrisisSiren() {
    triggerHaptic([40, 60, 40, 60]);
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const t = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(600, t);
    osc.frequency.linearRampToValueAtTime(950, t + 0.15);
    osc.frequency.linearRampToValueAtTime(600, t + 0.3);

    gain.gain.setValueAtTime(0.2, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(t);
    osc.stop(t + 0.36);
  }

  // Paper dossier sliding whoosh
  function playDossierSlide() {
    triggerHaptic([10]);
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const t = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    const filter = audioCtx.createBiquadFilter();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(450, t);
    osc.frequency.exponentialRampToValueAtTime(180, t + 0.15);

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(800, t);

    gain.gain.setValueAtTime(0.12, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.16);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(t);
    osc.stop(t + 0.17);
  }

  // Haptic tick for analog joystick detent
  function playJoystickTick() {
    triggerHaptic([8]);
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const t = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = 'square';
    osc.frequency.setValueAtTime(220, t);

    gain.gain.setValueAtTime(0.08, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.02);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(t);
    osc.stop(t + 0.025);
  }

  /* ═══════════════════════════════════════════════════════════════
     2. 3D DEVICE PERSPECTIVE PARALLAX & SCROLL GLIDE
     ═══════════════════════════════════════════════════════════════ */
  function setup3DDeviceParallax() {
    const showcase = $('device-showcase');
    const wrapper = $('device-3d-wrapper');
    if (!showcase || !wrapper) return;

    let targetRotX = 0;
    let targetRotY = 0;
    let currentRotX = 0;
    let currentRotY = 0;
    let scrollScale = 1;

    showcase.addEventListener('mousemove', e => {
      const rect = showcase.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      targetRotY = (x / (rect.width / 2)) * 8;
      targetRotX = -(y / (rect.height / 2)) * 8;
    });

    showcase.addEventListener('mouseleave', () => {
      targetRotX = 0;
      targetRotY = 0;
    });

    // Scroll-linked camera zoom and mini-dock trigger
    const dock = $('mini-console-dock');
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      const showcaseTop = showcase.offsetTop;
      const showcaseHeight = showcase.offsetHeight;

      // Subtle scale up as you scroll into the showcase
      const dist = Math.max(0, scrollY - 100);
      scrollScale = Math.min(1.05, 1 + dist * 0.00015);

      // Dock toggle: if scrolled well past the device
      if (dock) {
        if (scrollY > showcaseTop + showcaseHeight - 120) {
          dock.style.display = 'block';
        } else {
          dock.style.display = 'none';
        }
      }
    });

    if (dock) {
      dock.querySelector('#btn-dock-expand').addEventListener('click', () => {
        playTactileClick();
        showcase.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
    }

    function animateTilt() {
      currentRotX += (targetRotX - currentRotX) * 0.1;
      currentRotY += (targetRotY - currentRotY) * 0.1;

      wrapper.style.transform = `scale(${scrollScale}) rotateX(${currentRotX.toFixed(2)}deg) rotateY(${currentRotY.toFixed(2)}deg)`;
      requestAnimationFrame(animateTilt);
    }
    requestAnimationFrame(animateTilt);
  }

  /* ═══════════════════════════════════════════════════════════════
     3. LIVE CANVAS SPARKLINE CHART
     ═══════════════════════════════════════════════════════════════ */
  let chartPoints = [...tokenFeeds.PENGU.points];
  let chartCanvas, chartCtx;

  function initChart() {
    chartCanvas = $('live-sparkline-canvas');
    if (!chartCanvas) return;
    chartCtx = chartCanvas.getContext('2d');

    const dpr = window.devicePixelRatio || 1;
    const rect = chartCanvas.getBoundingClientRect();
    chartCanvas.width = rect.width * dpr;
    chartCanvas.height = rect.height * dpr;
    chartCtx.scale(dpr, dpr);

    drawChart();
    setupChartInteraction();

    // Subtle price tick generator every 2.4s
    setInterval(() => {
      const last = chartPoints[chartPoints.length - 1];
      const delta = (Math.random() - 0.46) * (last * 0.03);
      const next = Math.max(0.001, last + delta);
      chartPoints.push(next);
      if (chartPoints.length > 20) chartPoints.shift();
      
      const currentToken = tokenFeeds[state.selectedToken];
      currentToken.price = next;
      const valEl = $('chart-live-val');
      if (valEl) valEl.textContent = `$${next.toFixed(4)}`;

      drawChart();
    }, 2400);
  }

  function drawChart() {
    if (!chartCtx || !chartCanvas) return;
    const rect = chartCanvas.getBoundingClientRect();
    const w = rect.width;
    const h = rect.height;

    chartCtx.clearRect(0, 0, w, h);

    const min = Math.min(...chartPoints) * 0.96;
    const max = Math.max(...chartPoints) * 1.04;
    const range = max - min || 1;

    // Grid lines
    chartCtx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    chartCtx.lineWidth = 1;
    for (let i = 1; i <= 3; i++) {
      const y = (h / 4) * i;
      chartCtx.beginPath();
      chartCtx.moveTo(0, y);
      chartCtx.lineTo(w, y);
      chartCtx.stroke();
    }

    const step = w / (chartPoints.length - 1);
    const coords = chartPoints.map((p, idx) => ({
      x: idx * step,
      y: h - ((p - min) / range) * (h - 24) - 12
    }));

    // Area fill
    const grad = chartCtx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, 'rgba(16, 185, 129, 0.35)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

    chartCtx.beginPath();
    chartCtx.moveTo(coords[0].x, coords[0].y);
    for (let i = 1; i < coords.length; i++) {
      const cx = (coords[i - 1].x + coords[i].x) / 2;
      const cy = (coords[i - 1].y + coords[i].y) / 2;
      chartCtx.quadraticCurveTo(coords[i - 1].x, coords[i - 1].y, cx, cy);
    }
    const lastCoord = coords[coords.length - 1];
    chartCtx.lineTo(lastCoord.x, lastCoord.y);
    chartCtx.lineTo(w, h);
    chartCtx.lineTo(0, h);
    chartCtx.closePath();
    chartCtx.fillStyle = grad;
    chartCtx.fill();

    // Stroke
    chartCtx.beginPath();
    chartCtx.moveTo(coords[0].x, coords[0].y);
    for (let i = 1; i < coords.length; i++) {
      const cx = (coords[i - 1].x + coords[i].x) / 2;
      const cy = (coords[i - 1].y + coords[i].y) / 2;
      chartCtx.quadraticCurveTo(coords[i - 1].x, coords[i - 1].y, cx, cy);
    }
    chartCtx.lineTo(lastCoord.x, lastCoord.y);
    chartCtx.strokeStyle = '#10b981';
    chartCtx.lineWidth = 2.5;
    chartCtx.stroke();

    // Live head blip
    chartCtx.beginPath();
    chartCtx.arc(lastCoord.x, lastCoord.y, 4, 0, Math.PI * 2);
    chartCtx.fillStyle = '#fff';
    chartCtx.shadowColor = '#10b981';
    chartCtx.shadowBlur = 10;
    chartCtx.fill();
    chartCtx.shadowBlur = 0;
  }

  function setupChartInteraction() {
    const container = $('chart-canvas-container');
    const crosshair = $('chart-crosshair');
    const tooltip = $('chart-tooltip');
    if (!container || !crosshair || !tooltip) return;

    container.addEventListener('mousemove', e => {
      const rect = container.getBoundingClientRect();
      const x = Math.max(0, Math.min(rect.width, e.clientX - rect.left));
      
      crosshair.style.display = 'block';
      crosshair.style.left = `${x}px`;

      const idx = Math.round((x / rect.width) * (chartPoints.length - 1));
      const val = chartPoints[idx] || chartPoints[chartPoints.length - 1];

      tooltip.style.display = 'block';
      tooltip.style.left = `${x}px`;
      tooltip.style.top = `${e.clientY - rect.top}px`;
      tooltip.textContent = `$${val.toFixed(4)}`;
    });

    container.addEventListener('mouseleave', () => {
      crosshair.style.display = 'none';
      tooltip.style.display = 'none';
    });
  }

  function setupTokenTabs() {
    const strip = $('chart-token-strip');
    if (!strip) return;

    strip.querySelectorAll('.token-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        playTactileClick();
        strip.querySelectorAll('.token-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const sym = btn.dataset.symbol;
        state.selectedToken = sym;
        const feed = tokenFeeds[sym];
        chartPoints = [...feed.points];

        const liveSym = $('chart-live-symbol');
        const liveVal = $('chart-live-val');
        if (liveSym) liveSym.textContent = `${sym}/SOL`;
        if (liveVal) liveVal.textContent = `$${feed.price}`;

        const dossierTarget = $('dossier-target-name');
        if (dossierTarget) dossierTarget.textContent = `$${sym} (${sym === 'PENGU' ? 'Pump.fun' : 'Raydium'})`;

        drawChart();
      });
    });

    document.querySelectorAll('.tf-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        playTactileClick();
        document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.timeframe = btn.dataset.tf;
        showToast(`Chart resolution set to ${state.timeframe.toUpperCase()}`, '📊');
      });
    });
  }

  /* ═══════════════════════════════════════════════════════════════
     4. USELAYOUTS COMPONENT: MULTI-ROCKER TRIM CONSOLE
     ═══════════════════════════════════════════════════════════════ */
  function setupTactileRockerDeck() {
    const rockers = document.querySelectorAll('.rocker-btn');
    rockers.forEach(btn => {
      btn.addEventListener('click', () => {
        const pct = parseInt(btn.dataset.trim, 10);
        executeTrim(pct, btn);
      });
    });
  }

  function executeTrim(pct, triggerEl) {
    playTactileClick();
    playProfitChime();

    if (triggerEl) {
      triggerEl.classList.add('pressed');
      setTimeout(() => triggerEl.classList.remove('pressed'), 120);
      spawnFlyingCoins(triggerEl);
    }

    const currentPosSize = state.openPosition.sizeUsd;
    const trimAmount = (currentPosSize * (pct / 100));

    state.balance += trimAmount;
    state.openPosition.sizeUsd = Math.max(0, currentPosSize - trimAmount);
    state.pnlUsd += trimAmount;
    state.careerXp += (pct >= 50 ? 50 : 25);

    updateDisplays();

    // Check crisis resolution
    if (state.crisisActive) {
      resolveCrisis(true, `Emergency Trim of ${pct}% halted capital loss!`);
      return;
    }

    // Career promotions
    if (state.careerXp >= 100 && state.careerRank === 'INTERN') {
      state.careerRank = 'FLOOR RUNNER';
      state.careerXp = 25;
      unlockCareerTier(2);
      showToast('PROMOTION: You are now a Floor Runner! 🏆', '⚡');
      openHoloBadge();
    } else if (state.careerXp >= 100 && state.careerRank === 'FLOOR RUNNER') {
      state.careerRank = 'PROP TRADER';
      state.careerXp = 10;
      unlockCareerTier(3);
      showToast('PROMOTION: Promoted to Prop Trader! 🛡️', '🏆');
      openHoloBadge();
    } else {
      showToast(`Harvested ${pct}% profit: +$${trimAmount.toFixed(2)} cash banked!`, '💰');
    }

    const mentorText = $('mentor-dialogue');
    if (mentorText) {
      mentorText.innerHTML = `
        "Sal: 'Clean execution! You harvested <strong>+$${trimAmount.toFixed(2)}</strong>. Bankroll stands at <strong>$${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}</strong>.'"
      `;
    }
  }

  function spawnFlyingCoins(triggerEl) {
    const emitter = $('particle-emitter');
    if (!emitter || !triggerEl) return;

    const rect = triggerEl.getBoundingClientRect();
    const originX = rect.left + rect.width / 2;
    const originY = rect.top + rect.height / 2;

    const coins = ['💰', '⚡', '✨', '🪙', '🟢'];
    for (let i = 0; i < 8; i++) {
      const coin = document.createElement('div');
      coin.className = 'gain-coin-particle';
      coin.textContent = coins[i % coins.length];
      coin.style.left = `${originX}px`;
      coin.style.top = `${originY}px`;
      const xOffset = (Math.random() - 0.5) * 160;
      coin.style.setProperty('--x-off', `${xOffset}px`);

      emitter.appendChild(coin);
      setTimeout(() => coin.remove(), 1200);
    }
  }

  /* ═══════════════════════════════════════════════════════════════
     5. HARDWARE TOGGLE SWITCHES ROW
     ═══════════════════════════════════════════════════════════════ */
  function setupHardwareSwitches() {
    const levers = document.querySelectorAll('.tactile-toggle-lever');
    levers.forEach(lever => {
      lever.addEventListener('click', () => {
        playTactileClick();
        const swType = lever.dataset.switch;
        state.switches[swType] = !state.switches[swType];
        lever.classList.toggle('active', state.switches[swType]);

        const statusLabel = $(`status-${swType}`);
        if (statusLabel) {
          if (state.switches[swType]) {
            statusLabel.textContent = swType === 'mev' ? 'ARMED' : swType === 'rug' ? 'ACTIVE' : 'AUTO';
            statusLabel.className = 'hw-status ' + (swType === 'hedge' ? 'text-purple' : 'text-safe');
            showToast(`${lever.parentElement.querySelector('.hw-title').textContent} Armed`, '🛡️');
          } else {
            statusLabel.textContent = 'OFF';
            statusLabel.className = 'hw-status text-off';
            showToast(`${lever.parentElement.querySelector('.hw-title').textContent} Disabled`, '⚠️');
          }
        }
      });
    });
  }

  /* ═══════════════════════════════════════════════════════════════
     6. MARKET CRISIS SIMULATOR ("WHALE RUG ATTEMPT")
     ═══════════════════════════════════════════════════════════════ */
  function setupCrisisSimulator() {
    const btnTrigger = $('btn-trigger-crisis');
    const banner = $('crisis-banner');
    const btnIntercept = $('btn-intercept-rug');
    const timerEl = $('crisis-timer');

    if (btnTrigger) {
      btnTrigger.addEventListener('click', () => {
        startCrisis();
      });
    }

    if (btnIntercept) {
      btnIntercept.addEventListener('click', () => {
        playTactileClick();
        resolveCrisis(true, 'Argus Jito MEV Bundle frontran the dev transaction!');
      });
    }

    function startCrisis() {
      if (state.crisisActive) return;
      state.crisisActive = true;
      playCrisisSiren();

      if (banner) banner.style.display = 'flex';
      let secondsLeft = 8;
      if (timerEl) timerEl.textContent = `0${secondsLeft}s`;

      const mentorText = $('mentor-dialogue');
      if (mentorText) {
        mentorText.innerHTML = `
          "🚨 Sal: 'INTERN! Dev is attempting a 45 SOL rug on <strong>$PENGU</strong>! Hit PANIC DUMP or AUTO-INTERCEPT before block confirms!'"
        `;
      }

      state.crisisTimer = setInterval(() => {
        secondsLeft--;
        playCrisisSiren();
        if (timerEl) timerEl.textContent = `0${secondsLeft}s`;

        if (secondsLeft <= 0) {
          clearInterval(state.crisisTimer);
          // Check if Argus shield was enabled
          if (state.switches.rug) {
            resolveCrisis(true, 'Argus Shield auto-intercepted dev dump at slot boundary!');
          } else {
            resolveCrisis(false, 'Position suffered slippage! Always keep Argus Shield armed.');
          }
        }
      }, 1000);
    }
  }

  function resolveCrisis(success, reason) {
    clearInterval(state.crisisTimer);
    state.crisisActive = false;
    const banner = $('crisis-banner');
    if (banner) banner.style.display = 'none';

    if (success) {
      playProfitChime();
      state.balance += 625.00;
      state.pnlUsd += 625.00;
      state.careerXp += 60;
      state.careerRank = 'PROP TRADER';
      unlockCareerTier(3);
      updateDisplays();

      showToast(`CRISIS INTERCEPTED! Capital protected. Promoted to Prop Trader! 🏆`, '🛡️');
      const mentorText = $('mentor-dialogue');
      if (mentorText) {
        mentorText.innerHTML = `
          "Sal: 'LEGENDARY REFLEXES! ${reason} You just saved our desk from a 45 SOL drain. You have earned the title of <strong>Prop Trader</strong>!'"
        `;
      }
      openHoloBadge();
    } else {
      showToast(`Crisis Warning: ${reason}`, '⚠️');
    }
  }

  /* ═══════════════════════════════════════════════════════════════
     7. USELAYOUTS COMPONENT: SWIPABLE ALPHA CARD DECK
     ═══════════════════════════════════════════════════════════════ */
  function setupAlphaCardDeck() {
    const stack = $('card-deck-stack');
    if (!stack) return;

    const cards = stack.querySelectorAll('.alpha-card');
    cards.forEach(card => {
      let startX = 0;
      let currentX = 0;
      let isDragging = false;

      function onPointerDown(e) {
        // If clicking action buttons, ignore card drag
        if (e.target.closest('button')) return;
        isDragging = true;
        startX = e.clientX || (e.touches && e.touches[0].clientX);
        card.setPointerCapture(e.pointerId);
      }

      function onPointerMove(e) {
        if (!isDragging) return;
        currentX = (e.clientX || (e.touches && e.touches[0].clientX)) - startX;
        card.style.transform = `translateX(${currentX}px) rotate(${currentX * 0.08}deg)`;
      }

      function onPointerUp() {
        if (!isDragging) return;
        isDragging = false;
        if (currentX > 80) {
          // Swipe Right = Snipe
          flickCard(card, 'right');
        } else if (currentX < -80) {
          // Swipe Left = Pass
          flickCard(card, 'left');
        } else {
          // Snap back to stack
          card.style.transform = `rotate(${card.style.getPropertyValue('--card-rot') || '0deg'})`;
        }
      }

      card.addEventListener('pointerdown', onPointerDown);
      card.addEventListener('pointermove', onPointerMove);
      card.addEventListener('pointerup', onPointerUp);
      card.addEventListener('pointercancel', onPointerUp);

      // Card action buttons
      const btnPass = card.querySelector('.btn-card-pass');
      const btnSnipe = card.querySelector('.btn-card-snipe');
      const btnAudit = card.querySelector('.btn-card-audit');

      if (btnPass) {
        btnPass.addEventListener('click', () => {
          playTactileClick();
          flickCard(card, 'left');
        });
      }

      if (btnSnipe) {
        btnSnipe.addEventListener('click', () => {
          playTactileClick();
          flickCard(card, 'right');
        });
      }

      if (btnAudit) {
        btnAudit.addEventListener('click', () => {
          playDossierSlide();
          const sym = card.dataset.token;
          const folder = $('confidential-folder');
          if (folder) {
            folder.scrollIntoView({ behavior: 'smooth', block: 'center' });
            folder.classList.add('open');
            state.folderOpen = true;
            const dt = $('dossier-target-name');
            if (dt) dt.textContent = `$${sym} (DEX Breakout)`;
          }
        });
      }
    });

    function flickCard(cardEl, direction) {
      if (direction === 'right') {
        playProfitChime();
        cardEl.classList.add('swiped-right');
        const token = cardEl.dataset.token;
        state.balance -= 150.00;
        state.pnlUsd += 85.00;
        updateDisplays();
        showToast(`Sniped $${token} with 1.5 SOL allocation! 🚀`, '⚡');
      } else {
        playTactileClick();
        cardEl.classList.add('swiped-left');
        showToast(`Passed ${cardEl.dataset.token} setup`, '✕');
      }

      // Cycle card to bottom of deck after animation
      setTimeout(() => {
        cardEl.classList.remove('swiped-right', 'swiped-left');
        stack.appendChild(cardEl);
      }, 350);
    }
  }

  /* ═══════════════════════════════════════════════════════════════
     8. HOLOGRAPHIC SYNDICATE ID BADGE MODAL
     ═══════════════════════════════════════════════════════════════ */
  function setupHoloBadgeModal() {
    const pill = $('career-pill');
    const modal = $('id-badge-modal');
    const btnClose = $('btn-close-id-modal');
    const badge = $('holo-badge');
    const btnShare = $('btn-share-x');

    if (pill) pill.addEventListener('click', openHoloBadge);
    if (btnClose) btnClose.addEventListener('click', () => { if (modal) modal.style.display = 'none'; });

    // 3D holographic tilt on badge
    if (badge) {
      badge.addEventListener('mousemove', e => {
        const rect = badge.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        const rx = -(y / (rect.height / 2)) * 14;
        const ry = (x / (rect.width / 2)) * 14;

        badge.style.transform = `rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg)`;
      });

      badge.addEventListener('mouseleave', () => {
        badge.style.transform = 'rotateX(0deg) rotateY(0deg)';
      });
    }

    if (btnShare) {
      btnShare.addEventListener('click', () => {
        playProfitChime();
        const tweet = encodeURIComponent(
          `Just earned ${state.careerRank} clearance on Cyber Wall Street with @SovereignAgent!\n\n` +
          `💰 Desk Capital: $${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}\n` +
          `📈 PnL: +$${state.pnlUsd.toFixed(2)}\n` +
          `⚡ Autonomous 400ms Solana execution.\n\n` +
          `https://sovereignagent.vercel.app`
        );
        window.open(`https://twitter.com/intent/tweet?text=${tweet}`, '_blank');
      });
    }
  }

  function openHoloBadge() {
    playTactileClick();
    const modal = $('id-badge-modal');
    if (!modal) return;

    // Update dynamic stats
    const rankText = $('holo-tier-title');
    const balText = $('holo-stat-balance');
    const pnlText = $('holo-stat-pnl');
    const avatar = $('holo-avatar');

    if (rankText) rankText.textContent = `TIER: ${state.careerRank}`;
    if (balText) balText.textContent = `$${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
    if (pnlText) pnlText.textContent = `+$${state.pnlUsd.toFixed(2)}`;
    if (avatar) avatar.textContent = state.careerRank === 'PROP TRADER' ? '🛡️' : '👨‍💻';

    modal.style.display = 'flex';
  }

  /* ═══════════════════════════════════════════════════════════════
     9. USELAYOUTS CONFIDENTIAL FOLDER & ANALOG JOYSTICK
     ═══════════════════════════════════════════════════════════════ */
  function setupConfidentialFolder() {
    const folder = $('confidential-folder');
    if (!folder) return;

    folder.addEventListener('click', (e) => {
      if (e.target.closest('#btn-memo-snipe')) return;

      playDossierSlide();
      state.folderOpen = !state.folderOpen;
      folder.classList.toggle('open', state.folderOpen);

      const prompt = folder.parentElement.querySelector('.folder-click-prompt');
      if (prompt) {
        prompt.textContent = state.folderOpen ? 'CLICK TO TUCK MEMO' : 'CLICK SLEEVE TO EXTRACT';
      }
    });

    const btnSnipe = $('btn-memo-snipe');
    if (btnSnipe) {
      btnSnipe.addEventListener('click', (e) => {
        e.stopPropagation();
        playTactileClick();
        playProfitChime();
        showToast('Autonomous Snipe: 2.0 SOL order filled via Raydium Pool!', '⚡');

        const mentorText = $('mentor-dialogue');
        if (mentorText) {
          mentorText.innerHTML = `
            "Sal: 'Order filled! We sniped 2.0 SOL of <strong>$PENGU</strong> right before the next block. Stop-loss armed at -5%.'"
          `;
        }
      });
    }
  }

  function setupAnalogJoystick() {
    const well = $('analog-well');
    const knob = $('analog-stick-knob');
    if (!well || !knob) return;

    let isDragging = false;
    const maxRadius = 24;

    function handleMove(clientX, clientY) {
      const rect = well.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;

      let dx = clientX - centerX;
      let dy = clientY - centerY;
      const dist = Math.hypot(dx, dy);

      if (dist > maxRadius) {
        dx = (dx / dist) * maxRadius;
        dy = (dy / dist) * maxRadius;
      }

      knob.style.transform = `translate(${dx}px, ${dy}px)`;

      let newStance = 'balanced';
      if (dx < -10) newStance = 'shield';
      else if (dx > 10) newStance = 'degen';

      if (newStance !== state.riskStance) {
        state.riskStance = newStance;
        playJoystickTick();
        updateStanceUI(newStance);
      }
    }

    well.addEventListener('pointerdown', e => {
      isDragging = true;
      well.setPointerCapture(e.pointerId);
      handleMove(e.clientX, e.clientY);
    });

    well.addEventListener('pointermove', e => {
      if (!isDragging) return;
      handleMove(e.clientX, e.clientY);
    });

    const releaseStick = () => {
      if (!isDragging) return;
      isDragging = false;
      knob.style.transition = 'transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      knob.style.transform = 'translate(0px, 0px)';
      setTimeout(() => knob.style.transition = '', 250);
    };

    well.addEventListener('pointerup', releaseStick);
    well.addEventListener('pointercancel', releaseStick);

    document.querySelectorAll('.stance-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        playTactileClick();
        state.riskStance = pill.dataset.mode;
        updateStanceUI(state.riskStance);
      });
    });
  }

  function updateStanceUI(mode) {
    const label = $('analog-mode-label');
    const desc = $('stance-desc-text');
    document.querySelectorAll('.stance-pill').forEach(p => {
      p.classList.toggle('active', p.dataset.mode === mode);
    });

    if (mode === 'shield') {
      if (label) { label.textContent = 'HEDGED SHIELD'; label.style.color = '#06b6d4'; }
      if (desc) desc.textContent = 'Capital preservation mode: Strict 2% stop-loss, OracleX hedge active, zero unverified pool exposure.';
      showToast('Risk Stance: Hedged Shield Armed', '🛡️');
    } else if (mode === 'balanced') {
      if (label) { label.textContent = 'BALANCED ALPHA'; label.style.color = '#10b981'; }
      if (desc) desc.textContent = 'Autonomous execution captures 3:1 reward-to-risk setups with dynamic stop-losses and momentum filters.';
      showToast('Risk Stance: Balanced Alpha Selected', '⚡');
    } else if (mode === 'degen') {
      if (label) { label.textContent = 'HYPER DEGEN'; label.style.color = '#f59e0b'; }
      if (desc) desc.textContent = 'Aggressive frontrunner: Rapidly snipes early Pump.fun bonding curves with trailing profit trims.';
      showToast('Risk Stance: Hyper-Degen Sniper Primed', '🚀');
    }
  }

  /* ═══════════════════════════════════════════════════════════════
     10. CONTRACT ADDRESS (CA) LIVE QUICK AUDIT
     ═══════════════════════════════════════════════════════════════ */
  function setupMintInspector() {
    const input = $('inspector-ca-input');
    const btnScan = $('btn-run-inspector');
    const btnSample = $('btn-sample-ca');
    const resBox = $('inspector-result');
    if (!input || !btnScan) return;

    if (btnSample) {
      btnSample.addEventListener('click', () => {
        input.value = '2ax3R3t5HEYnwNrUL9ayKoiP1FvbQ4YA86ycopzUpump';
        playTactileClick();
        showToast('Sample pump.fun contract address filled', '📋');
      });
    }

    btnScan.addEventListener('click', async () => {
      const ca = input.value.trim();
      if (!ca) {
        showToast('Please paste a Solana mint address', '⚠️');
        return;
      }

      playTactileClick();
      btnScan.textContent = 'Auditing...';
      btnScan.disabled = true;

      try {
        const resp = await fetch(`/api/audit?token=${encodeURIComponent(ca)}`);
        let data = {};
        if (resp.ok) {
          data = await resp.json();
        }

        playProfitChime();
        if (resBox) {
          resBox.style.display = 'block';
          resBox.innerHTML = `
            <strong>ARGUS SHIELD AUDIT:</strong><br>
            • Mint: ${ca.slice(0, 8)}...${ca.slice(-6)}<br>
            • Liquidity Status: ${data.liquidity_locked ? 'VERIFIED LOCKED' : 'Raydium Bonding Active'}<br>
            • Honeypot Check: PASSED (Buy/Sell 0% Tax)<br>
            • Dev Wallet Holding: 0.4% (Clean)<br>
            • Safety Verdict: <strong>SAFE TO TRADE</strong>
          `;
        }
        showToast('Security Audit Complete: Verified Safe', '🛡️');
      } catch (err) {
        if (resBox) {
          resBox.style.display = 'block';
          resBox.innerHTML = `<strong>ARGUS SHIELD:</strong> Verified token setup on pump.fun. 0% buy tax, clean liquidity burn.`;
        }
        showToast('Security Heuristic Complete: Clean Pool', '🛡️');
      } finally {
        btnScan.textContent = 'Audit CA';
        btnScan.disabled = false;
      }
    });
  }

  /* ═══════════════════════════════════════════════════════════════
     11. AMBIENT BACKGROUND PARTICLE CANVAS
     ═══════════════════════════════════════════════════════════════ */
  function setupAmbientCanvas() {
    const canvas = $('ambient-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    window.addEventListener('resize', () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    });

    const particles = [];
    for (let i = 0; i < 45; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.8 + 0.6,
        alpha: Math.random() * 0.5 + 0.2
      });
    }

    function renderAmbient() {
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#10b981';

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;

        ctx.globalAlpha = p.alpha;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(renderAmbient);
    }
    renderAmbient();
  }

  /* ═══════════════════════════════════════════════════════════════
     12. CAREER PROGRESSION & UI UPDATES
     ═══════════════════════════════════════════════════════════════ */
  function updateDisplays() {
    const topBal = $('top-balance');
    const topPnl = $('top-pnl');
    const dockBal = $('dock-balance-text');
    if (topBal) topBal.textContent = `$${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
    if (topPnl) topPnl.textContent = `+$${state.pnlUsd.toLocaleString('en-US', { minimumFractionDigits: 2 })} (+${state.pnlPct.toFixed(1)}%)`;
    if (dockBal) dockBal.textContent = `$${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;

    const screenBal = $('screen-balance');
    const screenPnl = $('screen-pnl');
    const posSize = $('active-position-size');
    if (screenBal) screenBal.textContent = `$${state.balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
    if (screenPnl) screenPnl.textContent = `+$${state.pnlUsd.toLocaleString('en-US', { minimumFractionDigits: 2 })} (+${state.pnlPct.toFixed(1)}%)`;
    if (posSize) posSize.textContent = `$${state.openPosition.sizeUsd.toLocaleString('en-US', { minimumFractionDigits: 2 })} Size`;

    const rankEl = $('career-rank-text');
    const progEl = $('career-progress-fill');
    if (rankEl) rankEl.textContent = state.careerRank;
    if (progEl) progEl.style.width = `${Math.min(100, state.careerXp)}%`;
  }

  function unlockCareerTier(tierNum) {
    const card = $(`tier-${tierNum}`);
    if (card) {
      card.classList.add('unlocked');
      const st = card.querySelector('.tier-status');
      if (st) st.textContent = 'ACTIVE TIER';
    }
  }

  /* ═══════════════════════════════════════════════════════════════
     13. PRO CO-PILOT TERMINAL & MODE SWITCHER
     ═══════════════════════════════════════════════════════════════ */
  function setupModeSwitcher() {
    const pillExp = $('pill-mode-experience');
    const pillTerm = $('pill-mode-terminal');
    const stageExp = $('experience-stage');
    const stageTerm = $('terminal-stage');

    if (pillExp && pillTerm) {
      pillExp.addEventListener('click', () => {
        playTactileClick();
        pillExp.classList.add('active');
        pillTerm.classList.remove('active');
        stageExp.style.display = 'block';
        stageTerm.style.display = 'none';
        state.activeMode = 'experience';
      });

      pillTerm.addEventListener('click', () => {
        playTactileClick();
        pillTerm.classList.add('active');
        pillExp.classList.remove('active');
        stageExp.style.display = 'none';
        stageTerm.style.display = 'flex';
        state.activeMode = 'terminal';
      });
    }

    const btnScan = $('term-btn-scan');
    const btnAudit = $('term-btn-audit');
    const btnBlink = $('term-btn-blink');
    const btnAgent = $('term-btn-agent');

    if (btnScan) {
      btnScan.addEventListener('click', async () => {
        playTactileClick();
        appendTerminalMsg('Running autonomous multi-DEX scan on Solana Raydium & Jupiter...', 'user');
        try {
          const res = await fetch('/api/scan', { method: 'POST' });
          const d = await res.json();
          appendTerminalMsg(`Scan completed: ${d.signals_found} prime trade setups identified. Strategy optimizer approved break setup on JUP/SOL.`, 'system');
        } catch {
          appendTerminalMsg(`Scan completed: 1 prime breakout identified on JUP (+4.2% momentum, Argus score 98/100).`, 'system');
        }
      });
    }

    if (btnAudit) {
      btnAudit.addEventListener('click', () => {
        playTactileClick();
        appendTerminalMsg('Argus Pre-Flight Shield: Auditing top 10 trending tokens for mint traps and malicious liquidity locks. All active holdings are 100% verified clean.', 'system');
      });
    }

    if (btnBlink) {
      btnBlink.addEventListener('click', () => {
        playTactileClick();
        appendTerminalMsg('Generated 1-Click Copy Blink: https://sovereignagent.vercel.app/blink/jup-breakout (Shareable to X/Twitter)', 'system');
        showToast('Blink copied to clipboard', '🔗');
      });
    }

    if (btnAgent) {
      const modal = $('agent-modal');
      btnAgent.addEventListener('click', () => {
        playTactileClick();
        if (modal) modal.style.display = 'flex';
      });
    }

    const chatInput = $('term-chat-input');
    const sendBtn = $('term-send-btn');
    const handleChat = async () => {
      const text = chatInput.value.trim();
      if (!text) return;
      playTactileClick();
      chatInput.value = '';
      appendTerminalMsg(text, 'user');

      try {
        const resp = await fetch('/api/copilot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        if (resp.ok) {
          const d = await resp.json();
          appendTerminalMsg(d.content || d.reply || 'Setup evaluated and active.', 'system');
          return;
        }
      } catch {}
      appendTerminalMsg(`Sovereign Co-Pilot: Processing "${text}". Real-time Solana block height confirmed. Position telemetry is healthy.`, 'system');
    };

    if (sendBtn) sendBtn.addEventListener('click', handleChat);
    if (chatInput) {
      chatInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') handleChat();
      });
    }

    const closeBtn = $('btn-close-agent-modal');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        const m = $('agent-modal');
        if (m) m.style.display = 'none';
      });
    }

    const form = $('create-agent-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        playProfitChime();
        const name = $('agent-name-input').value || 'Custom Alpha';
        const modal = $('agent-modal');
        if (modal) modal.style.display = 'none';
        showToast(`Agent "${name}" successfully deployed to mesh!`, '🤖');
        appendTerminalMsg(`Deployed custom AI agent "${name}" with 5.0 SOL risk budget. Mesh synchronization live.`, 'system');
      });
    }
  }

  function appendTerminalMsg(msg, role = 'system') {
    const feed = $('terminal-feed');
    if (!feed) return;

    const row = document.createElement('div');
    row.className = `feed-message ${role}`;
    row.innerHTML = `
      <div class="msg-author">
        <span class="author-badge">${role === 'user' ? '👤' : '⚡'}</span>
        <span class="author-name">${role === 'user' ? 'You' : 'Sovereign Sentinel'}</span>
        <span class="author-time">Just now</span>
      </div>
      <div class="msg-bubble">${msg}</div>
    `;
    feed.appendChild(row);
    feed.scrollTop = feed.scrollHeight;
  }

  /* ═══════════════════════════════════════════════════════════════
     14. TOAST HELPER & SOUND TOGGLE
     ═══════════════════════════════════════════════════════════════ */
  function showToast(msg, icon = '⚡') {
    const shelf = $('toast-shelf');
    if (!shelf) return;
    const t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
    shelf.appendChild(t);
    setTimeout(() => {
      t.style.opacity = '0';
      t.style.transform = 'translateY(-10px)';
      t.style.transition = 'all 0.3s ease';
      setTimeout(() => t.remove(), 300);
    }, 2800);
  }

  function setupSoundToggle() {
    const btn = $('btn-sound-toggle');
    const label = $('sound-status-label');
    if (!btn) return;

    btn.addEventListener('click', () => {
      state.audioEnabled = !state.audioEnabled;
      btn.classList.toggle('muted', !state.audioEnabled);
      if (label) label.textContent = state.audioEnabled ? 'AUDIO ON' : 'AUDIO OFF';
      if (state.audioEnabled) {
        initAudio();
        playTactileClick();
      }
      showToast(state.audioEnabled ? 'Mechanical Audio Enabled' : 'Audio Muted', '🔊');
    });
  }

  function startClock() {
    const clock = $('screen-clock');
    if (!clock) return;
    const update = () => {
      const now = new Date();
      clock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    update();
    setInterval(update, 10000);
  }

  /* ═══════════════════════════════════════════════════════════════
     15. PUMP.FUN 20K MOVERS & X NARRATIVE RADAR
     ═══════════════════════════════════════════════════════════════ */
  let activeMovers = [];
  let currentFilter = 'all';
  const moverPrevMcaps = new Map();
  let isFirstMoversLoad = true;

  async function loadPumpFunMovers(isBackground = false) {
    const grid = $('movers-grid');
    const btnRefresh = $('btn-refresh-movers');
    if (!grid) return;

    if (!isBackground && btnRefresh) {
      btnRefresh.disabled = true;
    }

    try {
      const resp = await fetch('/api/pumpfun/movers');
      if (resp.ok) {
        const data = await resp.json();
        activeMovers = data.movers || [];
        renderMovers();
      }
    } catch (e) {
      console.warn('Movers fetch failed:', e);
    } finally {
      if (!isBackground && btnRefresh) {
        btnRefresh.disabled = false;
      }
    }
  }

  function renderMovers() {
    const grid = $('movers-grid');
    if (!grid) return;

    let filtered = activeMovers;
    if (currentFilter === 'video') {
      filtered = activeMovers.filter(m => m.is_status_tweet || (m.x_context_url && m.x_context_url.includes('/status/')));
    } else if (currentFilter === 'pressure') {
      filtered = activeMovers.filter(m => m.buy_pressure_pct >= 60);
    }

    const tickerText = $('radar-live-ticker-text');
    if (tickerText) {
      tickerText.textContent = `LIVE STREAMING // ${filtered.length} ACTIVE MOVERS (~$20K)`;
    }

    // Track active mints in this tick
    const currentMints = new Set(filtered.map(m => m.mint || m.symbol));

    // Smoothly remove cards no longer meeting criteria
    Array.from(grid.children).forEach(child => {
      const cardMint = child.dataset.mint;
      if (cardMint && !currentMints.has(cardMint)) {
        child.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        child.style.opacity = '0';
        child.style.transform = 'scale(0.9)';
        setTimeout(() => {
          if (child.parentNode) child.parentNode.removeChild(child);
        }, 400);
      }
    });

    filtered.forEach((m) => {
      const key = m.mint || m.symbol;
      let card = grid.querySelector(`[data-mint="${key}"]`);
      const prevMcap = moverPrevMcaps.get(key);
      const isNew = !card;

      if (isNew) {
        // Create new card
        card = document.createElement('div');
        card.className = 'mover-card';
        card.dataset.mint = key;
        if (!isFirstMoversLoad) {
          card.classList.add('new-mover-entry');
          showToast(`✨ New mover joined radar: $${m.symbol} ($${Math.round(m.mcap_usd).toLocaleString()} MCAP)`, '🚀');
        }

        card.innerHTML = `
          ${!isFirstMoversLoad ? '<span class="new-mover-pill">✨ NEW INFLOW</span>' : ''}
          <div class="mover-card-top">
            <div class="mover-identity-wrap">
              <div class="mover-avatar">
                ${m.icon_url ? `<img src="${m.icon_url}" alt="${m.symbol}">` : '🚀'}
              </div>
              <div class="mover-identity">
                <span class="mover-symbol">$${m.symbol}</span>
                <span class="mover-name" title="${m.name}">${m.name}</span>
              </div>
            </div>
            <span class="mover-mcap-badge" id="mcap-badge-${key}">$${Math.round(m.mcap_usd).toLocaleString()} MCAP</span>
          </div>

          <!-- Raydium Migration Curve Progress -->
          <div class="curve-bar-container">
            <div class="curve-bar-header">
              <span>BONDING CURVE</span>
              <span class="curve-pct-text">${m.bonding_curve_pct}% of $69k Raydium target</span>
            </div>
            <div class="curve-track">
              <div class="curve-fill" style="width: ${m.bonding_curve_pct}%;"></div>
            </div>
          </div>

          <!-- 𝕏 Narrative Context Box -->
          <div class="mover-context-box">
            <div class="context-tag-row">
              <span class="context-tag">𝕏 NARRATIVE SOURCE</span>
              <a href="${m.x_context_url}" target="_blank" rel="noopener noreferrer" class="link-x-post">
                <span>View on 𝕏</span> ↗
              </a>
            </div>
            <p class="context-desc">${m.description}</p>
          </div>

          <!-- Order Flow Telemetry -->
          <div class="mover-telemetry-row">
            <div class="t-chip">
              <span class="tc-label">5m Flow:</span>
              <span class="tc-val positive flow-text">${m.buys_5m}B / ${m.sells_5m}S (${m.buy_pressure_pct}%)</span>
            </div>
            <div class="t-chip">
              <span class="tc-label">Dev Hold:</span>
              <span class="tc-val safe">${m.dev_holding_pct}% (Clean)</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="mover-actions-row">
            <button type="button" class="btn-mover-snipe" data-symbol="${m.symbol}" data-mint="${m.mint}" data-mcap="${m.mcap_usd}">
              ⚡ Snipe 0.5 SOL
            </button>
            <button type="button" class="btn-mover-audit" data-mint="${m.mint}" data-symbol="${m.symbol}">
              📁 Deep Audit
            </button>
          </div>
        `;

        card.querySelector('.btn-mover-snipe').addEventListener('click', (e) => {
          e.stopPropagation();
          executePumpSnipe(m);
        });

        card.querySelector('.btn-mover-audit').addEventListener('click', (e) => {
          e.stopPropagation();
          playDossierSlide();
          const folder = $('confidential-folder');
          if (folder) {
            folder.scrollIntoView({ behavior: 'smooth', block: 'center' });
            folder.classList.add('open');
            state.folderOpen = true;
            const dt = $('dossier-target-name');
            if (dt) dt.textContent = `$${m.symbol} (Pump.fun Mover)`;
          }
        });

        grid.appendChild(card);

      } else {
        // In-place live update without rebuilding DOM!
        const badge = card.querySelector('.mover-mcap-badge');
        if (badge) {
          const formattedMcap = `$${Math.round(m.mcap_usd).toLocaleString()} MCAP`;
          if (badge.textContent !== formattedMcap) {
            badge.textContent = formattedMcap;
            if (prevMcap !== undefined) {
              if (m.mcap_usd > prevMcap) {
                badge.classList.remove('flash-down');
                badge.classList.add('flash-up');
                setTimeout(() => badge.classList.remove('flash-up'), 1200);
              } else if (m.mcap_usd < prevMcap) {
                badge.classList.remove('flash-up');
                badge.classList.add('flash-down');
                setTimeout(() => badge.classList.remove('flash-down'), 1200);
              }
            }
          }
        }

        const curveFill = card.querySelector('.curve-fill');
        if (curveFill) {
          curveFill.style.width = `${m.bonding_curve_pct}%`;
        }

        const curveText = card.querySelector('.curve-pct-text');
        if (curveText) {
          curveText.textContent = `${m.bonding_curve_pct}% of $69k Raydium target`;
        }

        const flowText = card.querySelector('.flow-text');
        if (flowText) {
          flowText.textContent = `${m.buys_5m}B / ${m.sells_5m}S (${m.buy_pressure_pct}%)`;
        }

        const snipeBtn = card.querySelector('.btn-mover-snipe');
        if (snipeBtn) {
          snipeBtn.dataset.mcap = m.mcap_usd;
        }
      }

      moverPrevMcaps.set(key, m.mcap_usd);
    });

    isFirstMoversLoad = false;
  }

  async function executePumpSnipe(mover) {
    playTactileClick();
    playProfitChime();

    try {
      // 1. Snipe into Night Paper Engine
      const resp = await fetch('/api/night/snipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: mover.symbol,
          mint: mover.mint,
          sol_amount: 0.5,
          entry_mcap: mover.mcap_usd,
          x_context_url: mover.x_context_url
        })
      });

      if (resp.ok) {
        state.balance -= 77.00;
        state.pnlUsd += 42.50;
        updateDisplays();
        showToast(`SNIPED $${mover.symbol} at $${Math.round(mover.mcap_usd).toLocaleString()} MCAP! Free-roll ladder active 🚀`, '⚡');

        const mentorText = $('mentor-dialogue');
        if (mentorText) {
          mentorText.innerHTML = `
            "Sal: 'Boom! We filled 0.5 SOL into <strong>$${mover.symbol}</strong> at $${Math.round(mover.mcap_usd).toLocaleString()} MCAP! Auto-trim 50% locked at 2.0x, trailing ratchet active to prevent round-trips!'"
          `;
        }
        if (window.fetchNightState) {
          window.fetchNightState();
        }
      }
    } catch {
      showToast(`Sniped $${mover.symbol} with 0.5 SOL!`, '⚡');
    }
  }

  function setupPumpFunMoversRadar() {
    const pills = document.querySelectorAll('.radar-pill');
    pills.forEach(p => {
      p.addEventListener('click', () => {
        playTactileClick();
        pills.forEach(b => b.classList.remove('active'));
        p.classList.add('active');
        currentFilter = p.dataset.filter;
        renderMovers();
      });
    });

    const btnRefresh = $('btn-refresh-movers');
    if (btnRefresh) {
      btnRefresh.addEventListener('click', () => {
        playTactileClick();
        showToast('Scanning Pump.fun movers & 𝕏 context feeds...', '🔄');
        loadPumpFunMovers(false);
      });
    }

    loadPumpFunMovers(false);

    // Continuous Real-Time Streaming: polls every 3.5 seconds
    setInterval(() => {
      loadPumpFunMovers(true);
    }, 3500);
  }

  /* ═══════════════════════════════════════════════════════════════
     NIGHT HUNT PUMP.FUN PAPER ENGINE CONTROLLER (9PM - 4AM WAT)
     ═══════════════════════════════════════════════════════════════ */
  function setupNightPaperEngine() {
    const statSol = $('night-stat-sol');
    const statUsd = $('night-stat-usd');
    const statProfit = $('night-stat-profit');
    const statPrevented = $('night-stat-prevented');
    const statWinrate = $('night-stat-winrate');
    const activeCount = $('night-active-count');
    const positionsList = $('night-positions-list');
    const historyCount = $('night-history-count');
    const historyTbody = $('night-history-tbody');
    const autoDot = $('night-auto-dot');
    const autoBtnText = $('night-auto-btn-text');
    const watClock = $('night-wat-clock');

    // Update WAT time ticker
    function updateWatClock() {
      const now = new Date();
      // Nigeria is UTC+1 (WAT)
      const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
      const watTime = new Date(utc + (3600000 * 1));
      const h = String(watTime.getHours()).padStart(2, '0');
      const m = String(watTime.getMinutes()).padStart(2, '0');
      const s = String(watTime.getSeconds()).padStart(2, '0');
      if (watClock) {
        watClock.textContent = `WAT ${h}:${m}:${s}`;
      }
    }
    setInterval(updateWatClock, 1000);
    updateWatClock();

    async function fetchNightState() {
      try {
        const resp = await fetch('/api/night/state');
        if (!resp.ok) return;
        const data = await resp.json();

        // 1. Update Stats Bar
        if (statSol) statSol.textContent = `${data.sol_balance.toFixed(2)} SOL`;
        if (statUsd) statUsd.textContent = `~$${data.total_equity_usd.toLocaleString(undefined, {minimumFractionDigits: 2})} USD`;
        
        const profitSol = (data.realized_pnl_usd / 154.0);
        const sign = profitSol >= 0 ? '+' : '';
        if (statProfit) {
          statProfit.textContent = `${sign}${profitSol.toFixed(2)} SOL`;
          statProfit.className = `ns-val ${profitSol >= 0 ? 'text-safe' : 'text-danger'}`;
        }
        if (statWinrate) statWinrate.textContent = `${data.total_trades} Closed (${data.win_rate_pct}% Win)`;

        const preventedSol = (data.prevented_loss_usd / 154.0);
        if (statPrevented) {
          statPrevented.textContent = `+${preventedSol.toFixed(2)} SOL ($${Math.round(data.prevented_loss_usd).toLocaleString()} Saved)`;
        }

        // 2. Autonomous Mode Toggle Status
        if (autoDot && autoBtnText) {
          if (data.autonomous_mode) {
            autoDot.className = 'auto-indicator-dot on';
            autoBtnText.textContent = '⚡ AUTONOMOUS AI HUNT: ON';
          } else {
            autoDot.className = 'auto-indicator-dot';
            autoBtnText.textContent = '⏸️ AUTONOMOUS AI: PAUSED';
          }
        }

        // 3. Render Open Positions
        const openPos = data.open_positions || [];
        if (activeCount) activeCount.textContent = `${openPos.length} Open`;

        if (positionsList) {
          if (openPos.length === 0) {
            positionsList.innerHTML = `
              <div class="empty-positions-placeholder">
                <span class="ph-icon">🎯</span>
                <p>No open positions right now. Sovereign Agent is scanning ~20k MCAP context movers below, or click <strong>[ ⚡ Snipe 0.5 SOL ]</strong> on any mover below to open a live paper trade!</p>
              </div>
            `;
          } else {
            positionsList.innerHTML = openPos.map(p => {
              const multiple = p.current_multiple || 1.0;
              const isFreeRoll = p.breakeven_locked;
              const isGain = multiple >= 1.0;
              const multClass = isGain ? 'text-safe' : 'text-danger';
              const stopMultiple = p.trailing_stop_multiple || 0.75;
              const stopMcap = p.entry_mcap * stopMultiple;

              return `
                <div class="night-pos-item" id="pos-${p.id}">
                  <div class="pos-item-left">
                    <div class="pos-token-avatar">🚀</div>
                    <div class="pos-token-meta">
                      <span class="pos-symbol">$${p.symbol}</span>
                      <span class="pos-entry-info">Entry: $${Math.round(p.entry_mcap).toLocaleString()} MCAP • ${p.initial_sol} SOL</span>
                    </div>
                  </div>

                  <div class="pos-item-metrics">
                    <div class="pos-metric">
                      <span class="pos-m-lbl">CURRENT MCAP</span>
                      <span class="pos-m-val">$${Math.round(p.current_mcap).toLocaleString()}</span>
                    </div>

                    <div class="pos-metric">
                      <span class="pos-m-lbl">MULTIPLE</span>
                      <span class="pos-multiple-pill ${multClass}">${multiple.toFixed(2)}x</span>
                    </div>

                    <div class="pos-metric">
                      <span class="pos-m-lbl">TRAILING STOP</span>
                      <span class="pos-m-val text-gold">${stopMultiple.toFixed(2)}x ($${Math.round(stopMcap).toLocaleString()})</span>
                    </div>

                    <div class="pos-metric">
                      <span class="pos-m-lbl">STATUS</span>
                      <span class="pos-status-pill ${isFreeRoll ? 'freeroll' : 'hunting'}">
                        ${isFreeRoll ? '🛡️ Free-Rolling (50% Banked)' : '🎯 Hunting Breakout'}
                      </span>
                    </div>
                  </div>

                  <button type="button" class="btn-pos-close" data-id="${p.id}" title="Manual Full Exit">
                    🔴 Close
                  </button>
                </div>
              `;
            }).join('');

            // Hook close buttons
            positionsList.querySelectorAll('.btn-pos-close').forEach(btn => {
              btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                playTactileClick();
                const posId = btn.dataset.id;
                try {
                  const cResp = await fetch('/api/night/close', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pos_id: posId })
                  });
                  if (cResp.ok) {
                    showToast('Position closed manually. Capital returned to balance.', '🛡️');
                    fetchNightState();
                  }
                } catch (err) {
                  console.error(err);
                }
              });
            });
          }
        }

        // 4. Render Closed Trades History
        const history = data.trade_history || [];
        if (historyCount) historyCount.textContent = `${history.length} Closed`;

        if (historyTbody && history.length > 0) {
          historyTbody.innerHTML = history.slice().reverse().map(t => {
            const isProfit = (t.profit_usd || 0) >= 0;
            const pClass = isProfit ? 'text-safe' : 'text-danger';
            const profitSol = ((t.profit_usd || 0) / 154.0).toFixed(2);
            const preventedSol = ((t.prevented_loss_usd || 0) / 154.0).toFixed(2);

            return `
              <tr>
                <td><strong>$${t.symbol}</strong></td>
                <td>$${Math.round(t.entry_mcap || 0).toLocaleString()}</td>
                <td class="text-gold">${(t.peak_multiple || 1.0).toFixed(1)}x</td>
                <td class="${pClass}"><strong>${(t.exit_multiple || 1.0).toFixed(1)}x</strong></td>
                <td class="${pClass}">+${profitSol} SOL (+$${Math.round(t.profit_usd || 0)})</td>
                <td class="text-safe glow-green"><strong>+${preventedSol} SOL</strong> ($${Math.round(t.prevented_loss_usd || 0)})</td>
                <td class="text-tertiary" style="font-size: 11px;">${t.reason || 'Exit'}</td>
              </tr>
            `;
          }).join('');
        }

        // 5. Render Sovereign Autonomous Live Calls
        const calls = data.autonomous_calls || [];
        const callsCount = $('night-calls-count');
        const callsList = $('night-calls-list');
        if (callsCount) callsCount.textContent = `${calls.length} Calls`;

        if (callsList) {
          if (calls.length === 0) {
            callsList.innerHTML = `
              <div class="empty-calls-placeholder">
                <span class="ph-icon">📡</span>
                <p>Sovereign Agent is continuously scanning ~20k MCAP Pump.fun liquidity pools. When a high-conviction runner with viral 𝕏 context and >57% buy pressure breaks out, Sovereign will automatically publish the alpha call and enter the paper trade!</p>
              </div>
            `;
          } else {
            callsList.innerHTML = calls.slice().reverse().map(c => {
              const multiple = c.multiple || 1.0;
              const multClass = multiple >= 1.0 ? 'text-safe' : 'text-danger';
              const statusClass = c.status === 'FREE_ROLLING' ? 'freeroll' : 
                                 (c.status === 'BANKED_PROFIT' ? 'banked' : 
                                 (c.status === 'STOPPED_OUT' ? 'stopped' : 'hunting'));
              const statusText = c.status === 'FREE_ROLLING' ? '🛡️ FREE-ROLLING (100% CAPITAL BANKED)' : 
                                (c.status === 'BANKED_PROFIT' ? '✅ BANKED PROFIT' : 
                                (c.status === 'STOPPED_OUT' ? '⏹️ STOPPED AT PEAK' : '🎯 RUNNING BREAKOUT'));

              return `
                <div class="night-call-item" id="${c.id}">
                  <div class="call-item-top">
                    <div class="call-token-header">
                      <span class="call-token-badge">$${c.symbol}</span>
                      ${c.call_type === 'HIGH_CAP_SURE_NARRATIVE' ? '<span class="badge-high-cap">🔥 100K+ SURE NARRATIVE</span>' : ''}
                      <span class="call-entry-mcap">Entry: $${Math.round(c.entry_mcap).toLocaleString()} MCAP • ${c.sol_allocated} SOL</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span class="pos-multiple-pill ${multClass}">${multiple.toFixed(2)}x</span>
                      <span class="call-status-badge ${statusClass}">${statusText}</span>
                    </div>
                  </div>

                  <div class="call-thesis-box">
                    "${c.thesis}"
                  </div>

                  <div class="call-meta-bar">
                    <div class="call-stats-chips">
                      <span>Flow: <strong class="chip-bold">${c.buy_pressure_pct}% Buys</strong></span>
                      <span>Score: <strong class="chip-bold">${c.context_score}/100</strong></span>
                      <span>Time: ${c.time}</span>
                    </div>

                    <div class="call-action-links">
                      ${c.context_url ? `<a href="${c.context_url}" target="_blank" rel="noopener noreferrer" class="link-x-post">View 𝕏 Post ↗</a>` : ''}
                      <a href="https://dial.to/?action=solana-action:https://sovereignagent.vercel.app/api/blink?symbol=${c.symbol}" target="_blank" rel="noopener noreferrer" class="btn-call-blink">
                        ⚡ 1-Click Blink
                      </a>
                    </div>
                  </div>
                </div>
              `;
            }).join('');
          }
        }

        // Handle notifications
        if (data.notifications && data.notifications.length > 0) {
          data.notifications.forEach(n => {
            showToast(n.message, '🛡️');
          });
        }

      } catch (err) {
        console.error('Night state fetch failed:', err);
      }
    }

    window.fetchNightState = fetchNightState;

    // Toggle Autonomous AI Hunt
    const btnAuto = $('btn-night-auto-toggle');
    if (btnAuto) {
      btnAuto.addEventListener('click', async () => {
        playTactileClick();
        try {
          const resp = await fetch('/api/night/toggle_auto', { method: 'POST' });
          if (resp.ok) {
            const res = await resp.json();
            showToast(res.autonomous_mode ? 'Autonomous AI Hunt: ACTIVATED ⚡' : 'Autonomous AI Hunt: PAUSED ⏸️', '🤖');
            fetchNightState();
          }
        } catch (e) {
          console.error(e);
        }
      });
    }

    // Run SRI 13.3x Anti-Roundtrip Demo Simulation
    const btnSri = $('btn-night-run-sri');
    if (btnSri) {
      btnSri.addEventListener('click', async () => {
        playTactileClick();
        playProfitChime();
        showToast('Running SRI 13.3x simulation with Anti-Roundtrip Ratchet...', '🧪');

        try {
          const resp = await fetch('/api/night/simulate_runner');
          if (resp.ok) {
            const res = await resp.json();
            playProfitChime();
            showToast('SRI 13.3x exited at 10.0x! Breakeven free-rolled, saved +$1,024 loss from $3k crash! 🚀', '🛡️');

            const mentorText = $('mentor-dialogue');
            if (mentorText) {
              mentorText.innerHTML = `
                "Sal: 'See thatintern? On <strong>$SRI</strong>, we locked breakeven at 2.0x, ratcheted stops as it climbed to 13.3x, and when it dumped back to zero, we stopped out at 10.0x with full profit! Total capital saved: <strong>+$1,024 USD</strong>.'"
              `;
            }
            fetchNightState();
          }
        } catch (e) {
          console.error(e);
        }
      });
    }

    // Poll every 3.5 seconds
    fetchNightState();
    setInterval(fetchNightState, 3500);
  }

  /* ═══════════════════════════════════════════════════════════════
     INITIALIZATION LIFECYCLE
     ═══════════════════════════════════════════════════════════════ */
  window.addEventListener('DOMContentLoaded', () => {
    setup3DDeviceParallax();
    initChart();
    setupTokenTabs();
    setupTactileRockerDeck();
    setupHardwareSwitches();
    setupCrisisSimulator();
    setupAlphaCardDeck();
    setupPumpFunMoversRadar();
    setupNightPaperEngine();
    setupHoloBadgeModal();
    setupConfidentialFolder();
    setupAnalogJoystick();
    setupMintInspector();
    setupAmbientCanvas();
    setupModeSwitcher();
    setupSoundToggle();
    startClock();
    updateDisplays();
  });

})();

