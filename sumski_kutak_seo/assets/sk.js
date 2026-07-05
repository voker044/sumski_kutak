/* Šumski Kutak — statičke interakcije (bez framework-a) */
(function () {
  'use strict';

  /* ---------- Header: pozadina pri skrolu ---------- */
  var header = document.querySelector('header.fixed');
  var SCROLLED = ['bg-background/85', 'backdrop-blur-xl', 'border-b', 'border-border'];
  function onScroll() {
    if (!header) return;
    var on = (window.scrollY || 0) > 24;
    SCROLLED.forEach(function (c) { header.classList.toggle(c, on); });
    header.classList.toggle('bg-transparent', !on);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Zaključavanje skrola za overlaye ---------- */
  function lockScroll(on) { document.documentElement.style.overflow = on ? 'hidden' : ''; }

  /* ---------- Mobilni meni ---------- */
  var mmBtn = document.querySelector('header button[aria-label="Meni"]');
  var mm = null;
  function closeMM() { if (mm) { mm.remove(); mm = null; lockScroll(false); if (mmBtn) mmBtn.setAttribute('aria-expanded', 'false'); } }
  function openMM() {
    if (mm) return;
    var links = [];
    document.querySelectorAll('header nav a').forEach(function (a) {
      links.push({ href: a.getAttribute('href'), label: a.textContent.trim(), active: a.getAttribute('aria-current') === 'page' });
    });
    mm = document.createElement('div');
    mm.id = 'sk-mm';
    mm.setAttribute('role', 'dialog');
    mm.setAttribute('aria-modal', 'true');
    mm.setAttribute('aria-label', 'Navigacija');
    var html = '<button id="sk-mm-x" aria-label="Zatvori meni">&#10005;</button><nav>';
    links.forEach(function (l, i) {
      html += '<a href="' + l.href + '"' + (l.active ? ' class="active" aria-current="page"' : '') + ' style="animation-delay:' + (0.06 + i * 0.05) + 's">' + l.label + '</a>';
    });
    html += '</nav><div class="sk-mm-cta"><a href="/kontakt" style="animation-delay:.4s">Rezervacija</a><p style="animation-delay:.45s">060 739 9978 &middot; 060 739 9979</p></div>';
    mm.innerHTML = html;
    document.body.appendChild(mm);
    lockScroll(true);
    if (mmBtn) mmBtn.setAttribute('aria-expanded', 'true');
    mm.querySelector('#sk-mm-x').addEventListener('click', closeMM);
    mm.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMM); });
  }
  if (mmBtn) mmBtn.addEventListener('click', function () { mm ? closeMM() : openMM(); });

  /* ---------- Lightbox (galerija + meni slike) ---------- */
  var lb = null;
  function closeLB() { if (lb) { lb.remove(); lb = null; lockScroll(false); } }
  function openLB(src, alt) {
    closeLB();
    lb = document.createElement('div');
    lb.id = 'sk-lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', alt || 'Uvećana slika');
    lb.innerHTML = '<button id="sk-lb-x" aria-label="Zatvori">&#10005;</button>' +
      '<figure><img src="' + src + '" alt="' + (alt || '').replace(/"/g, '&quot;') + '"/>' +
      (alt ? '<figcaption>' + alt + '</figcaption>' : '') + '</figure>';
    document.body.appendChild(lb);
    lockScroll(true);
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.id === 'sk-lb-x') closeLB(); });
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('button[aria-label^="Uvećaj sliku"], button[aria-label^="Pogledaj "]');
    if (!btn) return;
    var img = btn.querySelector('img');
    if (img) openLB(img.currentSrc || img.src, img.alt);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeLB(); closeMM(); }
  });

  /* ---------- Preporuka pića (meni) ---------- */
  document.querySelectorAll('button[aria-expanded]').forEach(function (btn) {
    var panel = btn.parentElement && btn.parentElement.querySelector('.sk-pair');
    if (!panel) return;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
      for (var i = btn.childNodes.length - 1; i >= 0; i--) {
        if (btn.childNodes[i].nodeType === 3 && btn.childNodes[i].nodeValue.trim()) {
          btn.childNodes[i].nodeValue = open ? 'Preporuči piće' : 'Sakrij preporuku';
          break;
        }
      }
    });
  });

  /* ---------- Reveal animacije pri skrolu (samo ispod prvog ekrana) ---------- */
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    var targets = document.querySelectorAll(
      'main h2, main .group.overflow-hidden.border-border, main figure, #sk-faq details, main section .rounded-sm.border.border-border'
    );
    var seen = new Set();
    var toObserve = [];
    var fold = window.innerHeight * 0.9;
    targets.forEach(function (el) {
      if (seen.has(el)) return;
      seen.add(el);
      if (el.getBoundingClientRect().top > fold) { el.classList.add('sk-reveal'); toObserve.push(el); }
    });
    if (toObserve.length) {
      var io = new IntersectionObserver(function (entries) {
        var batch = 0;
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          el.style.transitionDelay = Math.min(batch * 70, 350) + 'ms';
          el.classList.add('sk-in');
          io.unobserve(el);
          batch++;
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
      toObserve.forEach(function (el) { io.observe(el); });
    }
  }
})();
