/* Progressive enhancement: the generated reading record works without this file. */
(() => {
  'use strict';
  const treeTitles = {
    goal: 'Our goal and conditions', current_reality: 'What stands in the way',
    conflict: 'Where needs pull two ways', future_reality: 'The change we have chosen',
    prerequisite: 'Obstacles and prerequisites', transition: 'Actions to take'
  };
  const kinds = { goal: 'Goal', critical_success_factor: 'Critical success factor', necessary_condition: 'Necessary condition',
    undesirable_effect: 'Undesirable effect', cause: 'Cause', observation: 'Observation', objective: 'Objective', need: 'Need',
    prerequisite: 'Prerequisite', injection: 'Change', existing_condition: 'Existing condition', predicted_effect: 'Predicted effect',
    desirable_effect: 'Desired effect', obstacle: 'Obstacle', intermediate_objective: 'Intermediate objective', action: 'Action', expected_effect: 'Expected effect' };
  const relations = { necessary_for: 'is necessary for', contributes_to: 'contributes to' };
  const escape = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
  const dialog = document.querySelector('#item-dialog');
  const details = document.querySelector('#item-detail');
  const input = document.querySelector('#reasoning-search');
  let data, items, current, activeItem = null, previousFocus = null, closeFromRoute = false, routeOpenedDialog = false;
  let toastTimer;

  function readRoute() {
    const query = new URLSearchParams(location.search);
    return { view: ['overview', 'reasoning', 'record'].includes(query.get('view')) ? query.get('view') : 'overview',
      tree: Object.hasOwn(treeTitles, query.get('tree')) ? query.get('tree') : 'goal',
      mode: query.get('mode') === 'diagram' ? 'diagram' : 'reading',
      q: (query.get('q') || '').slice(0, 200), item: query.get('item') };
  }

  function itemURL(id) {
    const route = new URL(location.href);
    route.search = '';
    route.searchParams.set('view', 'reasoning');
    route.searchParams.set('tree', items.get(id).tree);
    route.searchParams.set('item', id);
    route.hash = `item-${id}`;
    return route;
  }

  function setRoute(next, replace = false) {
    const route = new URL(location.href);
    route.search = '';
    route.searchParams.set('view', next.view);
    if (next.view === 'reasoning') {
      route.searchParams.set('tree', next.tree);
      if (next.mode === 'diagram') route.searchParams.set('mode', 'diagram');
      if (next.q) route.searchParams.set('q', next.q);
    }
    if (next.item) route.searchParams.set('item', next.item);
    route.hash = next.item ? `item-${next.item}` : next.view;
    history[replace ? 'replaceState' : 'pushState']({demo: true, scroll: scrollY}, '', route);
    renderRoute();
  }

  function searchTree() {
    const term = current.q.toLocaleLowerCase().trim();
    const tree = data.trees[current.tree];
    const section = document.querySelector(`[data-tree="${current.tree}"]`);
    const matches = new Set();
    const selected = new Set();
    const matchText = item => item.isLink ? `${relations[item.relation]} ${item.from.map(id => items.get(id).text).join(' ')} ${items.get(item.to).text} ${item.accepted_by.join(' ')}` : `${item.text} ${kinds[item.kind]} ${item.accepted_by.join(' ')}`;
    for (const item of [...tree.nodes, ...tree.links]) {
      if (!term || matchText(items.get(item.id)).toLocaleLowerCase().includes(term)) {
        matches.add(item.id);
        if (item.from) { selected.add(item.to); item.from.forEach(id => selected.add(id)); }
        else selected.add(item.id);
      }
    }
    // A search retains whole connected components so it cannot alter the argument.
    let changed = true;
    while (changed) {
      changed = false;
      for (const link of tree.links) {
        const endpoints = [...link.from, link.to];
        if (endpoints.some(id => selected.has(id))) for (const id of endpoints) {
          if (!selected.has(id)) { selected.add(id); changed = true; }
        }
      }
    }
    for (const article of section.querySelectorAll('[data-node]')) {
      article.hidden = !selected.has(article.dataset.node);
      article.classList.toggle('search-match', Boolean(term && matches.has(article.dataset.node)));
    }
    for (const article of section.querySelectorAll('[data-connection]')) {
      const link = items.get(article.dataset.connection);
      article.hidden = !link.from.every(id => selected.has(id)) || !selected.has(link.to);
    }
    for (const graph of section.querySelectorAll('.graph-component')) {
      graph.hidden = ![...graph.querySelectorAll('[data-item]')].some(el => selected.has(el.dataset.item));
    }
    for (const card of section.querySelectorAll('[data-diagram] .statement-card')) card.hidden = !selected.has(card.dataset.item);
    for (const loose of section.querySelectorAll('.unconnected')) loose.hidden = ![...loose.querySelectorAll('.statement-card')].some(el => !el.hidden);
    for (const heading of section.querySelectorAll('.connections-heading')) heading.hidden = ![...section.querySelectorAll('[data-connection]')].some(el => !el.hidden);
    for (const empty of section.querySelectorAll('[data-diagram] .empty-state')) empty.hidden = Boolean(term && !matches.size);
    const status = document.querySelector('#search-status');
    status.textContent = term ? `${matches.size} matching ${matches.size === 1 ? 'item' : 'items'} in this view${selected.size ? '; connected context is included.' : '.'}` : 'Search is limited to this accepted public selection. Diagrams can be scrolled independently.';
    const noMatch = document.querySelector('#search-empty');
    noMatch.hidden = !term || Boolean(matches.size);
    section.querySelector('.reading-list').hidden = Boolean(term && !matches.size);
  }

  function renderRoute() {
    current = readRoute();
    if (current.item && items.has(current.item)) current.tree = items.get(current.item).tree;
    for (const panel of document.querySelectorAll('[data-view]')) panel.hidden = panel.dataset.view !== current.view;
    for (const link of document.querySelectorAll('[data-view-tab]')) {
      if (link.dataset.viewTab === current.view) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    }
    for (const section of document.querySelectorAll('[data-tree]')) section.hidden = section.dataset.tree !== current.tree;
    for (const link of document.querySelectorAll('[data-tree-tab]')) {
      link.setAttribute('aria-current', String(link.dataset.treeTab === current.tree));
      const route = new URL(link.href); route.searchParams.set('mode', current.mode); link.href = route;
    }
    for (const link of document.querySelectorAll('[data-mode]')) {
      link.setAttribute('aria-current', String(link.dataset.mode === current.mode));
      const route = new URL(link.href); route.searchParams.set('tree', current.tree);
      if (current.q) route.searchParams.set('q', current.q); else route.searchParams.delete('q');
      link.href = route;
    }
    for (const reading of document.querySelectorAll('[data-reading]')) reading.hidden = current.mode !== 'reading';
    for (const diagram of document.querySelectorAll('[data-diagram]')) diagram.hidden = current.mode !== 'diagram';
    input.value = current.q;
    searchTree();
    document.title = current.view === 'reasoning' ? `${treeTitles[current.tree]} · Reason Commons` : current.view === 'record' ? 'About the record · Reason Commons' : 'See the thinking · Reason Commons';
    if (current.item && items.has(current.item)) openItem(current.item);
    else if (dialog.open) { closeFromRoute = true; dialog.close(); activeItem = null; }
    else if (current.item) toast('That item is not in this public selection.');
  }

  function relatedHTML(item) {
    const tree = data.trees[item.tree];
    if (item.isLink) {
      return [...item.from, item.to].map(id => `<a href="${escape(itemURL(id))}" data-item="${id}"><span>${item.from.includes(id) ? 'Source statement' : 'Target statement'}</span>${escape(items.get(id).text)}</a>`).join('');
    }
    const links = tree.links.filter(link => link.to === item.id || link.from.includes(item.id));
    if (!links.length) return '<p>No accepted connections in this published selection. The statement stays separate.</p>';
    return links.map(link => {
      const other = link.to === item.id ? link.from.map(id => items.get(id).text).join(' AND ') : items.get(link.to).text;
      return `<a href="${escape(itemURL(link.id))}" data-item="${link.id}"><span>${link.to === item.id ? 'Incoming' : 'Outgoing'} accepted connection · ${relations[link.relation]}</span>${escape(other)}</a>`;
    }).join('');
  }

  function briefFor(item) {
    const wording = item.isLink ? `${item.from.map(id => items.get(id).text).join('\nAND\n')}\n${relations[item.relation]}\n${items.get(item.to).text}` : item.text;
    return `I am exploring the Reason Commons demonstration. Help me develop a contribution about this specific ${item.isLink ? 'connection' : 'statement'}.\n\nProject: ${data.title}\nPublic release: ${data.release_id}; snapshot prepared ${data.snapshot_date}\nItem: ${item.id}\nStanding in this release: accepted for now\nAccepted by: ${item.accepted_by.join(' and ')}\n\n${wording}\n\nPublic context: ${itemURL(item.id).href}\n\nUse the reason-commons skill if available. First establish my identity and the current authorized working state. Treat this public snapshot as historical context, and check whether the item has changed before proposing any shared edits. Help me formulate an observation, question, or challenge without assuming I endorse this item or have shared editing access. If shared state is unavailable, prepare a draft I can retain. Nothing has been submitted by copying this brief.`;
  }

  function openItem(id) {
    if (activeItem === id && dialog.open) return;
    const item = items.get(id);
    activeItem = id;
    const kind = item.isLink ? `Connection · ${relations[item.relation]}` : kinds[item.kind];
    const statement = item.isLink ? `<div class="detail-connection">${item.from.length > 1 ? '<p class="joint-label">All source statements act together (AND).</p>' : ''}${item.from.map(source => `<p class="detail-statement">${escape(items.get(source).text)}</p>`).join('<p class="joint-label">AND</p>')}<p class="relation-word">${relations[item.relation]} ↓</p><p class="detail-statement">${escape(items.get(item.to).text)}</p></div>` : `<p class="detail-statement">${escape(item.text)}</p>`;
    const brief = briefFor(item);
    details.innerHTML = `<div class="detail-meta"><span class="item-kind">${escape(treeTitles[item.tree])}<br>${escape(kind)}</span><span class="standing">✓ Accepted for now</span></div><h2 id="detail-heading" class="sr-only">${escape(kind)} details</h2>${statement}<dl class="provenance"><div><dt>Accepted by</dt><dd>${escape(item.accepted_by.join(' and '))}</dd></div><div><dt>Contribution</dt><dd>${escape(item.contributors.map(c => c.name).join(' · '))}</dd></div><div><dt>Recorded context</dt><dd>${escape(item.acceptance_context)}</dd></div></dl><div class="detail-share"><button type="button" class="secondary" data-copy-link>Copy item link ↗</button><a class="secondary" href="?view=reasoning&amp;tree=${item.tree}&amp;mode=diagram#reasoning" data-route>View this perspective</a></div><section class="detail-section"><h3>${item.isLink ? 'The statements this connects' : 'Connections in this selection'}</h3><div class="detail-relationships">${relatedHTML(item)}</div></section><section class="detail-section"><span class="eyebrow">Bring a contribution to your AI</span><h3>Start with this exact context</h3><p>Copy the brief into an AI conversation to develop a question, observation, or challenge. The skill should check the current working record first.</p><details><summary class="text-link">Read or manually copy the brief</summary><pre class="brief" tabindex="0">${escape(brief)}</pre></details><div class="detail-share"><button type="button" class="button primary" data-copy-brief>Copy contribution brief</button><a class="text-link" href="/skills">Get the skill ↗</a></div><p class="copy-feedback" aria-live="polite"></p><p class="access-note">This page is read-only. Copying prepares a brief; it does not submit anything or grant access to the shared record. You can retain a draft if you cannot access a shared workspace.</p></section>`;
    document.title = `${kind} · Reason Commons`;
    if (!dialog.open) {
      previousFocus = document.activeElement;
      dialog.showModal();
    }
    dialog.scrollTop = 0;
    document.querySelector('.close-dialog').focus({preventScroll: true});
  }

  function toast(message) {
    const element = document.querySelector('#toast');
    element.textContent = message; element.classList.add('shown');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => element.classList.remove('shown'), 3500);
  }

  async function copy(text, status) {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text);
      if (status) status.textContent = 'Brief copied. Nothing has been submitted.';
      toast(status ? 'Brief copied' : 'Item link copied');
    } catch {
      if (status) status.textContent = 'Clipboard unavailable. Open the readable brief and copy it manually.';
      const disclosure = details.querySelector('details');
      disclosure.open = true;
      disclosure.scrollIntoView({behavior: 'auto', block: 'nearest'});
      if (!status) {
        const previous = details.querySelector('.manual-link'); if (previous) previous.remove();
        const paragraph = document.createElement('p'); paragraph.className = 'brief manual-link'; paragraph.textContent = text;
        details.querySelector('.detail-share').after(paragraph);
        toast('Select and copy the visible item link.');
      }
    }
  }

  function closeItem() {
    if (!dialog.open) return;
    if (routeOpenedDialog) { history.back(); routeOpenedDialog = false; }
    else setRoute({...current, item: null}, true);
  }

  async function start() {
    try {
      const embedded = document.querySelector('#public-record');
      if (!embedded) throw new Error('Public record unavailable');
      data = JSON.parse(embedded.textContent);
      if (data.projection_version !== 1) throw new Error('Unsupported public record');
      items = new Map();
      for (const [tree, content] of Object.entries(data.trees)) for (const [key, list] of Object.entries(content)) for (const item of list) {
        if (item.status !== 'accepted') throw new Error('Unexpected standing');
        items.set(item.id, {...item, tree, isLink: key === 'links'});
      }
      document.body.classList.add('enhanced');
      document.addEventListener('click', event => {
        const link = event.target.closest('a');
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
        if (link?.hasAttribute('data-item')) {
          const id = link.dataset.item;
          if (!items.has(id)) return;
          event.preventDefault();
          const wasOpen = dialog.open;
          setRoute({...current, item: id}, wasOpen);
          if (!wasOpen) routeOpenedDialog = true;
        } else if (link?.hasAttribute('data-route')) {
          event.preventDefault();
          const route = new URL(link.href);
          const query = route.searchParams;
          setRoute({view: query.get('view') || 'overview', tree: query.get('tree') || 'goal', mode: query.get('mode') || 'reading', q: query.get('q') || '', item: null});
          document.querySelector('.project-navigation').scrollIntoView({behavior: 'auto', block: 'start'});
        } else if (link?.hasAttribute('data-how')) {
          event.preventDefault();
          if (dialog.open) setRoute({...current, item: null}, true);
          document.querySelector('#how-it-works').scrollIntoView({behavior: 'auto', block: 'start'});
        }
        if (event.target.closest('[data-copy-link]')) copy(itemURL(activeItem).href);
        if (event.target.closest('[data-copy-brief]')) copy(briefFor(items.get(activeItem)), details.querySelector('.copy-feedback'));
      });
      input.addEventListener('input', () => setRoute({...current, q: input.value, item: null}, true));
      document.querySelector('.close-dialog').addEventListener('click', closeItem);
      dialog.addEventListener('cancel', event => { event.preventDefault(); closeItem(); });
      dialog.addEventListener('click', event => { if (event.target === dialog) {
        const rect = dialog.getBoundingClientRect();
        if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeItem();
      }});
      dialog.addEventListener('close', () => {
        activeItem = null;
        if (closeFromRoute) closeFromRoute = false;
        if (previousFocus && document.contains(previousFocus)) previousFocus.focus({preventScroll: true});
      });
      addEventListener('popstate', renderRoute);
      renderRoute();
      if (current.view !== 'overview' && !dialog.open) document.querySelector('.project-navigation').scrollIntoView({behavior: 'auto', block: 'start'});
    } catch (error) {
      document.body.classList.remove('enhanced');
      for (const element of document.querySelectorAll('[hidden]')) if (element.id !== 'search-empty') element.hidden = false;
      const notice = document.createElement('p'); notice.className = 'scope-notice';
      notice.textContent = 'Interactive views could not load. The complete generated reading record remains available on this page.';
      document.querySelector('.project-navigation').after(notice);
    }
  }
  start();
})();
