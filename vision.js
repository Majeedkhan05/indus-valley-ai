/* =========================================================
   VISION — heuristic image analyzer
   No API. No tokens. Pure client-side canvas + statistics.
   Goal: classify an uploaded image into broad Indus-relevant
   categories and route to the right KB topic.
   ========================================================= */

window.IVA_VISION = (function() {

  /**
   * Analyze an Image element. Returns:
   * {
   *   summary: short human-readable string,
   *   category: 'seal' | 'script' | 'artifact' | 'map' | 'site-photo' | 'illustration' | 'unknown',
   *   stats: {brightness, sepia, edgeDensity, aspect, dominantHue},
   *   suggestedTopics: [topicTitle, ...]
   * }
   */
  function analyze(imgEl) {
    const cv = document.createElement('canvas');
    const W = 96; // small for speed
    const H = 96;
    cv.width = W; cv.height = H;
    const ctx = cv.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(imgEl, 0, 0, W, H);
    const data = ctx.getImageData(0, 0, W, H).data;

    // ── stats accumulators
    let totalR=0,totalG=0,totalB=0, totalLum=0;
    const pixels = W * H;
    const histR = new Array(8).fill(0);
    const histG = new Array(8).fill(0);
    const histB = new Array(8).fill(0);

    for (let i = 0; i < data.length; i += 4) {
      const r=data[i], g=data[i+1], b=data[i+2];
      totalR+=r; totalG+=g; totalB+=b;
      totalLum += 0.299*r + 0.587*g + 0.114*b;
      histR[r >> 5]++;
      histG[g >> 5]++;
      histB[b >> 5]++;
    }
    const avgR = totalR/pixels, avgG = totalG/pixels, avgB = totalB/pixels;
    const brightness = totalLum/pixels;            // 0..255
    const sepia = sepiaScore(avgR, avgG, avgB);    // 0..1, brown-cream warmth
    const aspect = imgEl.naturalWidth / imgEl.naturalHeight;
    const dominantHue = classifyHue(avgR, avgG, avgB);

    // ── edge density (Sobel-light approx via luminance gradient)
    const edgeDensity = computeEdgeDensity(data, W, H);

    // ── monochrome-ness: variance between channels
    const colorSpread = (Math.abs(avgR-avgG) + Math.abs(avgG-avgB) + Math.abs(avgR-avgB)) / 3;

    // ── classify
    let category = 'unknown';
    let summary = '';
    let suggestedTopics = [];

    const isWarm = sepia > 0.45;
    const isDark = brightness < 80;
    const isLight = brightness > 200;
    const isSquarish = Math.abs(aspect - 1) < 0.18;
    const isHighEdge = edgeDensity > 0.18;
    const isMonochrome = colorSpread < 18;
    const isLineArt = isLight && isHighEdge && isMonochrome;
    const isPhoto = !isLineArt && colorSpread > 20;

    // — seal (square-ish, warm sepia, photo-like, mid edge)
    if (isWarm && isSquarish && isPhoto && edgeDensity > 0.08) {
      category = 'seal';
      summary = 'A photograph of what appears to be an Indus-style seal — square-ish, warm steatite tones, with surface relief detail.';
      suggestedTopics = ['Indus seals — what they are and what they do', 'The "unicorn" motif', 'How a seal was actually made'];
    }
    // — script line art (high edge density, light bg, low color)
    else if (isLineArt) {
      category = 'script';
      summary = 'A line-art / glyph-style image. Looks like a transcription of an Indus script sign or a sign-sequence.';
      suggestedTopics = ['The Indus script — current status', 'The "fish" sign — the most frequent sign in the script', 'Parpola — the Dravidian decipherment hypothesis'];
    }
    // — map / aerial / site-plan (greenish + brown + high edge from grid)
    else if (dominantHue === 'green' || dominantHue === 'brown-green') {
      category = 'map';
      summary = 'Looks like an aerial photo, site map, or excavation plan.';
      suggestedTopics = ['Indus urban planning & drainage', 'Mohenjo-daro vs Harappa vs Dholavira', 'Dholavira (Gujarat)'];
    }
    // — figurine / artefact photo (warm, photo, non-square)
    else if (isWarm && isPhoto) {
      category = 'artifact';
      summary = 'A photograph of an artefact — likely a figurine, pot, ornament, or sculptural object in clay/stone/metal.';
      suggestedTopics = ['Terracotta figurines', 'The "Priest-King" statuette', 'The Dancing Girl'];
    }
    // — illustration / diagram (light bg, lower edge)
    else if (isLight && colorSpread < 35) {
      category = 'illustration';
      summary = 'Looks like an illustration, diagram, or scholarly figure.';
      suggestedTopics = ['The Indus / Harappan Civilization — overview', 'Chronology — Indus phases & dating'];
    }
    // — generic site photo (dark, high edge, varied color)
    else if (isPhoto) {
      category = 'site-photo';
      summary = 'A general photograph — possibly a site, structure, or landscape.';
      suggestedTopics = ['Indus urban planning & drainage', 'The Great Bath of Mohenjo-daro'];
    }

    if (!summary) {
      summary = 'I can\'t classify this image confidently. I\'ll attach it to your message and use the text context to answer.';
      suggestedTopics = ['The Indus / Harappan Civilization — overview'];
    }

    return {
      summary,
      category,
      stats: {
        brightness: Math.round(brightness),
        sepia: +sepia.toFixed(2),
        edgeDensity: +edgeDensity.toFixed(3),
        aspect: +aspect.toFixed(2),
        dominantHue,
        colorSpread: Math.round(colorSpread)
      },
      suggestedTopics
    };
  }

  /* — sepia score: how brownish-warm — */
  function sepiaScore(r, g, b) {
    if (r <= g) return 0;
    const warmth = (r - b) / 255;
    const balance = 1 - Math.abs((r - g) - (g - b)) / 255;
    return Math.max(0, Math.min(1, warmth * 1.6 * balance));
  }

  /* — categorical hue label — */
  function classifyHue(r, g, b) {
    const max = Math.max(r,g,b), min = Math.min(r,g,b);
    const delta = max - min;
    if (delta < 14) return 'gray';
    if (r > g && r > b) {
      if (g > b * 1.1) return 'brown';
      return 'red';
    }
    if (g > r && g > b) {
      if (r > b * 1.1) return 'brown-green';
      return 'green';
    }
    return 'cool';
  }

  /* — luminance-gradient edge density — */
  function computeEdgeDensity(data, W, H) {
    let edgeSum = 0;
    let count = 0;
    for (let y = 1; y < H - 1; y += 2) {
      for (let x = 1; x < W - 1; x += 2) {
        const i = (y * W + x) * 4;
        const ir = (y * W + (x + 1)) * 4;
        const id = ((y + 1) * W + x) * 4;
        const lum = 0.299*data[i]+0.587*data[i+1]+0.114*data[i+2];
        const lumR = 0.299*data[ir]+0.587*data[ir+1]+0.114*data[ir+2];
        const lumD = 0.299*data[id]+0.587*data[id+1]+0.114*data[id+2];
        const grad = Math.abs(lum - lumR) + Math.abs(lum - lumD);
        edgeSum += grad;
        count++;
      }
    }
    return (edgeSum / count) / 255;
  }

  /* — given a category + suggested topic titles, locate the topic in the KB — */
  function pickTopic(suggestedTitles) {
    if (!window.IVA_KB) return null;
    for (const title of suggestedTitles) {
      const t = window.IVA_KB.topics.find(x => x.title === title);
      if (t) return t;
    }
    return null;
  }

  /* — helper: read file → Image — */
  function fileToImage(file) {
    return new Promise((resolve, reject) => {
      if (!file.type.startsWith('image/')) return reject(new Error('not an image'));
      const url = URL.createObjectURL(file);
      const img = new Image();
      img.onload = () => resolve({ img, url });
      img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('image load failed')); };
      img.src = url;
    });
  }

  /* — helper: read file → text (for .txt, .md, etc) — */
  function fileToText(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error);
      reader.readAsText(file);
    });
  }

  return { analyze, pickTopic, fileToImage, fileToText };
})();
