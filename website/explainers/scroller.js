/* ============================================================
   Shared scroller engine — the LTP explainer series
   Pure IntersectionObserver step machinery. No scrolljacking,
   no scroll listeners for positioning (that's CSS position:sticky).

   Markup contract per section:
     <section class="scroll-item">
       <div class="sticky-item"><div class="stage">
         <svg>… <g class="layer" data-layer="ID">…</g> …</svg>
         <div class="steps"><div class="step" data-step="ID"><p>…</p></div></div>
       </div></div>
       <div class="trigger" data-t="ID"></div>   <!-- one per step -->
     </section>

   Optional per-step hook: window.onStep = (id) => {…}
   ============================================================ */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var steps  = [].slice.call(document.querySelectorAll('.step'));
  var layers = [].slice.call(document.querySelectorAll('.layer'));

  var stacks = [].slice.call(document.querySelectorAll('.steps.stack'));

  /* A stacked group accumulates instead of replacing: every block up to and
     including the live one stays on screen, the live one marked .cur and the
     rest dimmed by CSS. Membership is read from DOM order, so no bookkeeping
     against the triggers is needed — if the active id belongs to some other
     section, the whole group clears. */
  function stack(group, id) {
    var kids = group.children, seen = false;
    for (var i = kids.length - 1; i >= 0; i--) {
      var k = kids[i];
      if (k.dataset.step === id) seen = true;
      k.classList.toggle('on', seen);
      k.classList.toggle('cur', k.dataset.step === id);
    }
  }

  function show(id) {
    if (!id) return;
    for (var i = 0; i < steps.length; i++) {
      steps[i].classList.toggle('on', steps[i].dataset.step === id);
    }
    for (var s = 0; s < stacks.length; s++) stack(stacks[s], id);
    for (var j = 0; j < layers.length; j++) {
      var keys = (layers[j].dataset.layer || '').split(/\s+/);
      layers[j].classList.toggle('on', keys.indexOf(id) !== -1);
    }
    if (typeof window.onStep === 'function') window.onStep(id);
    fitPortrait();
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) show(e.target.dataset.t);
    });
  }, { rootMargin: '-45% 0px -45% 0px' });

  [].forEach.call(document.querySelectorAll('.trigger'), function (t) { io.observe(t); });

  // progress rule
  var bar = document.querySelector('.progress');
  if (bar) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var max = document.body.scrollHeight - window.innerHeight;
        bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
        ticking = false;
      });
    }, { passive: true });
  }

  /* The bar stays out of the hero's way and appears once the hero has left,
     so the reader always has a name for where they are and a way back. */
  var nav = document.querySelector('.topnav'), hero = document.querySelector('.hero');
  if (nav && hero) {
    new IntersectionObserver(function (entries) {
      nav.classList.toggle('on', !entries[0].isIntersecting);
    }, { threshold: 0 }).observe(hero);
  } else if (nav) {
    nav.classList.add('on');
  }

  /* The page has to say that it scrolls. Once it has been scrolled, it has
     made its point and gets out of the way. */
  var cue = document.querySelector('.scrollcue');
  if (cue) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > window.innerHeight * 0.3) cue.classList.add('gone');
    }, { passive: true });
  }

  /* Count a number up as it lands. Respects reduced motion. */
  window.countUp = function (el, to, ms) {
    if (!el || el.dataset.counted === '1') return;
    el.dataset.counted = '1';
    if (reduce) { el.textContent = to; return; }
    var v = 0, step = Math.max(1, Math.round(to / 24));
    var t = setInterval(function () {
      v = Math.min(to, v + step);
      el.textContent = v;
      if (v >= to) clearInterval(t);
    }, (ms || 900) / 24);
  };

  /* ---------- portrait fit ----------
     These drawings are laid out landscape: 700–900 user units across, dropped
     into a 390px phone, which renders a 13px label at 6px. Each page gives its
     wider compositions a narrower portrait arrangement of its own; on top of
     that, this zooms each stage to whatever is actually showing at the current
     step and parks it in the upper band, leaving the foot clear for the
     caption. A drawing that wants to be left alone sets data-no-fit.

       BAND   fraction of the viewport height the drawing may occupy
       ANCHOR where the drawing's centre sits, as a fraction of the height  */
  var BAND = 0.62, ANCHOR = 0.32, PAD = 0.06;
  var DRAWABLE = 'rect,circle,ellipse,line,path,polyline,polygon,text,image';

  function hidden(el, root) {
    for (var n = el; n && n !== root; n = n.parentNode) {
      if (n.getAttribute && n.getAttribute('opacity') === '0') return true;
      if (n.classList && n.classList.contains('layer') && !n.classList.contains('on')) return true;
    }
    return false;
  }

  /* Union of what is currently visible, in the svg's own user space — so it is
     unaffected by whatever viewBox a previous step left behind. */
  function visibleBox(svg) {
    var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    var root;
    try { root = svg.getScreenCTM(); } catch (e) { return null; }
    if (!root) return null;
    var toUser = root.inverse();
    [].forEach.call(svg.querySelectorAll(DRAWABLE), function (el) {
      if (hidden(el, svg)) return;
      var b, m;
      // element user space → root user space, via the screen and back, so the
      // result doesn't depend on the viewBox we are about to replace
      try { b = el.getBBox(); m = toUser.multiply(el.getScreenCTM()); } catch (e) { return; }
      if (!b || (!b.width && !b.height) || !m) return;
      [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height],
       [b.x + b.width, b.y + b.height]].forEach(function (p) {
        var px = m.a * p[0] + m.c * p[1] + m.e, py = m.b * p[0] + m.d * p[1] + m.f;
        if (px < x0) x0 = px; if (px > x1) x1 = px;
        if (py < y0) y0 = py; if (py > y1) y1 = py;
      });
    });
    if (!isFinite(x0) || x1 <= x0 || y1 <= y0) return null;
    return { x: x0, y: y0, width: x1 - x0, height: y1 - y0 };
  }

  function fitPortrait() {
    if (!window.matchMedia('(max-width: 640px)').matches) return;
    [].forEach.call(document.querySelectorAll('.sticky-item .stage svg'), function (svg) {
      if (svg.hasAttribute('data-no-fit')) return;
      var rect = svg.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      var bb = visibleBox(svg);
      if (!bb) return;

      var cw = bb.width * (1 + PAD * 2), ch = bb.height * (1 + PAD * 2);
      // the scale that fits what's showing into the band, capped so a single
      // small element doesn't blow up into a poster
      var s = Math.min(rect.width / cw, (rect.height * BAND) / ch, 1.6);
      var vbW = rect.width / s, vbH = rect.height / s;

      svg.setAttribute('viewBox', [
        (bb.x + bb.width / 2) - vbW / 2,
        (bb.y + bb.height / 2) - (rect.height * ANCHOR) / s,
        vbW, vbH
      ].map(function (n) { return Math.round(n * 100) / 100; }).join(' '));
    });
  }

  /* Content is drawn by each page's own inline script, which runs after this
     one, so measure on load rather than now. */
  window.addEventListener('load', fitPortrait);
  var rt;
  window.addEventListener('resize', function () {
    clearTimeout(rt); rt = setTimeout(fitPortrait, 200);
  });
  window.fitPortrait = fitPortrait;

  // first step visible before any scroll
  var first = document.querySelector('.trigger');
  if (first) show(first.dataset.t);
})();
