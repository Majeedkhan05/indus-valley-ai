/* =========================================================
   Gemini Nano — on-device LLM enrichment
   Chrome 127+ (with flags). 100% local. No API key. No tokens.
   Falls back silently if unavailable.
   ========================================================= */

window.IVA_NANO = (function() {

  let session = null;
  let _state = 'unknown'; // 'unavailable' | 'unsupported' | 'downloading' | 'ready' | 'error'
  let _stateText = 'Detecting on-device model…';

  const SYSTEM_PROMPT = [
    'You are a domain-specific research assistant for the Indus Valley Civilization (c. 3300–1300 BCE).',
    '',
    'MANDATORY ANSWER STRUCTURE (every reply must follow this):',
    '1. DIRECT ANSWER — 1–2 sentences answering the question.',
    '2. EVIDENCE — specific sites (Dholavira, Harappa, Mohenjo-daro, Lothal, Kalibangan, Rakhigarhi), artefacts, or scholarly findings.',
    '3. INTERPRETATION — explain what the evidence implies.',
    '4. ALTERNATIVE VIEW — at least one competing or minority interpretation.',
    '5. LIMITATION — note gaps, debates, or caveats with cautious language.',
    '',
    'CONFIDENCE CONTROL:',
    '• AVOID: "universally", "definitive", "proves", "unique", "always", "never", "no civilization".',
    '• USE: "widely believed", "suggests", "likely indicates", "scholars debate", "remains contested", "cannot be confirmed".',
    '',
    'REDUNDANCY: Do NOT repeat information already stated in the same answer.',
    '',
    'HARD RULES:',
    '• Answer ONLY questions about the Indus / Harappan civilization. Refuse out-of-domain politely.',
    '• The Indus script remains UNDECIPHERED — never claim a confident phonetic reading.',
    '• The Rakhigarhi 2019 aDNA study found NO Steppe ancestry in mature-Harappan individuals.',
    '• Name scholars by surname when relevant (Marshall, Wheeler, Kenoyer, Possehl, Parpola, Mahadevan, Bisht, Shinde, Yajnadevam).',
    '• No video, animation, image, or multimedia generation.',
    '• Be concise — under 200 words.'
  ].join('\n');

  /** Detect availability. Resolves to {available: boolean, state: string, text: string} */
  async function detect() {
    try {
      // New API — window.LanguageModel
      if (typeof window !== 'undefined' && 'LanguageModel' in window) {
        const cap = await window.LanguageModel.availability().catch(() => null);
        if (cap === 'available' || cap === 'readily') {
          _state = 'ready'; _stateText = 'Gemini Nano · on-device';
          return { available: true, state: _state, text: _stateText };
        }
        if (cap === 'after-download' || cap === 'downloading' || cap === 'downloadable') {
          _state = 'downloading'; _stateText = 'Gemini Nano · downloading…';
          return { available: false, state: _state, text: _stateText };
        }
      }
      // Legacy API path — window.ai.languageModel
      if (typeof window !== 'undefined' && 'ai' in window && window.ai && window.ai.languageModel) {
        const cap = await window.ai.languageModel.capabilities().catch(() => null);
        if (cap && cap.available === 'readily') {
          _state = 'ready'; _stateText = 'Gemini Nano · on-device';
          return { available: true, state: _state, text: _stateText };
        }
        if (cap && cap.available === 'after-download') {
          _state = 'downloading'; _stateText = 'Gemini Nano · downloading…';
          return { available: false, state: _state, text: _stateText };
        }
      }
      _state = 'unsupported';
      _stateText = 'Gemini Nano · unavailable in this browser';
      return { available: false, state: _state, text: _stateText };
    } catch (e) {
      _state = 'error';
      _stateText = 'Gemini Nano · error';
      return { available: false, state: _state, text: _stateText };
    }
  }

  /** Lazy-create session */
  async function ensureSession() {
    if (session) return session;
    try {
      if ('LanguageModel' in window) {
        session = await window.LanguageModel.create({
          initialPrompts: [{ role: 'system', content: SYSTEM_PROMPT }],
          temperature: 0.4,
          topK: 3
        });
      } else if (window.ai && window.ai.languageModel) {
        session = await window.ai.languageModel.create({
          systemPrompt: SYSTEM_PROMPT,
          temperature: 0.4,
          topK: 3
        });
      }
    } catch (e) {
      session = null;
    }
    return session;
  }

  /**
   * Generate an enrichment paragraph for a given question.
   * Returns null if Nano isn't available — caller falls back.
   */
  async function ask(question, contextNote) {
    const det = await detect();
    if (!det.available) return null;
    const s = await ensureSession();
    if (!s) return null;
    const prompt = contextNote
      ? `Question: ${question}\n\nContext from a curated knowledge base: ${contextNote}\n\nAdd ONE concise paragraph (2–4 sentences) of additional, accurate context strictly within the Indus Valley domain. Do not repeat what the context already says.`
      : `Within the Indus Valley Civilization domain only — answer this in 2–4 short sentences, academically careful. If out of scope say so in one sentence.\n\nQuestion: ${question}`;
    try {
      const result = await s.prompt(prompt);
      return (result || '').trim();
    } catch (e) {
      return null;
    }
  }

  function state() { return { state: _state, text: _stateText }; }

  function destroy() {
    if (session && session.destroy) try { session.destroy(); } catch(_) {}
    session = null;
  }

  return { detect, ask, state, destroy };
})();
