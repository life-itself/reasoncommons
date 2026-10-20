/* The clinic team alongside the story. Each beat reconstructs its exact
   knowledge state; no timed transcript and no duplicated inline scenes. */
(function () {
  'use strict';

  var D = window.SKILL_MARGIN;
  if (!D || !D.scenes) return;

  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* The Ashfield clinic, shared across the trilogy. A page can extend it. */
  var CAST = {
    sam:     { name: 'Sam Whitfield',    short: 'Sam',        role: 'Practice manager' },
    maria:   { name: 'Maria Costa',      short: 'Maria',      role: 'Front desk' },
    adeyemi: { name: 'Dr Funmi Adeyemi', short: 'Dr Adeyemi', role: 'Doctor' },
    tomasz:  { name: 'Tomasz Nowak',     short: 'Tomasz',     role: 'Triage nurse' },
    leila:   { name: 'Leila Haddad',     short: 'Leila',      role: 'Pharmacist' },
    skill:   { name: 'Reason Commons',   short: 'Reason Commons', role: 'The reason-commons skill' }
  };
  Object.keys(D.cast || {}).forEach(function (k) { CAST[k] = D.cast[k]; });

  /* How the team chat is invoked: `/reason` answers by default, records in
     capture mode, and `/reason-accept` endorses a displayed review. */
  var CMD = { capture: '/reason · capture', ask: '/reason · ask', review: '/reason · review',
              accept: '/reason-accept' };
  var MIC = '<svg viewBox="0 0 12 12" aria-hidden="true"><rect x="4" y="1" width="4" height="6.4" rx="2" ' +
    'fill="none" stroke="currentColor" stroke-width="1.2"/><path d="M2.4 5.6 C2.4 9.6 9.6 9.6 9.6 5.6 M6 8.6 L6 11" ' +
    'fill="none" stroke="currentColor" stroke-width="1.2"/></svg>';

  /* ---------- avatars ----------
     Drawn in the series' line style, one marker of role each, and run
     through a gentler version of the pages' rough filter. */
  var SPRITE =
    '<svg xmlns="' + NS + '" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' +
    '<filter id="sm-rough" x="-10%" y="-10%" width="120%" height="120%">' +
      '<feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="5" result="n"/>' +
      '<feDisplacementMap in="SourceGraphic" in2="n" scale="1.3" xChannelSelector="R" yChannelSelector="G"/></filter>' +
    '<clipPath id="sm-clip"><circle cx="24" cy="24" r="22.4"/></clipPath>' +
    av('sam',
      '<path d="M16.4 19 C15.8 10.6 32.2 10.6 31.6 19 C29.4 15.2 18.6 15.2 16.4 19Z" fill="var(--ink-soft)"/>',
      '<circle cx="21.2" cy="20.2" r="2.3" fill="none" stroke="var(--ink)" stroke-width="1.1"/>' +
      '<circle cx="26.8" cy="20.2" r="2.3" fill="none" stroke="var(--ink)" stroke-width="1.1"/>' +
      '<path d="M23.5 20.2 L24.5 20.2" stroke="var(--ink)" stroke-width="1.1"/>',
      '<path d="M19.6 33.4 L24 40 L28.4 33.4" fill="none" stroke="var(--skill)" stroke-width="1.3"/>' +
      '<rect x="22" y="39.6" width="4" height="5.2" rx=".6" fill="var(--paper)" stroke="var(--ink)" stroke-width="1"/>') +
    av('maria',
      '<circle cx="31.4" cy="12" r="3.7" fill="var(--ink-soft)"/>' +
      '<path d="M16.4 19.6 C15.6 11 32.4 11 31.6 19.6 C29.6 15.6 18.4 15.6 16.4 19.6Z" fill="var(--ink-soft)"/>',
      '',
      '<path d="M15.6 21.4 C15.4 9.4 32.6 9.4 32.4 21.4" fill="none" stroke="var(--ink)" stroke-width="1.6"/>' +
      '<rect x="13.9" y="18.6" width="3.2" height="5.6" rx="1.3" fill="var(--ink)"/>' +
      '<path d="M15.6 24 Q16.4 27.4 21 26.6" fill="none" stroke="var(--ink)" stroke-width="1.3"/>' +
      '<circle cx="21.4" cy="26.5" r=".9" fill="var(--ink)"/>') +
    av('adeyemi',
      '<path d="M16.3 19.4 C15 12.2 18.8 10.6 20.8 11.5 C22.4 9.8 25.6 9.8 27.2 11.5 C29.2 10.6 33 12.2 31.7 19.4 C29.2 15.8 18.8 15.8 16.3 19.4Z" fill="var(--ink)"/>',
      '',
      '<path d="M18.6 32.6 C17.4 38.6 20.8 41.4 24 41.4 C27.2 41.4 30.6 38.6 29.4 32.6" fill="none" stroke="var(--ink)" stroke-width="1.4"/>' +
      '<circle cx="24" cy="42.6" r="1.9" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.2"/>') +
    av('tomasz',
      '<path d="M16.6 18.4 C16.4 12 31.6 12 31.4 18.4 C29.4 15.8 18.6 15.8 16.6 18.4Z" fill="var(--ink-faint)"/>',
      '<path d="M16.8 21.6 C17.2 29.4 30.8 29.4 31.2 21.6 C29.4 25.2 18.6 25.2 16.8 21.6Z" fill="var(--ink-soft)"/>',
      '<path d="M20 33.4 L24 38 L28 33.4" fill="none" stroke="var(--ink)" stroke-width="1.3"/>' +
      '<path d="M31 35.4 L31 37.6" stroke="var(--ink)" stroke-width="1"/>' +
      '<circle cx="31" cy="39.4" r="1.9" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.1"/>', true) +
    av('leila',
      '<path d="M14.6 23.4 C13.6 9 34.4 9 33.4 23.4 C33.8 29.4 30 33 24 33.4 C18 33 14.2 29.4 14.6 23.4Z" fill="var(--skill-soft)" stroke="var(--ink)" stroke-width="1.5"/>',
      '', '<rect x="28.6" y="37" width="5" height="7" rx="1" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.1"/>' +
      '<path d="M28.2 37 L34 37" stroke="var(--ink)" stroke-width="1.6"/>', false, 6.6) +
    '<symbol id="sm-av-skill" viewBox="0 0 48 48"><g filter="url(#sm-rough)">' +
      '<rect x="4.5" y="4.5" width="39" height="39" rx="10" fill="var(--skill-soft)" stroke="var(--skill)" stroke-width="1.6"/>' +
      '<path d="M24 18.4 L24 23.6 M16 29 L16 23.6 L32 23.6 L32 29" fill="none" stroke="var(--skill)" stroke-width="1.5"/>' +
      '<rect x="18.6" y="11" width="10.8" height="7.4" rx="1.2" fill="var(--paper)" stroke="var(--skill)" stroke-width="1.5"/>' +
      '<rect x="10.6" y="29" width="10.8" height="7.4" rx="1.2" fill="var(--paper)" stroke="var(--skill)" stroke-width="1.5"/>' +
      '<rect x="26.6" y="29" width="10.8" height="7.4" rx="1.2" fill="var(--paper)" stroke="var(--skill)" stroke-width="1.5"/>' +
    '</g></symbol>' +
    '</defs></svg>';

  /* One person: a circle, shoulders, a head, and whatever marks them out.
     `back` sits behind the head (hair, a bun, a scarf), `face` on it,
     `front` on the chest or over the head. */
  function av(id, back, face, front, noSmile, headR) {
    var r = headR || 7.6;
    return '<symbol id="sm-av-' + id + '" viewBox="0 0 48 48"><g filter="url(#sm-rough)">' +
      '<circle cx="24" cy="24" r="22.4" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.4"/>' +
      '<g clip-path="url(#sm-clip)">' +
        '<path d="M8.6 47 C8.6 34.2 39.4 34.2 39.4 47Z" fill="var(--paper-2)" stroke="var(--ink)" stroke-width="1.5"/>' +
        '<path d="M21.4 27.4 L21.4 31 M26.6 27.4 L26.6 31" stroke="var(--ink)" stroke-width="1.4"/>' +
        back +
        '<circle cx="24" cy="20.4" r="' + r + '" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>' +
        '<circle cx="21.3" cy="20.2" r=".95" fill="var(--ink)"/><circle cx="26.7" cy="20.2" r=".95" fill="var(--ink)"/>' +
        (noSmile ? '' : '<path d="M21.9 23.6 Q24 25.1 26.1 23.6" fill="none" stroke="var(--ink)" stroke-width="1.1"/>') +
        face + front +
      '</g></g></symbol>';
  }

  function avatar(id, cls) {
    return '<svg class="sm-av' + (cls ? ' ' + cls : '') + '" viewBox="0 0 48 48" aria-hidden="true">' +
      '<use href="#sm-av-' + id + '"/></svg>';
  }

  /* Scroll is the editorial clock. A beat is the complete state of the
     companion, not the start of a timed transcript. Future messages are
     never mounted, and reverse scrolling reconstructs the earlier state. */
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function fmt(s) {
    return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*([^*]+)\*/g, '<em>$1</em>');
  }
  function nodes(list) {
    return '<div class="sm-nodes">' + list.map(function (n) {
      return (n.via ? '<span class="sm-via">↓ ' + esc(n.via) + '</span>' : '') +
        '<div class="sm-node s-' + n.s.toLowerCase() + (n.mark ? ' mark' : '') + '">' +
        '<span class="sm-k">[' + esc(n.s) + '] · ' + esc(n.k) + '</span>' + fmt(n.t) + '</div>';
    }).join('') + '</div>';
  }
  function message(m, previous) {
    var p = CAST[m.from];
    return '<div class="sm-msg' + (m.from === 'skill' ? ' skill' : '') + (previous ? ' previous' : ' latest') + '" data-from="' + esc(m.from) + '">' +
      avatar(m.from) + '<div class="sm-bub"><span class="sm-name">' + esc(p.short) + '</span>' +
      (m.type ? '<span class="sm-type">' + esc(m.type) + '</span>' : '') +
      (m.dictated ? '<span class="sm-dict">' + MIC + 'Dictated</span>' : '') +
      (m.cmd ? '<code class="sm-cmd">' + esc(CMD[m.cmd] || m.cmd) + '</code> ' : '') +
      fmt(m.text) + (m.nodes ? nodes(m.nodes) : '') + '</div></div>';
  }
  function castStrip(focus) {
    return '<div class="sm-roster" aria-label="The people in this example">' +
      ['sam', 'maria', 'tomasz', 'adeyemi', 'leila', 'skill'].map(function (id) {
        return '<span class="sm-person' + (focus.indexOf(id) !== -1 ? ' active' : '') + '" title="' + esc(CAST[id].name + ' · ' + CAST[id].role) + '">' + avatar(id) + '<span>' + esc(id === 'skill' ? 'Skill' : CAST[id].short) + '</span></span>';
      }).join('') + '</div>';
  }
  function capacityBoard(n, focus) {
    var stations = [['Check-in', 60, 'maria'], ['Triage', 45, 'tomasz'], ['Doctor', 20, 'adeyemi'], ['Pharmacy', 50, 'leila'], ['Follow-up', 40, 'maria']];
    return '<div class="sm-capacities" aria-label="Daily capacities introduced so far">' + stations.map(function (s, i) {
      return '<div class="' + (i < n ? 'known' : 'unknown') + (focus.indexOf(s[2]) !== -1 && i < n ? ' active' : '') + '"><span>' + s[0] + '</span><b>' + (i < n ? s[1] : '—') + '</b></div>';
    }).join('') + '</div><p class="sm-unit">People per day · as introduced in the story</p>';
  }
  function castView(b) {
    var focus = b.focus || [];
    return '<div class="sm-cast-view"><p class="sm-context">' + fmt(b.text || D.cover.text) + '</p>' +
      '<p class="sm-focusline">' + focus.filter(function (k) { return k !== 'skill'; }).map(function (k) { return esc(CAST[k].name + ' · ' + CAST[k].role); }).join('<br>') + '</p>' +
      '<ul class="sm-cast">' + ['sam', 'maria', 'tomasz', 'adeyemi', 'leila', 'skill'].map(function (id) {
        return '<li class="' + (focus.indexOf(id) !== -1 ? 'active' : '') + '">' + avatar(id) + '<div><b>' + esc(CAST[id].name) + '</b><span>' + esc(CAST[id].role) + (id === 'skill' ? ' · invited later' : '') + '</span></div></li>';
      }).join('') + '</ul>' + (b.capacities != null ? capacityBoard(b.capacities, focus) : '') + '</div>';
  }
  function introView(b) {
    return '<div class="sm-intro">' + avatar('skill') + '<p class="sm-invite">Reason Commons joins<br>the conversation</p><p class="sm-context">' + fmt(b.text) + '</p><p class="sm-intro-note">The people bring the questions.<br>The skill helps keep the reasoning.</p></div>';
  }
  function conversation(b) {
    var s = D.scenes.filter(function (x) { return x.id === b.scene; })[0];
    var visible = s.msgs.slice(Math.max(0, b.count - 2), b.count);
    var newest = s.msgs[b.count - 1];
    var notification = s.notify && b.count === 1;
    var who = CAST[s.who];
    var thread = '<div class="sm-thread">' + visible.map(function (m, i) { return message(m, i < visible.length - 1); }).join('') + '</div>';
    var device;
    if (s.device === 'phone') {
      var body = notification
        ? '<div class="sm-lock"><span class="sm-clock">' + esc(s.clock || '08:30') + '</span><div class="sm-note"><span class="sm-note-app">' + avatar(newest.from) + 'Team chat · now</span><b>' + esc(CAST[newest.from].short) + '</b><p>' + fmt(newest.text) + '</p></div><span class="sm-lock-hint">A colleague asks for ' + esc(who.short) + '’s input</span></div>'
        : '<div class="sm-apphead">' + esc(D.channel || '#ashfield-flow') + ' <span>Chat prototype</span></div>' + thread;
      device = '<div class="sm-phone' + (notification ? ' notified' : '') + '"><div class="sm-notch"></div><div class="sm-screen">' + body + '</div></div>';
    } else {
      device = '<div class="sm-monitor"><div class="sm-win"><div class="sm-bar"><i></i><i></i><i></i><span>AI assistant · skill installed</span></div>' + thread + '</div><div class="sm-neck"></div><div class="sm-foot"></div></div>';
    }
    return '<div class="sm-conversation"><div class="sm-who">' + avatar(s.who) + '<div><b>' + esc(who.name) + '</b><span>' + esc(who.role + ' · ' + s.place) + '</span></div><span class="sm-surface">' + (s.device === 'phone' ? 'Phone' : 'Desktop') + '</span></div>' +
      '<div class="sm-device" data-device="' + s.device + '">' + device + '</div>' +
      '<p class="sm-receipt">' + (notification ? 'Notification · scroll to follow the reply' : 'Message ' + b.count + ' of ' + s.msgs.length + ' · ' + esc(s.time)) + '</p>' +
      (b.note ? '<p class="sm-diff">' + fmt(b.note) + '</p>' : '') + '</div>';
  }
  function closeView() {
    return '<div class="sm-close"><p class="sm-context">' + fmt(D.close.text) + '</p><p class="sm-prompt"><span>Try one real question</span>“Here is what keeps happening.<br>Help me check my explanation.”</p><code class="sm-install">' + esc(D.close.install) + '</code><div class="sm-links">' + D.close.links.map(function (l) { return '<a href="' + esc(l.href) + '">' + esc(l.text) + '</a>'; }).join('') + '</div><p class="sm-fine">Illustrated example. The people and messages are invented. Phone chat is a prototype; install the skill in your AI assistant.</p></div>';
  }

  var beats = D.beats.map(function (b) {
    b.el = b.step ? document.querySelector('.trigger[data-t="' + b.step + '"]') : document.querySelector('[data-sm-beat="' + b.at + '"]');
    if (!b.el) throw new Error('Missing margin beat: ' + (b.step || b.at));
    return b;
  });
  var rail = document.createElement('aside');
  rail.className = 'sm-rail';
  rail.setAttribute('aria-label', 'The clinic team, alongside the story');
  rail.innerHTML = '<div class="sm-head"><span>Alongside the story</span><span class="sm-tools"><a href="' + esc(D.original) + '">Original</a><button class="sm-hide" type="button" aria-label="Hide the skill margin">Hide</button></span></div><div class="sm-roster-slot"></div><div class="sm-stage"></div><p class="sm-follow">Illustrated example · scroll to follow the team</p>';
  document.body.insertAdjacentHTML('afterbegin', SPRITE);
  document.body.appendChild(rail);
  document.body.classList.add('sm-on');
  var stage = rail.querySelector('.sm-stage');
  var roster = rail.querySelector('.sm-roster-slot');
  var tab = document.createElement('button');
  tab.type = 'button'; tab.className = 'sm-tab'; tab.textContent = 'Show the team';
  document.body.appendChild(tab);
  function collapse(on) {
    document.body.classList.toggle('sm-collapsed', on);
    rail.inert = on;
    try { localStorage.setItem('sm-collapsed', on ? '1' : '0'); } catch (e) {}
    if (typeof window.fitPortrait === 'function') window.fitPortrait();
    update();
  }
  rail.querySelector('.sm-hide').addEventListener('click', function () { collapse(true); tab.focus(); });
  tab.addEventListener('click', function () { collapse(false); rail.querySelector('.sm-hide').focus(); });
  try {
    if (localStorage.getItem('sm-collapsed') === '1') {
      document.body.classList.add('sm-collapsed');
      rail.inert = true;
    }
  } catch (e) {}

  var current = -2;
  function render(index) {
    if (index === current) return;
    var forward = index > current;
    current = index;
    var b = index >= 0 ? beats[index] : D.opening;
    var s = b.scene ? D.scenes.filter(function (x) { return x.id === b.scene; })[0] : null;
    var focus = b.focus || (s ? [s.msgs[b.count - 1].from] : []);
    roster.innerHTML = castStrip(focus);
    rail.dataset.mode = b.mode;
    rail.dataset.beat = b.step || b.at || 'opening';
    stage.innerHTML = '<div class="sm-scene' + (forward && !reduce ? ' sm-arrive' : '') + '"><p class="sm-chapter">' + esc(b.chapter || '') + '</p><h2>' + esc(b.title || '') + '</h2>' +
      (b.mode === 'cast' ? castView(b) : b.mode === 'intro' ? introView(b) : b.mode === 'close' ? closeView() : conversation(b)) + '</div>';
    rail.dataset.message = b.count || '0';
  }

  /* Reconcile the main drawing from its own trigger geometry too. This
     prevents IntersectionObserver delivery order leaving an old caption
     behind after a large jump or a reversal. Shared scroller.js is intact. */
  var steps = [].slice.call(document.querySelectorAll('.step'));
  var layers = [].slice.call(document.querySelectorAll('.layer'));
  var triggers = [].slice.call(document.querySelectorAll('.trigger'));
  var storyId = '';
  var originalStep = window.onStep;
  function syncStory(id) {
    if (!id || storyId === id) return;
    storyId = id;
    steps.forEach(function (e) { e.classList.toggle('on', e.dataset.step === id); });
    layers.forEach(function (e) { e.classList.toggle('on', e.dataset.layer.split(/\s+/).indexOf(id) !== -1); });
    [].forEach.call(document.querySelectorAll('.steps.stack'), function (g) {
      var seen = false;
      for (var i = g.children.length - 1; i >= 0; i--) {
        var e = g.children[i];
        if (e.dataset.step === id) seen = true;
        e.classList.toggle('on', seen); e.classList.toggle('cur', e.dataset.step === id);
      }
    });
    if (typeof originalStep === 'function') originalStep(id);
    if (typeof window.fitPortrait === 'function') window.fitPortrait();
  }
  var ticking = false;
  function update() {
    ticking = false;
    var line = innerHeight * 0.55;
    var picked = -1;
    for (var i = 0; i < beats.length; i++) {
      if (beats[i].el.getBoundingClientRect().top <= line) picked = i;
    }
    var activeTrigger = null;
    triggers.forEach(function (t) {
      var section = t.closest('.scroll-item').getBoundingClientRect();
      if (section.top <= line && section.bottom > line && t.getBoundingClientRect().top <= line) activeTrigger = t;
    });
    if (activeTrigger) syncStory(activeTrigger.dataset.t);
    render(picked);
  }
  function schedule() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  function observedStep() {
    /* The shared observer may fire after the scroll frame. Reconcile from
       geometry rather than accepting a stale entry from a skipped trigger. */
    storyId = ''; schedule();
  }
  window.onStep = observedStep;
  window.addEventListener('scroll', schedule, { passive: true });
  var portrait = window.matchMedia('(max-width: 640px)').matches;
  var lastWidth = innerWidth;
  window.addEventListener('resize', function () {
    var nextPortrait = window.matchMedia('(max-width: 640px)').matches;
    if (portrait !== nextPortrait && typeof window.rebuildExplainerArtwork === 'function') {
      window.rebuildExplainerArtwork();
      layers = [].slice.call(document.querySelectorAll('.layer'));
      originalStep = window.onStep;
      window.onStep = observedStep;
      portrait = nextPortrait;
    }
    /* Keep the reading beat when a window changes width. Height-only changes
       (including a phone's browser toolbar) leave ordinary scrolling alone. */
    if (lastWidth !== innerWidth && current >= 0) {
      var top = beats[current].el.getBoundingClientRect().top + scrollY - innerHeight * 0.5;
      window.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
    }
    lastWidth = innerWidth;
    storyId = '';
    schedule();
  });
  window.addEventListener('load', schedule);
  if (document.fonts) document.fonts.ready.then(function () { storyId = ''; schedule(); });
  update();
})();
