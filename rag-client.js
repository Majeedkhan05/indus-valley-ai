/* =========================================================
   Indus Valley AI — Optional RAG backend connector
   ─────────────────────────────────────────────────────────
   When the FastAPI backend is running on http://localhost:8000,
   this module takes over chat answering with grounded RAG +
   Ollama LLM responses. If the backend is offline, the site
   falls back transparently to the keyword KB.
   ========================================================= */
window.IVA_RAG = (function() {

  const BASE = (localStorage.getItem('ivai_backend_url') || 'http://localhost:8000').replace(/\/$/, '');
  let _online = false;
  let _info = null;

  async function ping() {
    try {
      const r = await fetch(BASE + '/health', { method: 'GET', cache: 'no-store' });
      if (!r.ok) throw new Error('not ok');
      _info = await r.json();
      _online = true;
      return _info;
    } catch (e) {
      _online = false;
      _info = null;
      return null;
    }
  }

  async function query(question, history = []) {
    const r = await fetch(BASE + '/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, top_k: 6, history })
    });
    if (!r.ok) throw new Error('query failed: ' + r.status);
    return await r.json();
  }

  /** Streaming generator (yields token strings, then a final {citations} object) */
  async function* queryStream(question, history = []) {
    const r = await fetch(BASE + '/query_stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, top_k: 6, history })
    });
    if (!r.ok || !r.body) throw new Error('stream failed: ' + r.status);

    const reader = r.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop() || '';
      for (const ev of events) {
        const line = ev.trim();
        if (!line.startsWith('data:')) continue;
        try {
          const obj = JSON.parse(line.slice(5).trim());
          yield obj;
        } catch (e) { /* skip */ }
      }
    }
  }

  async function uploadPdf(file) {
    const fd = new FormData();
    fd.append('file', file);
    const r = await fetch(BASE + '/upload_pdf', { method: 'POST', body: fd });
    if (!r.ok) throw new Error('upload failed: ' + r.status);
    return await r.json();
  }

  async function analyzeImage(file) {
    const fd = new FormData();
    fd.append('file', file);
    const r = await fetch(BASE + '/analyze_image', { method: 'POST', body: fd });
    if (!r.ok) throw new Error('image analysis failed: ' + r.status);
    return await r.json();
  }

  function setBackendUrl(url) {
    localStorage.setItem('ivai_backend_url', url);
  }

  function isOnline() { return _online; }
  function info()     { return _info; }

  return { ping, query, queryStream, uploadPdf, analyzeImage, setBackendUrl, isOnline, info };
})();
