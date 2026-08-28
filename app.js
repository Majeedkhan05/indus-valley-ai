/* =========================================================
   INDUS VALLEY AI — interactions (v2)
   - Custom cursor + spotlight
   - Scroll progress + reveal + scroll-spine
   - Magnetic hover on key controls
   - Mobile nav, modal
   - Seal / city / motif rendering
   - AI chat:
     · domain-locked KB matching
     · Gemini Nano on-device enrichment (free, no API)
     · file/image upload + vision heuristics
     · learning paths (sequential KB walkthroughs)
     · (video-gen feature removed per scope)
   ========================================================= */

(() => {

  /* ──────────────────────────────────────────────
     CUSTOM CURSOR + SPOTLIGHT
     ────────────────────────────────────────────── */
  const cursor = document.querySelector('.cursor');
  const cursorDot = document.querySelector('.cursor-dot');
  const cursorRing = document.querySelector('.cursor-ring');
  const spotlight = document.querySelector('.spotlight');

  let mx = window.innerWidth / 2, my = window.innerHeight / 2;
  let rx = mx, ry = my;                          // ring lerps; dot is instant
  let spotlightFrameSkip = false;                // spotlight throttle
  const isCoarse = window.matchMedia('(pointer: coarse)').matches;
  if (isCoarse && cursor) cursor.style.display = 'none';

  // pointer tracker — only stores coords, does no DOM writes
  window.addEventListener('pointermove', e => {
    mx = e.clientX; my = e.clientY;
  }, { passive: true });

  // single rAF loop drives EVERYTHING — dot follows instantly, ring lerps,
  // spotlight CSS-vars updated on alternating frames (30fps is enough)
  function cursorTick() {
    // dot: instant follow, no lerp — feels responsive
    if (cursorDot) cursorDot.style.transform = `translate3d(${mx}px,${my}px,0)`;

    // ring: snappy lerp (0.22 — much faster than the old 0.12)
    rx += (mx - rx) * 0.22;
    ry += (my - ry) * 0.22;
    if (cursorRing) cursorRing.style.transform = `translate3d(${rx}px,${ry}px,0)`;

    // spotlight: throttled to every other frame
    if (spotlight && !spotlightFrameSkip) {
      spotlight.style.setProperty('--mx', mx + 'px');
      spotlight.style.setProperty('--my', my + 'px');
    }
    spotlightFrameSkip = !spotlightFrameSkip;

    requestAnimationFrame(cursorTick);
  }
  if (!isCoarse) requestAnimationFrame(cursorTick);

  document.querySelectorAll('a, button, .seal-card, .city-card, .motif-card').forEach(el => {
    el.addEventListener('pointerenter', () => cursor && cursor.classList.add('cursor-hover'));
    el.addEventListener('pointerleave', () => cursor && cursor.classList.remove('cursor-hover'));
  });

  /* ──────────────────────────────────────────────
     MAGNETIC HOVER (rAF-throttled, GPU-composited)
     ────────────────────────────────────────────── */
  document.querySelectorAll('.btn-primary, .chat-send, .chat-attach-btn').forEach(el => {
    let pending = null;
    let scheduled = false;
    el.style.willChange = 'transform';
    const apply = () => {
      scheduled = false;
      if (!pending) return;
      el.style.transform = `translate3d(${pending.x}px,${pending.y}px,0)`;
    };
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect();
      pending = { x: (e.clientX - r.left - r.width / 2) * 0.22,
                  y: (e.clientY - r.top  - r.height / 2) * 0.22 };
      if (!scheduled) { scheduled = true; requestAnimationFrame(apply); }
    }, { passive: true });
    el.addEventListener('pointerleave', () => {
      pending = null;
      el.style.transform = '';
    });
  });

  /* ──────────────────────────────────────────────
     SCROLL PROGRESS + SPINE + REVEAL
     ────────────────────────────────────────────── */
  const progress = document.getElementById('progress');
  const spineFill = document.querySelector('.spine-fill');
  const spineNodes = document.querySelectorAll('.spine-nodes li');
  const sectionMap = {
    hero: document.querySelector('.hero'),
    about: document.querySelector('#about'),
    chat: document.querySelector('#chat'),
    pillars: document.querySelector('.pillars'),
    seals: document.querySelector('#seals'),
    cities: document.querySelector('#cities'),
    routes: document.querySelector('#routes'),
    motifs: document.querySelector('#motifs'),
    script: document.querySelector('#script'),
    analysis: document.querySelector('#analysis'),
    research: document.querySelector('#research')
  };

  document.querySelectorAll('section:not(.hero):not(.ticker), .seal-grid, .city-grid, .motif-grid, .pillars-grid, .research-list, .india-grid, .trade-grid, .script-grid, .time-list, .about-points').forEach(el => {
    el.classList.add('reveal');
  });
  const ro = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        ro.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => ro.observe(el));

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    requestAnimationFrame(() => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = Math.max(0, Math.min(1, window.scrollY / max));
      if (progress) progress.style.width = (pct * 100) + '%';
      if (spineFill) spineFill.style.transform = `scaleY(${pct})`;

      // active spine node — closest to center of viewport
      let activeKey = null;
      let closest = Infinity;
      const center = window.scrollY + window.innerHeight / 2;
      for (const [k, el] of Object.entries(sectionMap)) {
        if (!el) continue;
        const top = el.offsetTop;
        const mid = top + el.offsetHeight / 2;
        const d = Math.abs(mid - center);
        if (d < closest) { closest = d; activeKey = k; }
      }
      spineNodes.forEach(n => n.classList.toggle('active', n.dataset.spine === activeKey));
      ticking = false;
    });
    ticking = true;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // spine click → scroll to section
  spineNodes.forEach(n => {
    n.addEventListener('click', () => {
      const el = sectionMap[n.dataset.spine];
      if (el) window.scrollTo({ top: el.offsetTop - 60, behavior: 'smooth' });
    });
  });

  /* ──────────────────────────────────────────────
     MOBILE NAV + MODAL
     ────────────────────────────────────────────── */
  const burger = document.querySelector('[data-nav-toggle]');
  const navLinks = document.querySelector('.nav-links');
  if (burger && navLinks) {
    burger.addEventListener('click', () => navLinks.classList.toggle('open'));
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));
  }

  const modal = document.getElementById('modal');
  const modalBody = modal.querySelector('[data-modal-body]');
  function openModal(html) {
    modalBody.innerHTML = html;
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeModal() {
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  modal.querySelectorAll('[data-modal-close]').forEach(el => el.addEventListener('click', closeModal));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') closeModal();
  });

  /* ──────────────────────────────────────────────
     RENDER: seals / cities / motifs / script
     ────────────────────────────────────────────── */
  const sealGrid = document.querySelector('[data-seal-grid]');
  if (sealGrid && window.IVA_DATA) {
    sealGrid.innerHTML = IVA_DATA.seals.map(s => `
      <article class="seal-card" data-seal="${s.id}">
        <img src="${s.file}" alt="Indus seal — ${s.label}" loading="lazy" />
        <div class="seal-card-meta">
          <strong>${s.label}</strong>
          <span>#${s.id}</span>
        </div>
      </article>
    `).join('');
    sealGrid.querySelectorAll('.seal-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = parseInt(card.dataset.seal, 10);
        const seal = IVA_DATA.seals.find(s => s.id === id);
        if (!seal) return;
        openModal(`
          <p class="m-meta">Seal · #${seal.id} · ${seal.tag}</p>
          <h3>${seal.label}</h3>
          <img src="${seal.file}" alt="Seal #${seal.id}" />
          <p>This seal — like most of the Indus corpus — pairs an animal motif with a short line of script (5–6 signs on average). Steatite (soapstone) was kiln-fired to harden it before carving.</p>
          <p>The seal is best read as an <em>administrative or personal monogram</em> — a stamp pressed into clay to mark goods, sealings, or trade documents. The animal motif likely identifies a clan, guild, or office; the script identifies a specific person, role, or commodity.</p>
          <ul class="m-list">
            <li>Catalog ID: ${seal.id}</li>
            <li>Type: ${seal.tag}</li>
            <li>Likely use: administrative seal / trade marker</li>
            <li>Material context: steatite (soapstone), fired</li>
          </ul>
          <p>Want a deeper read? <a href="#chat" class="btn btn-pill" onclick="document.getElementById('modal').setAttribute('aria-hidden','true');document.body.style.overflow='';">Ask the AI →</a></p>
        `);
      });
    });
  }

  const cityGrid = document.querySelector('[data-city-grid]');
  if (cityGrid && window.IVA_DATA) {
    cityGrid.innerHTML = IVA_DATA.cities.map(c => `
      <article class="city-card" data-city="${c.name}">
        <h4>${c.name}</h4>
        <p class="c-loc">${c.loc}</p>
        <p>${c.summary}</p>
        <div class="c-stats">${c.stats.map(s => `<span class="c-chip">${s}</span>`).join('')}</div>
      </article>
    `).join('');
    cityGrid.querySelectorAll('.city-card').forEach(card => {
      card.addEventListener('click', () => {
        const name = card.dataset.city;
        const c = IVA_DATA.cities.find(x => x.name === name);
        if (!c) return;
        openModal(`
          <p class="m-meta">City · ${c.loc}</p>
          <h3>${c.name}</h3>
          <p>${c.summary}</p>
          <ul class="m-list">${c.detail.map(d => `<li>${d}</li>`).join('')}</ul>
          <a href="#chat" class="btn btn-pill m-cta" onclick="document.getElementById('modal').setAttribute('aria-hidden','true');document.body.style.overflow='';">Ask the AI more →</a>
        `);
      });
    });
  }

  const motifGrid = document.querySelector('[data-motif-grid]');
  if (motifGrid && window.IVA_DATA) {
    motifGrid.innerHTML = IVA_DATA.motifs.map(m => `
      <article class="motif-card" data-motif="${m.name}">
        <div class="motif-glyph">${m.glyph}</div>
        <h4>${m.name}</h4>
        <p>${m.summary}</p>
        <p class="motif-freq">Frequency · ${m.freq}</p>
      </article>
    `).join('');
    motifGrid.querySelectorAll('.motif-card').forEach(card => {
      card.addEventListener('click', () => {
        const name = card.dataset.motif;
        const m = IVA_DATA.motifs.find(x => x.name === name);
        if (!m) return;
        openModal(`
          <p class="m-meta">Motif · ${m.freq}</p>
          <h3>${m.name}</h3>
          <p>${m.summary}</p>
          <ul class="m-list">${m.detail.map(d => `<li>${d}</li>`).join('')}</ul>
          <a href="#chat" class="btn btn-pill m-cta" onclick="document.getElementById('modal').setAttribute('aria-hidden','true');document.body.style.overflow='';">Discuss with the AI →</a>
        `);
      });
    });
  }

  const scriptStrip = document.querySelector('[data-script-strip]');
  if (scriptStrip && window.IVA_DATA) {
    scriptStrip.innerHTML = IVA_DATA.scriptGlyphs.map(d => `
      <div class="script-glyph" title="Stylized Indus sign">
        <svg viewBox="0 0 48 48"><path d="${d}"/></svg>
      </div>
    `).join('');
  }

  /* ──────────────────────────────────────────────
     COMPUTATIONAL SCRIPT ANALYSIS
     ────────────────────────────────────────────── */
  if (window.IVA_SCRIPT) {
    const A = window.IVA_SCRIPT;

    // Frequency bars
    const freqHost = document.querySelector('[data-freq-bars]');
    if (freqHost) {
      const max = A.frequency[0].count;
      freqHost.innerHTML = A.frequency.map(f => `
        <div class="a-bar-row" title="${f.note}">
          <span class="a-bar-label">${f.sign}</span>
          <div class="a-bar-track"><div class="a-bar-fill" style="width:0"></div></div>
          <span class="a-bar-num">${f.count}</span>
        </div>
      `).join('');
      // Animate after a frame
      requestAnimationFrame(() => {
        freqHost.querySelectorAll('.a-bar-fill').forEach((el, i) => {
          el.style.width = ((A.frequency[i].count / max) * 100).toFixed(1) + '%';
        });
      });
    }

    // Positional 3-column
    const posHost = document.querySelector('[data-pos-cols]');
    if (posHost) {
      const col = (label, key) => `
        <div class="a-pos-col">
          <h5>${label}</h5>
          ${A.positional[key].map(p => `
            <div class="a-pos-item" title="${p.note}">
              <span>${p.sign.split(' ')[0]}</span>
              <span class="a-pct">${p.pct}%</span>
            </div>
          `).join('')}
        </div>`;
      posHost.innerHTML = col('Initial','initial') + col('Medial','medial') + col('Final','final');
    }

    // Bigrams
    const bigramHost = document.querySelector('[data-bigram-list]');
    if (bigramHost) {
      bigramHost.innerHTML = A.bigrams.map(b => `
        <li title="${b.note}">
          <span class="a-bigram-pair">${b.label}</span>
          <span class="a-bigram-count">${b.count}×</span>
        </li>
      `).join('');
    }

    // Z-scores
    const zHost = document.querySelector('[data-zscore-list]');
    if (zHost) {
      zHost.innerHTML = A.zScores.map(z => `
        <li>
          <span>${z.sign} <em style="color:var(--ink-mute)">· ${z.position}</em></span>
          <span class="a-z-val">Z = ${z.z}</span>
          <span class="a-z-sig">${z.significance}</span>
        </li>
      `).join('');
    }

    // Length distribution
    const lenHost = document.querySelector('[data-len-bars]');
    if (lenHost) {
      const maxLen = Math.max(...A.lengthDistribution.map(l => l.count));
      lenHost.innerHTML = A.lengthDistribution.map(l => `
        <div class="a-len-col" title="Length ${l.length}: ${l.count} inscriptions (${l.pct}%)">
          <div class="a-len-bar" style="height:0"></div>
          <span class="a-len-label">${l.length}</span>
        </div>
      `).join('');
      requestAnimationFrame(() => {
        lenHost.querySelectorAll('.a-len-bar').forEach((el, i) => {
          el.style.height = ((A.lengthDistribution[i].count / maxLen) * 100).toFixed(1) + '%';
        });
      });
    }

    // Conclusions
    const concHost = document.querySelector('[data-conclude-list]');
    if (concHost) {
      concHost.innerHTML = A.conclusions.map(c => `<li>${c}</li>`).join('');
    }
  }

  /* ──────────────────────────────────────────────
     CHAT
     ────────────────────────────────────────────── */
  const chatForm = document.querySelector('[data-chat-form]');
  const chatInput = document.querySelector('[data-chat-input]');
  const chatStream = document.querySelector('[data-chat-stream]');
  const chatQuick = document.querySelector('[data-chat-quick]');
  const chatPaths = document.querySelector('[data-chat-paths]');
  const fileInput = document.querySelector('[data-chat-file]');
  const attachTrigger = document.querySelector('[data-attach-trigger]');
  const attachBox = document.querySelector('[data-chat-attach]');
  const attachThumb = document.querySelector('[data-attach-thumb]');
  const attachName = document.querySelector('[data-attach-name]');
  const attachMeta = document.querySelector('[data-attach-meta]');
  const attachClear = document.querySelector('[data-attach-clear]');
  // const videoBtn = document.querySelector('[data-video-redirect]'); // removed
  const dropZone = document.querySelector('[data-drop-zone]');
  const nanoBadge = document.querySelector('[data-nano-badge]');
  const nanoText = document.querySelector('[data-nano-text]');

  let pendingFile = null;
  let pendingAnalysis = null;
  let pendingObjectUrl = null;
  let lastTopic = null;
  let ragOnline = false;
  const chatHistory = [];   // for the RAG backend's history slot

  /* — RAG backend detection — */
  if (window.IVA_RAG) {
    window.IVA_RAG.ping().then(info => {
      if (info) {
        ragOnline = true;
        if (nanoBadge && nanoText) {
          nanoText.textContent = `RAG · ${info.ollama_model} · ${info.vector_count} chunks`;
          nanoBadge.dataset.state = 'ready';
        }
        console.log('[IVAI] RAG online:', info);
      } else {
        console.log('[IVAI] RAG offline — using KB.');
      }
    });
  }

  /* — Gemini Nano badge — */
  if (window.IVA_NANO && nanoBadge) {
    window.IVA_NANO.detect().then(s => {
      nanoText.textContent = s.text;
      nanoBadge.dataset.state = s.state;
    });
  }

  /* — paths — sequential walkthroughs — */
  const PATHS = {
    seals:   ['Indus seals — what they are and what they do','The "unicorn" motif','How a seal was actually made','The Ernestite drill — Harappan precision'],
    cities:  ['The Indus / Harappan Civilization — overview','Mohenjo-daro vs Harappa vs Dholavira','Dholavira (Gujarat)','Lothal — the Bronze Age port','Rakhigarhi & the 2018 ancient-DNA study'],
    script:  ['The Indus script — current status','The "fish" sign — the most frequent sign in the script','Parpola — the Dravidian decipherment hypothesis','Yajnadevam — the recent computational claim'],
    trade:   ['Indus trade with Mesopotamia','"Meluhha" — what the Mesopotamians called the Indus','Shortugai — the Indus outpost on the Oxus','Sutkagan-Dor — the westernmost outpost','Carnelian beads — a Harappan signature export'],
    decline: ['How the civilization ended','The 4.2-ka event — climate & Indus decline','The Ghaggar-Hakra / Sarasvati river','Chronology — Indus phases & dating']
  };

  if (chatPaths) {
    chatPaths.querySelectorAll('button').forEach(b => {
      b.addEventListener('click', async () => {
        const key = b.dataset.path;
        const titles = PATHS[key];
        if (!titles) return;
        appendUser(`Walk me through: ${b.textContent.trim()}`);
        appendBotTyping();
        await wait(700);
        const removeTyping = () => { const t = chatStream.querySelector('[data-typing]'); if (t) t.remove(); };
        removeTyping();

        appendBot('Learning path · ' + b.textContent.trim(), [
          `I'll walk you through ${titles.length} topics in sequence. Each builds on the last.`
        ], 'Curated path');

        for (let i = 0; i < titles.length; i++) {
          await wait(450);
          const topic = window.IVA_KB.topics.find(x => x.title === titles[i]);
          if (topic) {
            appendBot(`<span class="path-step">${i+1}/${titles.length}</span> · ${topic.title}`, topic.body, topic.sources);
            lastTopic = topic;
            await maybeEnrich(topic.title, topic.body[0]);
          }
        }
      });
    });
  }

  /* — main form — */
  if (chatForm && chatInput && chatStream && window.IVA_KB) {
    chatForm.addEventListener('submit', e => {
      e.preventDefault();
      const q = chatInput.value.trim();
      if (!q && !pendingFile) return;
      handleQuestion(q || (pendingAnalysis ? `Tell me about: ${pendingAnalysis.summary}` : 'Analyze this image'));
      chatInput.value = '';
    });

    if (chatQuick) {
      chatQuick.querySelectorAll('button').forEach(b => {
        b.addEventListener('click', () => handleQuestion(b.dataset.q));
      });
    }
  }

  /* — file upload — */
  if (attachTrigger && fileInput) {
    attachTrigger.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
      const f = fileInput.files && fileInput.files[0];
      if (f) handleFile(f);
      fileInput.value = '';
    });
  }
  if (attachClear) {
    attachClear.addEventListener('click', clearAttachment);
  }

  /* — drag-drop — */
  let dragDepth = 0;
  window.addEventListener('dragenter', e => {
    if (!e.dataTransfer || !e.dataTransfer.types.includes('Files')) return;
    e.preventDefault();
    dragDepth++;
    if (dropZone) dropZone.setAttribute('aria-hidden', 'false');
  });
  window.addEventListener('dragover', e => { if (e.dataTransfer && e.dataTransfer.types.includes('Files')) e.preventDefault(); });
  window.addEventListener('dragleave', () => {
    dragDepth = Math.max(0, dragDepth - 1);
    if (dragDepth === 0 && dropZone) dropZone.setAttribute('aria-hidden', 'true');
  });
  window.addEventListener('drop', e => {
    e.preventDefault();
    dragDepth = 0;
    if (dropZone) dropZone.setAttribute('aria-hidden', 'true');
    const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
    if (f) handleFile(f);
  });

  /* video generation removed per project scope */

  /* — file handling — */
  async function handleFile(file) {
    pendingFile = file;
    if (file.type.startsWith('image/')) {
      try {
        const { img, url } = await window.IVA_VISION.fileToImage(file);
        if (pendingObjectUrl) { URL.revokeObjectURL(pendingObjectUrl); }
        pendingObjectUrl = url;
        attachThumb.style.display = '';   // always reset before showing
        attachThumb.src = url;
        attachName.textContent = file.name;
        attachMeta.textContent = `${(file.size/1024).toFixed(1)} KB · ${img.naturalWidth}×${img.naturalHeight}`;
        attachBox.hidden = false;
        pendingAnalysis = window.IVA_VISION.analyze(img);
      } catch (err) {
        appendBot('Couldn\'t load that image', ['I tried to read the file but the browser couldn\'t decode it. Please try a different image (PNG / JPG / WEBP).'], null);
        clearAttachment();
      }
    } else {
      try {
        const text = await window.IVA_VISION.fileToText(file);
        attachThumb.src = '';
        attachThumb.style.display = 'none';
        attachName.textContent = file.name;
        attachMeta.textContent = `${(file.size/1024).toFixed(1)} KB · text`;
        attachBox.hidden = false;
        pendingAnalysis = { isText: true, text: text.slice(0, 4000), summary: 'a text/script document' };
      } catch (err) {
        appendBot('Couldn\'t read the file', ['Only image, txt, md, json, and csv files are supported.'], null);
        clearAttachment();
      }
    }
  }

  function clearAttachment() {
    pendingFile = null;
    pendingAnalysis = null;
    if (pendingObjectUrl) { URL.revokeObjectURL(pendingObjectUrl); pendingObjectUrl = null; }
    if (attachBox) attachBox.hidden = true;
    if (attachThumb) { attachThumb.src = ''; attachThumb.style.display = ''; }
  }

  /* ──────────────────────────────────────────────
     MESSAGES
     ────────────────────────────────────────────── */
  const BOT_AVATAR_HTML = `
    <div class="msg-avatar logo-wrap">
      <img src="assets/logo.png" alt="" class="logo-img" onerror="this.style.display='none';this.nextElementSibling.style.display='block'" />
      <svg viewBox="0 0 64 64" class="logo-fallback" style="display:none"><rect width="64" height="64" rx="14" fill="#0F0F0F"/><path d="M14 44 V20 L24 36 L34 20 V44" stroke="#D4AF37" stroke-width="3.5" fill="none" stroke-linejoin="round" stroke-linecap="round"/><circle cx="44" cy="32" r="8" stroke="#C2A878" stroke-width="3" fill="none"/><circle cx="44" cy="32" r="2" fill="#D4AF37"/></svg>
    </div>`;

  function appendUser(q, attachmentHtml) {
    const html = `
      <article class="msg msg-user">
        <div class="msg-avatar">You</div>
        <div class="msg-bubble">
          ${attachmentHtml || ''}
          <p>${escapeHtml(q)}</p>
        </div>
      </article>
    `;
    chatStream.insertAdjacentHTML('beforeend', html);
    scrollChat();
  }

  function appendBotTyping() {
    chatStream.insertAdjacentHTML('beforeend', `
      <article class="msg msg-bot" data-typing>
        ${BOT_AVATAR_HTML}
        <div class="msg-bubble"><div class="typing"><span></span><span></span><span></span></div></div>
      </article>`);
    scrollChat();
  }

  function appendBot(title, paragraphs, sources) {
    const typing = chatStream.querySelector('[data-typing]');
    if (typing) typing.remove();
    const titleHtml = title ? `<p><strong>${title}</strong></p>` : '';
    const sourceHtml = sources ? `<div class="msg-cite">Source · ${sources}</div>` : '';
    chatStream.insertAdjacentHTML('beforeend', `
      <article class="msg msg-bot">
        ${BOT_AVATAR_HTML}
        <div class="msg-bubble">
          ${titleHtml}
          ${paragraphs.map(p => `<p>${p}</p>`).join('')}
          ${sourceHtml}
        </div>
      </article>`);
    scrollChat();
  }

  function appendBotEnrichment(text) {
    const last = chatStream.querySelector('.msg-bot:last-child .msg-bubble');
    if (!last) return;
    const html = `<div class="msg-enrich"><span class="enrich-tag">Gemini Nano · on-device</span><p>${escapeHtml(text)}</p></div>`;
    last.insertAdjacentHTML('beforeend', html);
    scrollChat();
  }

  function scrollChat() { chatStream.scrollTop = chatStream.scrollHeight; }
  function wait(ms) { return new Promise(r => setTimeout(r, ms)); }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;" }[c]));
  }

  /* ──────────────────────────────────────────────
     QUESTION HANDLER (with vision + Gemini Nano)
     ────────────────────────────────────────────── */
  async function handleQuestion(qRaw) {
    const q = qRaw.trim();

    // include attachment in user bubble
    let attachmentHtml = '';
    if (pendingFile) {
      if (pendingFile.type.startsWith('image/') && attachThumb && attachThumb.src) {
        attachmentHtml = `<div class="msg-attach"><img src="${attachThumb.src}" alt="" /></div>`;
      } else {
        attachmentHtml = `<div class="msg-attach msg-attach-file">📎 ${escapeHtml(pendingFile.name)}</div>`;
      }
    }
    appendUser(q, attachmentHtml);
    appendBotTyping();

    const visionInfo = pendingAnalysis;
    const visionFile = pendingFile;
    clearAttachment();

    // small think delay
    await wait(700 + Math.min(1400, q.length * 25));

    // — vision-first branch —
    if (visionInfo && !visionInfo.isText) {
      const topic = window.IVA_VISION.pickTopic(visionInfo.suggestedTopics) || null;
      const stats = visionInfo.stats;
      const visionParas = [
        `<strong>Vision read:</strong> ${escapeHtml(visionInfo.summary)}`,
        `<strong>Heuristics</strong> — category: <code>${visionInfo.category}</code> · brightness ${stats.brightness}/255 · sepia warmth ${stats.sepia} · edge-density ${stats.edgeDensity} · aspect ${stats.aspect} · hue <code>${stats.dominantHue}</code>.`,
        topic
          ? `Closest match in my corpus: <em>${topic.title}</em>. Here's what I know:`
          : `I don't have a confident corpus match — but I can give general Indus context.`
      ];
      appendBot('Image analysis', visionParas, 'Client-side vision · no API');
      if (topic) {
        await wait(500);
        appendBotTyping();
        await wait(700);
        appendBot(topic.title, topic.body, topic.sources);
        lastTopic = topic;
        await maybeEnrich(q || topic.title, topic.body[0]);
      }
      return;
    }

    if (visionInfo && visionInfo.isText) {
      appendBot('Text document received', [
        `I read <strong>${visionFile.name}</strong> (${visionInfo.text.length} chars). I'll treat its content as additional context for your question — but I still only answer within the Indus / Harappan domain.`
      ], 'Client-side · no upload');
      // fall through into KB answer using the question (and possibly the text)
    }

    // — RAG backend (if online) takes priority —
    if (ragOnline && window.IVA_RAG) {
      try {
        await runRagStream(q);
        return;
      } catch (err) {
        console.warn('[IVAI] RAG failed, falling back to KB:', err);
        ragOnline = false;
      }
    }

    // — KB answer (fallback) —
    const result = answer(q);
    appendBot(result.title, result.body, result.sources);
    if (result.topic) lastTopic = result.topic;
    await maybeEnrich(q, result.body[0]);
  }

  /* — RAG streaming answer with live citations — */
  async function runRagStream(question) {
    const typing = chatStream.querySelector('[data-typing]');
    if (typing) typing.remove();

    // Insert empty bot bubble we'll stream into
    const bubbleId = 'rag-' + Date.now();
    chatStream.insertAdjacentHTML('beforeend', `
      <article class="msg msg-bot">
        ${BOT_AVATAR_HTML}
        <div class="msg-bubble" id="${bubbleId}">
          <p class="rag-stream"></p>
          <div class="rag-cites" hidden></div>
        </div>
      </article>`);
    scrollChat();

    const bubble  = document.getElementById(bubbleId);
    const target  = bubble.querySelector('.rag-stream');
    const citesEl = bubble.querySelector('.rag-cites');

    let buf = '';
    try {
      for await (const ev of window.IVA_RAG.queryStream(question, chatHistory)) {
        if (ev.token) {
          buf += ev.token;
          target.textContent = buf;
          scrollChat();
        }
        if (ev.citations && ev.citations.length) {
          citesEl.hidden = false;
          citesEl.innerHTML =
            '<div class="rag-cites-label">Sources</div>' +
            ev.citations.map((c, i) => `
              <details class="rag-cite">
                <summary>
                  <span class="rag-cite-n">[${i+1}]</span>
                  <span class="rag-cite-doc">${escapeHtml(c.document)}</span>
                  <span class="rag-cite-page">p. ${c.page}</span>
                  <span class="rag-cite-score">${(c.score * 100).toFixed(0)}%</span>
                </summary>
                ${c.snippet ? `<p class="rag-cite-snippet">${escapeHtml(c.snippet)}…</p>` : ''}
              </details>
            `).join('');
        }
      }
    } catch (e) {
      target.textContent = buf || '[stream interrupted — falling back to KB]';
      throw e;
    }

    // Save to history for next turn
    chatHistory.push({ role: 'user', content: question });
    chatHistory.push({ role: 'assistant', content: buf });
    if (chatHistory.length > 8) chatHistory.splice(0, chatHistory.length - 8);
  }

  async function maybeEnrich(question, contextHint) {
    if (!window.IVA_NANO) return;
    const det = await window.IVA_NANO.state();
    if (det.state !== 'ready') return;
    const text = await window.IVA_NANO.ask(question, contextHint);
    if (text && text.length > 8) appendBotEnrichment(text);
  }

  /* ──────────────────────────────────────────────
     CORE: domain check + topic match
     ────────────────────────────────────────────── */
  function answer(qRaw) {
    const q = qRaw.toLowerCase().trim();

    // Step 1: try to match a topic FIRST (greetings, in-domain, etc.)
    // If we match anything well, return it — don't even check domain.
    const m = bestTopic(q);
    if (m) return { title: m.topic.title, body: m.topic.body, sources: m.topic.sources, topic: m.topic };

    // Step 2: if no topic matched, check hard out-of-scope (bitcoin, IPL, etc.)
    const outOfScopeHard = /(\bbitcoin\b|\bcrypto\b|\brecipe\b|\bweather\b|\bstock\b|\bcurrent president\b|\bchatgpt\b|\bgpt-?4\b|\bopenai\b|\biphone\b|\bandroid\b|\bnetflix\b|\bcricket score\b|\bipl\b|\bhomework\b|\bcalculate\b|\bsolve\b|\bjavascript\b|\bpython code\b)/i.test(q);
    if (outOfScopeHard) {
      return { title: window.IVA_KB.outOfDomain.title, body: window.IVA_KB.outOfDomain.body, sources: null };
    }

    // Step 3: nothing matched, but not obviously out-of-scope — show the helpful in-domain fallback
    return { title: window.IVA_KB.domainFallback.title, body: window.IVA_KB.domainFallback.body, sources: null };
  }

  /* ──────────────────────────────────────────────
     SMART TOPIC MATCHER
     - normalises input (handles spelling variants, hyphens)
     - synonym expansion
     - phrase + word-level scoring
     - boosts multi-word phrase matches
     ────────────────────────────────────────────── */
  const SYNONYMS = {
    'mohenjodaro': 'mohenjo-daro', 'moenjodaro': 'mohenjo-daro', 'mohenjo daro': 'mohenjo-daro',
    'civilisation': 'civilization', 'ivc': 'indus valley civilization',
    'harappa civilisation': 'harappan civilization', 'harrapa': 'harappa', 'harrapan': 'harappan',
    'pashupathi': 'pashupati', 'pasupati': 'pashupati',
    'dolavira': 'dholavira', 'dholavera': 'dholavira',
    'rakigarhi': 'rakhigarhi', 'rakhigari': 'rakhigarhi',
    'ghagar': 'ghaggar', 'sarasvathi': 'sarasvati', 'saraswati': 'sarasvati',
    'mesopotamian': 'mesopotamia', 'sumerian': 'sumer', 'meluha': 'meluhha',
    'sealings': 'seals', 'inscription': 'script', 'inscriptions': 'script',
    'bath': 'great bath', 'bathing': 'great bath',
    'farming': 'agriculture', 'crops': 'agriculture',
    'depicts': 'shows', 'depict': 'shows', 'represent': 'shows',
    'ended': 'decline', 'collapse': 'decline', 'collapsed': 'decline', 'fall': 'decline',
    'language': 'script', 'writing': 'script', 'writing system': 'script'
  };

  function normalize(q) {
    let n = q.toLowerCase().trim();
    n = n.replace(/[?!.,;:]/g, ' ').replace(/\s+/g, ' ');
    for (const [from, to] of Object.entries(SYNONYMS)) {
      const re = new RegExp('\\b' + from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'g');
      n = n.replace(re, to);
    }
    return n;
  }

  function bestTopic(q) {
    const qn = normalize(q);
    const qWords = new Set(qn.split(/\s+/).filter(w => w.length > 2));

    // STOP WORDS — these don't count as meaningful overlap
    const STOP = new Set(['the','what','was','were','are','tell','about','more','some','this','that','have','has','for','from','with','any','can','may','our','your','their','its','they']);

    let best = null, bestScore = 0;
    window.IVA_KB.topics.forEach(t => {
      let phraseScore = 0;            // score from full phrase matches
      let wordScore   = 0;            // best word-level match score (not summed)
      t.keys.forEach(k => {
        const kn = k.toLowerCase();
        if (qn.includes(kn)) {
          // full phrase match — strongly boost multi-word
          const wc = kn.split(/\s+/).length;
          phraseScore += kn.length * (wc > 1 ? 3 : 1.5);
          return;
        }
        const kWords = kn.split(/\s+/).filter(w => w.length > 2 && !STOP.has(w));
        if (kWords.length === 0) return;
        if (kWords.every(w => qWords.has(w))) {
          // every meaningful word of the key is in the question — strong match
          wordScore = Math.max(wordScore, kn.length * 1.5);
        } else {
          // partial overlap of meaningful words only — small contribution
          const overlap = kWords.filter(w => qWords.has(w)).length;
          if (overlap === kWords.length) {
            wordScore = Math.max(wordScore, kn.length);
          } else if (overlap > 0) {
            wordScore = Math.max(wordScore, overlap * 3);
          }
        }
      });
      // total = phrase matches + best single word-level match (not sum)
      const score = phraseScore + wordScore;
      if (score > bestScore) { bestScore = score; best = t; }
    });

    if (bestScore >= 2) return { topic: best, score: bestScore };
    return null;
  }

})();
