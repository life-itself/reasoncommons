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

  function show(id) {
    if (!id) return;
    for (var i = 0; i < steps.length; i++) {
      steps[i].classList.toggle('on', steps[i].dataset.step === id);
    }
    for (var j = 0; j < layers.length; j++) {
      var keys = (layers[j].dataset.layer || '').split(/\s+/);
      layers[j].classList.toggle('on', keys.indexOf(id) !== -1);
    }
    if (typeof window.onStep === 'function') window.onStep(id);
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

  // first step visible before any scroll
  var first = document.querySelector('.trigger');
  if (first) show(first.dataset.t);
})();
