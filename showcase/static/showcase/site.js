(() => {
  'use strict';
  const translations = JSON.parse(document.getElementById('editorial-translations').textContent);
  let language = document.documentElement.lang;
  const menu = document.getElementById('mobile-menu');
  const menuToggle = document.getElementById('menu-toggle');
  const menuClose = document.getElementById('menu-close');
  const modal = document.getElementById('preview-modal');
  const triggers = [...document.querySelectorAll('[data-preview-index]')];
  const modalImage = document.getElementById('preview-modal-img');
  const modalLabel = document.getElementById('preview-modal-label');
  const dots = document.getElementById('preview-modal-dots');
  let currentIndex = 0;
  let returnFocus = null;
  let menuReturnFocus = null;
  const translated = key => translations[language][key] || '';

  function renderGallery() {
    if (!triggers.length) return;
    const current = triggers[currentIndex];
    const image = current.querySelector('img');
    const caption = current.closest('figure').querySelector('figcaption').textContent;
    modalImage.src = image.src;
    modalImage.alt = image.alt;
    modalLabel.textContent = caption;
    document.getElementById('preview-modal-position').textContent = `${currentIndex + 1} / ${triggers.length}`;
    [...dots.children].forEach((dot, index) => {
      dot.setAttribute('aria-current', String(index === currentIndex));
      dot.setAttribute('aria-label', `${translated('preview.open')}: ${triggers[index].closest('figure').querySelector('figcaption').textContent}`);
    });
  }

  function setLanguage(next, persist = true) {
    if (!translations[next]) return;
    language = next;
    document.documentElement.lang = next;
    document.querySelectorAll('[data-i18n]').forEach(node => {
      if (translations[next][node.dataset.i18n] !== undefined) node.textContent = translated(node.dataset.i18n);
    });
    document.querySelectorAll('[data-i18n-alt]').forEach(node => { node.alt = translated(node.dataset.i18nAlt); });
    document.querySelectorAll('[data-i18n-aria]').forEach(node => { node.setAttribute('aria-label', translated(node.dataset.i18nAria)); });
    const title = translated('hero.title').replace(/^YemX\s+/, '');
    const suffix = next === 'fr' ? 'des commerçants.' : 'for merchants.';
    const matched = title.endsWith(suffix);
    document.querySelector('[data-hero="lead"]').textContent = matched ? title.slice(0, -suffix.length).trimEnd() : title;
    document.querySelector('[data-hero="emphasis"]').textContent = matched ? suffix : '';
    document.querySelector('meta[name="description"]').content = translated('hero.subtitle');
    document.querySelectorAll('[data-language]').forEach(node => {
      node.classList.toggle('active', node.dataset.language === next);
      node.setAttribute('aria-current', String(node.dataset.language === next));
    });
    triggers.forEach(node => { node.setAttribute('aria-label', `${translated('preview.open')}: ${node.closest('figure').querySelector('figcaption').textContent}`); });
    renderGallery();
    if (persist) {
      try { localStorage.setItem('yemx-lang', next); } catch (_) { /* Cookies still preserve the choice when storage is unavailable. */ }
      document.cookie = `yemx-lang=${next}; Path=/; Max-Age=31536000; SameSite=Lax${location.protocol === 'https:' ? '; Secure' : ''}`;
    }
  }

  document.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      setLanguage(link.dataset.language);
      const url = new URL(location.href);
      url.searchParams.set('lang', language);
      history.replaceState(null, '', url);
    });
  });

  const inertTargets = [...document.body.children].filter(node => ![menu, modal].includes(node) && node.tagName !== 'SCRIPT');
  function closeMenu(restore = true) {
    menu.classList.remove('open');
    menu.hidden = true;
    menuToggle.setAttribute('aria-expanded', 'false');
    inertTargets.forEach(node => { node.inert = false; });
    document.body.classList.remove('scroll-locked');
    if (restore) menuReturnFocus?.focus({preventScroll: true});
  }
  menuToggle.addEventListener('click', () => {
    menuReturnFocus = document.activeElement;
    menu.hidden = false;
    menu.classList.add('open');
    menuToggle.setAttribute('aria-expanded', 'true');
    inertTargets.forEach(node => { node.inert = true; });
    document.body.classList.add('scroll-locked');
    menuClose.focus();
  });
  menuClose.addEventListener('click', () => closeMenu());
  document.getElementById('mobile-menu-backdrop').addEventListener('click', () => closeMenu());
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    closeMenu(false);
    const target = link.hash && document.getElementById(link.hash.slice(1));
    if (target) { target.setAttribute('tabindex', '-1'); target.focus({preventScroll: true}); }
  }));
  menu.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); closeMenu(); }
    if (event.key === 'Tab') {
      const controls = [...menu.querySelectorAll('a, button')];
      const first = controls[0], last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  const resizeObserver = new ResizeObserver(() => {
    if (innerWidth >= 768 && !menu.hidden) closeMenu();
  });
  resizeObserver.observe(document.documentElement);

  triggers.forEach((trigger, index) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.addEventListener('click', () => { currentIndex = index; renderGallery(); });
    dots.append(dot);
    trigger.addEventListener('click', () => {
      returnFocus = trigger;
      currentIndex = index;
      renderGallery();
      modal.showModal();
      document.body.classList.add('scroll-locked');
      document.getElementById('preview-modal-close').focus();
    });
  });
  const navigateGallery = direction => {
    currentIndex = (currentIndex + direction + triggers.length) % triggers.length;
    renderGallery();
  };
  document.getElementById('preview-modal-close').addEventListener('click', () => modal.close());
  document.getElementById('preview-modal-backdrop').addEventListener('click', () => modal.close());
  document.getElementById('preview-modal-prev').addEventListener('click', () => navigateGallery(-1));
  document.getElementById('preview-modal-next').addEventListener('click', () => navigateGallery(1));
  modal.addEventListener('keydown', event => {
    if (event.key === 'Tab') {
      const controls = [...modal.querySelectorAll('button')];
      const first = controls[0], last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); navigateGallery(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  modal.addEventListener('click', event => {
    if (event.target === modal) modal.close();
  });
  modal.addEventListener('close', () => {
    document.body.classList.remove('scroll-locked');
    returnFocus?.focus({preventScroll: true});
  });
  document.querySelectorAll('#faq details').forEach(faq => {
    faq.addEventListener('toggle', () => { faq.querySelector('summary').setAttribute('aria-expanded', String(faq.open)); });
  });
  new IntersectionObserver(([entry]) => {
    document.getElementById('navbar').classList.toggle('nav-scrolled', !entry.isIntersecting);
  }, {rootMargin: '-80px 0px 0px 0px', threshold: 0}).observe(document.getElementById('intro'));

  let stored = language;
  try { stored = localStorage.getItem('yemx-lang') || language; } catch (_) { /* Cookie-selected language remains available. */ }
  const explicit = new URL(location.href).searchParams.get('lang');
  setLanguage(explicit === 'fr' || explicit === 'en' ? explicit : stored);
})();
