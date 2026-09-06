(() => {
  const content = document.getElementById('content');
  const sidebarNav = document.getElementById('sidebarNav');
  const globalSearch = document.getElementById('globalSearch');
  const palette = document.getElementById('searchPalette');
  const paletteSearch = document.getElementById('paletteSearch');
  const paletteResults = document.getElementById('paletteResults');
  const toast = document.getElementById('toast');
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('mobileBackdrop');
  const wordCountSmall = document.getElementById('wordCountSmall');

  const state = { paletteSelected: 0, lastQuery: '' };
  const RECENT_KEY = 'dicionario-recentes-v1';

  const STOP = new Set('a ao aos as um uma uns umas de do da dos das e ou em no na nos nas para por com sem que isso isto aquilo eu voce você seu sua seus suas ser estar ter há mais menos como onde quando qual quais quem porque por quê entre sobre muito muita muito pouco poucas não sim já só apenas algo aquilo aquele aquela aquelas aqueles o os um uma'.split(' '));

  const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[c]));
  const normalize = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const tokens = (value) => normalize(value).split(/[^a-z0-9]+/).filter(t => t.length > 1 && !STOP.has(t));
  const slug = (value) => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

  function getRecent() {
    try { return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]'); } catch { return []; }
  }
  function setRecent(list) {
    try { localStorage.setItem(RECENT_KEY, JSON.stringify(list.slice(0, 12))); } catch {}
  }
  function pushRecent(id) {
    if (!ENTRY_MAP.has(id)) return;
    const list = getRecent().filter(x => x !== id);
    list.unshift(id);
    setRecent(list);
  }

  const APP_BASE = window.__DICIONARIO_BASE__ || new URL('./', location.href).href;
  const isFile = location.protocol === 'file:';

  function hrefFor(id) {
    const path = `palavras/${encodeURIComponent(id)}`;
    return isFile ? `#/${path}` : new URL(path, APP_BASE).pathname + new URL(path, APP_BASE).search + new URL(path, APP_BASE).hash;
  }
  function navigate(id) {
    const target = hrefFor(id);
    if (target.startsWith('#')) location.hash = target.slice(1);
    else history.pushState({}, '', target);
    render();
    closeSidebar();
  }

  function currentRoute() {
    let value = location.pathname.replace(/^\/+/, '');
    if (value.startsWith('palavras/')) return { type: 'word', id: decodeURIComponent(value.slice(9)) };
    if (value === 'sobre') return { type: 'about' };
    if (value.startsWith('categoria/')) return { type: 'category', category: decodeURIComponent(value.slice(10)) };
    if (location.hash) {
      const h = decodeURIComponent(location.hash.replace(/^#\/?/, ''));
      if (h.startsWith('palavras/')) return { type: 'word', id: h.slice(9) };
      if (h === 'sobre') return { type: 'about' };
      if (h.startsWith('categoria/')) return { type: 'category', category: h.slice(10) };
    }
    return { type: 'home' };
  }

  function categoryHref(category) {
    const path = `categoria/${encodeURIComponent(category)}`;
    if (isFile) return `#/${path}`;
    const url = new URL(path, APP_BASE);
    return url.pathname + url.search + url.hash;
  }

  function renderSidebar(route) {
    const nav = [
      { label: 'Comece aqui', href: '#/', id: 'home' },
      ...CATEGORY_ORDER.map(category => ({ label: category, href: categoryHref(category), id: `cat:${category}`, count: CATEGORY_CATALOGS[category].length }))
    ];
    sidebarNav.innerHTML = `
      <div class="sidebar-section">
        <div class="sidebar-label">Navegação</div>
        ${nav.slice(0,1).map(item => `<a class="sidebar-link ${route.type === 'home' ? 'active' : ''}" href="${item.href}" data-route-link><span class="sidebar-dot"></span><span>${escapeHtml(item.label)}</span></a>`).join('')}
      </div>
      <div class="sidebar-section">
        <div class="sidebar-label">Explorar</div>
        ${nav.slice(1).map(item => `<a class="sidebar-link ${route.category === item.label || (route.type === 'word' && ENTRY_MAP.get(route.id)?.category === item.label) ? 'active' : ''}" href="${item.href}" data-route-link><span class="sidebar-dot"></span><span>${escapeHtml(item.label)}</span><span class="count">${item.count}</span></a>`).join('')}
      </div>`;
    wordCountSmall.textContent = `${DICTIONARY.length.toLocaleString('pt-BR')} palavras`;
  }

  function routeLink(id, text = null, cls = '') {
    const e = ENTRY_MAP.get(id);
    if (!e) return escapeHtml(text || id);
    return `<a href="${hrefFor(e.id)}" class="${cls}" data-word-link data-id="${escapeHtml(e.id)}">${escapeHtml(text || e.word)}</a>`;
  }

  function smartLinkText(text) {
    const source = String(text || '');
    const candidates = DICTIONARY
      .filter(e => normalize(e.word).length >= 5)
      .sort((a, b) => normalize(b.word).length - normalize(a.word).length);

    const matches = [];
    const occupied = [];
    const isLetter = (char) => char && /[\p{L}\p{N}]/u.test(char);

    for (const e of candidates) {
      const needle = String(e.word || '');
      if (!needle) continue;
      const hay = source.toLocaleLowerCase('pt-BR');
      const target = needle.toLocaleLowerCase('pt-BR');
      let from = 0;
      while (from < hay.length) {
        const at = hay.indexOf(target, from);
        if (at === -1) break;
        const before = source[at - 1];
        const after = source[at + target.length];
        const boundary = !isLetter(before) && !isLetter(after);
        const rangeEnd = at + target.length;
        const overlaps = occupied.some(([a, b]) => at < b && rangeEnd > a);
        if (boundary && !overlaps) {
          matches.push({ start: at, end: rangeEnd, entry: e });
          occupied.push([at, rangeEnd]);
          break;
        }
        from = at + target.length;
      }
    }

    matches.sort((a, b) => a.start - b.start);
    let output = '';
    let cursor = 0;
    for (const match of matches) {
      if (match.start < cursor) continue;
      output += escapeHtml(source.slice(cursor, match.start));
      output += routeLink(match.entry.id, source.slice(match.start, match.end), 'inline-word');
      cursor = match.end;
    }
    output += escapeHtml(source.slice(cursor));
    return output;
  }

  function scoreEntry(entry, query) {
    const q = normalize(query).trim();
    if (!q) return 0;
    const qs = tokens(q);
    const wordN = normalize(entry.word);
    const defN = normalize(entry.definition);
    const recN = normalize(entry.recognition);
    const catN = normalize(entry.category);
    const relatedN = normalize(entry.related.join(' '));
    let score = 0;
    if (wordN === q) score += 100;
    if (wordN.includes(q)) score += 55;
    if (catN.includes(q)) score += 15;
    if (defN.includes(q)) score += 24;
    if (recN.includes(q)) score += 20;
    if (relatedN.includes(q)) score += 15;
    for (const token of qs) {
      if (wordN.includes(token)) score += 24;
      if (defN.includes(token)) score += 8;
      if (recN.includes(token)) score += 7;
      if (catN.includes(token)) score += 5;
      if (relatedN.includes(token)) score += 4;
    }
    return score;
  }

  function search(query, limit = 60) {
    if (!query.trim()) return [];
    return DICTIONARY.map(e => ({ e, score: scoreEntry(e, query) }))
      .filter(x => x.score > 0)
      .sort((a,b) => b.score - a.score || a.e.word.localeCompare(b.e.word, 'pt-BR'))
      .slice(0, limit)
      .map(x => x.e);
  }

  function randomEntry(filterFn = null) {
    const pool = filterFn ? DICTIONARY.filter(filterFn) : DICTIONARY;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function recentEntries() { return getRecent().map(id => ENTRY_MAP.get(id)).filter(Boolean); }

  function wordCard(e) {
    return `<a class="word-card" href="${hrefFor(e.id)}" data-word-link data-id="${escapeHtml(e.id)}">
      <div class="word">${escapeHtml(e.word)}</div>
      <div class="type">${escapeHtml(e.type)}</div>
      <div class="snippet">${escapeHtml(e.definition)}</div>
      <div class="row"><span class="tag">${escapeHtml(e.category)}</span><span class="arrow">↗</span></div>
    </a>`;
  }

  function home() {
    const highlights = [
      ENTRY_MAP.get('saudade'), ENTRY_MAP.get('ambivalencia'), ENTRY_MAP.get('efemeridade'),
      ENTRY_MAP.get('epifania'), ENTRY_MAP.get('ressonancia'), ENTRY_MAP.get('quietude'),
    ].filter(Boolean);
    const recents = recentEntries();
    const recentBlock = recents.length ? recents.slice(0,6).map(wordCard).join('') : highlights.slice(0,6).map(wordCard).join('');
    const cats = CATEGORY_ORDER.map((c, i) => ({ c, i })).slice(0, 10);
    const featured = highlights.map(wordCard).join('');
    return `<div class="hero">
      <div class="eyebrow">um dicionário para coisas difíceis de nomear</div>
      <h1>Às vezes, o que falta não é uma resposta.<br><em>É uma palavra.</em></h1>
      <p>O Dicionário reúne palavras para sentimentos, estados mentais, relações, experiências, sensações e ideias que costumam escapar de uma explicação simples. Entre, escolha uma palavra qualquer e veja onde ela leva.</p>
      <div class="hero-actions"><button class="button primary" data-surprise><span class="icon">✦</span> Me surpreenda</button><button class="button" data-open-search><span class="icon">⌕</span> Procurar uma palavra</button></div>
    </div>

    <section class="section">
      <div class="section-head"><div><div class="eyebrow">01</div><h2>Explore por assunto</h2></div><p>${DICTIONARY.length.toLocaleString('pt-BR')} entradas<br>em ${CATEGORY_ORDER.length} categorias</p></div>
      <div class="category-grid">${cats.map(({c}) => `<a class="category-card" href="${categoryHref(c)}" data-route-link><h3>${escapeHtml(c)}</h3><p>${escapeHtml(CATEGORY_META[c]?.description || '')}</p><div class="card-foot"><span class="tiny-line"></span>${CATEGORY_CATALOGS[c].length} palavras</div></a>`).join('')}</div>
    </section>

    <section class="section">
      <div class="section-head"><div><div class="eyebrow">02</div><h2>Algumas palavras</h2></div><p>Comece por qualquer uma.<br>A ideia é continuar clicando.</p></div>
      <div class="word-grid">${featured}</div>
    </section>

    <section class="section">
      <div class="section-head"><div><div class="eyebrow">03</div><h2>${recents.length ? 'Você passou por aqui' : 'Sugestões para continuar'}</h2></div><p>${recents.length ? 'Seu histórico fica apenas neste navegador.' : 'Entradas selecionadas para uma primeira visita.'}</p></div>
      <div class="word-grid">${recentBlock}</div>
    </section>

    <section class="section"><div class="callout"><p><strong>Como usar:</strong> não precisa saber o que procurar. Pesquise por uma palavra, uma situação ou até uma frase vaga como “sentir falta de algo que acabou”. O mecanismo procura em nomes, definições, categorias, conexões e situações de reconhecimento.</p></div></section>`;
  }

  function categoryPage(category) {
    if (!CATEGORY_META[category]) return notFound();
    const entries = DICTIONARY.filter(e => e.category === category);
    return `<div class="list-page">
      <div class="page-top"><a class="breadcrumb-link" href="#/" data-route-link>Dicionário</a><span class="breadcrumb-sep">/</span><span>${escapeHtml(category)}</span></div>
      <div class="eyebrow">coleção ${String(CATEGORY_META[category].index + 1).padStart(2,'0')}</div>
      <h1>${escapeHtml(category)}</h1>
      <p class="list-intro">${escapeHtml(CATEGORY_META[category].description)}</p>
      <div class="results-bar"><span>${entries.length} entradas</span><span>ordem alfabética</span></div>
      <div class="result-list">${entries.slice().sort((a,b)=>a.word.localeCompare(b.word,'pt-BR')).map(e => `<a class="result-row" href="${hrefFor(e.id)}" data-word-link data-id="${escapeHtml(e.id)}"><div><div class="result-word">${escapeHtml(e.word)}</div><div class="result-type">${escapeHtml(e.type)}</div></div><div><div class="result-definition">${escapeHtml(e.definition)}</div><div class="result-extra">${escapeHtml(e.termKind)}</div></div></a>`).join('')}</div>
    </div>`;
  }

  function relatedEntries(entry) {
    const ids = [...new Set(entry.related || [])];
    const direct = ids.map(id => ENTRY_MAP.get(id)).filter(Boolean);
    const same = DICTIONARY.filter(e => e.category === entry.category && e.id !== entry.id && !ids.includes(e.id));
    while (direct.length < 5 && same.length) direct.push(same[Math.floor(Math.random() * same.length)]);
    return [...new Map(direct.map(e=>[e.id,e])).values()].slice(0,6);
  }

  function entryPage(id) {
    const e = ENTRY_MAP.get(id);
    if (!e) return notFound();
    pushRecent(e.id);
    document.title = `${e.word} — Dicionário`;
    const categoryEntries = DICTIONARY.filter(x => x.category === e.category).sort((a,b)=>a.word.localeCompare(b.word,'pt-BR'));
    const pos = categoryEntries.findIndex(x=>x.id===e.id);
    const prev = categoryEntries[(pos - 1 + categoryEntries.length) % categoryEntries.length];
    const next = categoryEntries[(pos + 1) % categoryEntries.length];
    const related = relatedEntries(e);
    const contrast = (e.contrasts || []).map(id => ENTRY_MAP.get(id)).filter(Boolean);
    return `<div class="entry-page">
      <div class="page-top"><a class="breadcrumb-link" href="#/" data-route-link>Dicionário</a><span class="breadcrumb-sep">/</span><a class="breadcrumb-link" href="${categoryHref(e.category)}" data-route-link>${escapeHtml(e.category)}</a><span class="breadcrumb-sep">/</span><span>${escapeHtml(e.word)}</span></div>
      <article class="entry">
        <div class="entry-meta"><span class="pill accent">${escapeHtml(e.category)}</span><span class="pill">${escapeHtml(e.termKind)}</span></div>
        <h1>${escapeHtml(e.word)}</h1>
        <div class="entry-type">${escapeHtml(e.type)}</div>
        <div class="entry-lead">${smartLinkText(e.definition)}</div>
        <div class="entry-grid">
          <div class="entry-main">
            <section><h2>Como reconhecer</h2><p class="text">${smartLinkText(e.recognition)}</p></section>
            <section><h2>Palavras relacionadas</h2><div class="link-list">${(e.related || []).map(id => ENTRY_MAP.has(id) ? routeLink(id) : '').join('') || '<span class="text">Ainda não há conexões cadastradas.</span>'}</div></section>
            <section><h2>Contrastes</h2><div class="link-list">${contrast.length ? contrast.map(x=>routeLink(x.id)).join('') : '<span class="text">Nenhum contraste definido para esta entrada.</span>'}</div></section>
            <section><h2>Continue explorando</h2><div class="continue">${related.map(x=>`<a href="${hrefFor(x.id)}" data-word-link data-id="${escapeHtml(x.id)}"><div class="c-word">${escapeHtml(x.word)}</div><div class="c-cat">${escapeHtml(x.category)}</div></a>`).join('')}</div></section>
            <div class="entry-nav">
              <a href="${hrefFor(prev.id)}" data-word-link data-id="${escapeHtml(prev.id)}"><div class="label">Anterior</div><div class="nav-word">← ${escapeHtml(prev.word)}</div></a>
              <a href="${hrefFor(next.id)}" class="next" data-word-link data-id="${escapeHtml(next.id)}"><div class="label">Próxima</div><div class="nav-word">${escapeHtml(next.word)} →</div></a>
            </div>
          </div>
          <aside>
            <div class="sidebar-card"><h3>Na categoria</h3><div class="link-list"><a class="chip-link" href="${categoryHref(e.category)}" data-route-link>Ver as ${categoryEntries.length} entradas</a></div></div>
            <div class="sidebar-card"><h3>Compartilhar</h3><div class="link-list"><button class="chip-link" data-copy-link data-id="${escapeHtml(e.id)}">Copiar link</button></div></div>
          </aside>
        </div>
      </article>
    </div>`;
  }

  function about() {
    document.title = 'Sobre — Dicionário';
    return `<div class="list-page">
      <div class="page-top"><a class="breadcrumb-link" href="#/" data-route-link>Dicionário</a><span class="breadcrumb-sep">/</span><span>Sobre</span></div>
      <div class="eyebrow">um projeto em crescimento</div><h1>Dar nome muda a maneira de olhar.</h1>
      <p class="list-intro">O Dicionário foi pensado para ser consultado sem pressa. Em vez de organizar o mundo apenas por significado formal, ele tenta aproximar palavras de situações: coisas que sentimos, pensamos, lembramos, fazemos e reconhecemos nos outros.</p>
      <div class="about-grid">
        <div class="about-card"><h3>Conteúdo independente</h3><p>As definições desta interface foram escritas especificamente para este projeto. O objetivo não é reproduzir verbetes de uma obra de referência, e sim explicar conceitos em linguagem brasileira clara e humana.</p></div>
        <div class="about-card"><h3>Conexões primeiro</h3><p>Cada entrada aponta para outras. A proposta é que uma busca raramente termine na própria palavra: ela deve abrir uma trilha para outra experiência, outro conceito ou outro modo de dizer.</p></div>
        <div class="about-card"><h3>Sem backend</h3><p>O projeto é totalmente estático. O banco fica em <span class="code-inline">data.js</span>, e a interface em <span class="code-inline">app.js</span>. É possível abrir localmente ou publicar em qualquer hospedagem estática.</p></div>
        <div class="about-card"><h3>Um arquivo para crescer</h3><p>Para adicionar uma entrada, basta editar o catálogo em <span class="code-inline">data.js</span>. A interface monta busca, relações, categorias e páginas automaticamente.</p></div>
      </div>
      <section class="section"><div class="callout"><p><strong>${DICTIONARY.length.toLocaleString('pt-BR')} conceitos em ${CATEGORY_ORDER.length} categorias.</strong> O banco inicial mistura vocabulário comum, termos raros e conceitos contemporâneos. Termos estrangeiros são marcados na própria entrada.</p></div></section>
    </div>`;
  }

  function notFound() {
    document.title = 'Não encontrado — Dicionário';
    return `<div class="list-page"><div class="eyebrow">404</div><h1>Essa palavra escapou.</h1><p class="list-intro">Não encontrei essa entrada no catálogo. Talvez outra palavra consiga dizer melhor o que você está procurando.</p><div class="hero-actions"><button class="button" data-open-search>Buscar novamente</button><button class="button primary" data-surprise>Me surpreenda</button></div></div>`;
  }

  function render(route = currentRoute()) {
    renderSidebar(route);
    if (route.type === 'word') content.innerHTML = entryPage(route.id);
    else if (route.type === 'category') content.innerHTML = categoryPage(route.category);
    else if (route.type === 'about') content.innerHTML = about();
    else { document.title = 'Dicionário — talvez exista uma palavra'; content.innerHTML = home(); }
    bindContent();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(showToast.timer);
    showToast.timer = setTimeout(() => toast.classList.remove('show'), 1900);
  }

  async function copyLink(id) {
    const url = new URL(hrefFor(id), location.href).href;
    try { await navigator.clipboard.writeText(url); showToast('Link copiado'); }
    catch { showToast('Não foi possível copiar'); }
  }

  function openSearch(query='') {
    palette.classList.remove('hidden');
    paletteSearch.value = query;
    state.lastQuery = query;
    state.paletteSelected = 0;
    renderPalette(query);
    setTimeout(() => paletteSearch.focus(), 0);
  }
  function closeSearch() { palette.classList.add('hidden'); globalSearch.value = ''; }

  function renderPalette(query) {
    const results = search(query, 12);
    if (!query.trim()) {
      const featured = recentEntries().slice(0,5);
      paletteResults.innerHTML = featured.length
        ? `<div class="palette-head" style="border:0;padding:8px 8px 6px">Recentes</div>${featured.map(paletteRow).join('')}`
        : `<div class="palette-empty">Experimente procurar uma palavra, uma sensação ou uma frase.</div>`;
      return;
    }
    paletteResults.innerHTML = results.length ? results.map((e,i) => paletteRow(e,i===0)).join('') : `<div class="palette-empty">Nenhuma entrada encontrada para “${escapeHtml(query)}”.</div>`;
  }
  function paletteRow(e, selected=false) {
    return `<div class="palette-result ${selected ? 'selected' : ''}" data-id="${escapeHtml(e.id)}" data-palette-result><div><div class="name">${escapeHtml(e.word)}</div><div class="meta">${escapeHtml(e.category)}</div></div><div class="desc">${escapeHtml(e.definition)}</div></div>`;
  }

  function bindContent() {
    content.querySelectorAll('[data-word-link]').forEach(a => a.addEventListener('click', (ev) => {
      ev.preventDefault();
      const id = a.dataset.id;
      if (id) navigate(id);
    }));
    content.querySelectorAll('[data-route-link]').forEach(a => a.addEventListener('click', (ev) => {
      const href = a.getAttribute('href');
      if (!href) return;
      if (href.startsWith('#')) { ev.preventDefault(); history.replaceState({}, '', href); render(); closeSidebar(); }
      else { ev.preventDefault(); if (href.startsWith('/')) history.pushState({}, '', href); render(); closeSidebar(); }
    }));
    content.querySelectorAll('[data-surprise]').forEach(b => b.addEventListener('click', () => navigate(randomEntry().id)));
    content.querySelectorAll('[data-open-search]').forEach(b => b.addEventListener('click', () => openSearch()));
    content.querySelectorAll('[data-copy-link]').forEach(b => b.addEventListener('click', () => copyLink(b.dataset.id)));
  }

  globalSearch.addEventListener('focus', () => openSearch(globalSearch.value));
  globalSearch.addEventListener('input', () => openSearch(globalSearch.value));
  globalSearch.addEventListener('keydown', (e) => { if (e.key === 'Enter') { const [r] = search(globalSearch.value,1); if (r) navigate(r.id); } });

  paletteSearch.addEventListener('input', () => { state.lastQuery=paletteSearch.value; state.paletteSelected=0; renderPalette(paletteSearch.value); });
  paletteResults.addEventListener('click', (e) => {
    const row = e.target.closest('[data-palette-result]');
    if (row) { navigate(row.dataset.id); closeSearch(); }
  });
  palette.addEventListener('click', e => { if (e.target.matches('[data-close-search], .palette-backdrop')) closeSearch(); });

  document.getElementById('openSidebar').addEventListener('click', () => { sidebar.classList.add('open'); backdrop.classList.add('show'); });
  document.getElementById('closeSidebar').addEventListener('click', closeSidebar);
  backdrop.addEventListener('click', closeSidebar);
  function closeSidebar() { sidebar.classList.remove('open'); backdrop.classList.remove('show'); }

  document.addEventListener('click', (e) => {
    const nav = e.target.closest('[data-nav]');
    if (nav) closeSidebar();
  });

  window.addEventListener('popstate', () => render());
  window.addEventListener('hashchange', () => render());

  document.addEventListener('keydown', (e) => {
    const metaK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
    if (metaK) { e.preventDefault(); openSearch(); return; }
    if (e.key === 'Escape') { closeSearch(); closeSidebar(); return; }
    const tag = document.activeElement?.tagName;
    if ((e.metaKey || e.ctrlKey) || tag === 'INPUT' || tag === 'TEXTAREA') return;
    const route = currentRoute();
    if (route.type === 'word') {
      const current = ENTRY_MAP.get(route.id); if (!current) return;
      const entries=DICTIONARY.filter(x=>x.category===current.category).sort((a,b)=>a.word.localeCompare(b.word,'pt-BR'));
      const pos=entries.findIndex(x=>x.id===current.id);
      if (e.key === 'ArrowLeft') navigate(entries[(pos-1+entries.length)%entries.length].id);
      if (e.key === 'ArrowRight') navigate(entries[(pos+1)%entries.length].id);
    }
  });


  render();
})();
