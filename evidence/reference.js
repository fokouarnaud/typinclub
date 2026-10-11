// ========== I18N ==========
const translations = {
  fr: {
    "nav.features": "Fonctionnalités",
    "nav.how": "Comment ça marche",
    "nav.pricing": "Tarifs",
    "nav.download": "Télécharger",
    "hero.title": '<span class="text-primary font-extrabold text-5xl md:text-6xl lg:text-7xl tracking-tight mb-6 block md:mb-8">YemX</span>Le cahier numérique <span class="text-primary italic">des commerçants.</span>',
    "hero.subtitle": "Gérez vos ventes, stocks et crédits clients directement depuis votre téléphone. Simple, rapide et 100% hors-ligne — conçu au Cameroun pour les commerçants.",
    "hero.apk": "Ou télécharger l'APK",
    "hero.badge": "Conçu pour l'Afrique",
    "store.available": "Disponible sur",
    "store.soon": "Bientôt sur",
    "problem.title": "Tu connais ça ?",
    "problem.notebook.title": "Cahier raturé",
    "problem.notebook.desc": "Pages arrachées, écriture illisible ou cahier mouillé ? Ne perdez plus vos données précieuses.",
    "problem.calc.title": "Calculatrice infinie",
    "problem.calc.desc": "Passer des heures à recalculer la journée avec des erreurs qui vous font perdre de l'argent.",
    "problem.debt.title": "Dette perdue",
    "problem.debt.desc": "Oublier qui vous doit quoi et quand. Les petits crédits non réclamés ruinent votre commerce.",
    "features.tag": "Innovation",
    "features.title": "YemX : tout ce qu'il faut pour gérer votre commerce",
    "features.sales.title": "Ventes rapides",
    "features.sales.desc": "Enregistrez une vente en moins de 3 secondes. Vos clients n'attendent plus.",
    "features.stock.title": "Stock temps réel",
    "features.stock.desc": "Soyez alerté quand un produit finit. Ne soyez plus jamais en rupture de stock par surprise.",
    "features.credits.title": "Gestion crédits",
    "features.credits.desc": "Suivez les ardoises de vos clients et envoyez des rappels de paiement en un clic.",
    "features.offline.title": "Offline-first",
    "features.offline.desc": "Pas d'internet ? Pas de problème. L'application fonctionne 100% sans connexion.",
    "features.multi.title": "Multi-boutiques",
    "features.multi.desc": "Gérez plusieurs points de vente depuis un seul compte. Idéal pour les entrepreneurs.",
    "features.pdf.title": "Rapports PDF Professionnels",
    "features.pdf.desc": "Générez vos bilans hebdomadaires ou mensuels en PDF pour une analyse précise de votre croissance.",
    "features.pdf.cta": "Voir un exemple",
    "preview.tag": "Aperçu",
    "preview.title": "Découvrez YemX en action",
    "preview.dashboard": "Tableau de bord",
    "preview.stock": "Gestion du stock",
    "preview.report": "Rapport PDF",
    "preview.journal": "Journal d'activité",
    "steps.title": "Démarrer avec YemX en 3 étapes",
    "steps.s1.title": "Installer YemX",
    "steps.s1.desc": "Installez l'application depuis Google Play, ou téléchargez l'APK directement depuis ce site.",
    "steps.s2.title": "Créer votre boutique",
    "steps.s2.desc": "Entrez le nom de votre commerce et ajoutez vos premiers articles en rayon.",
    "steps.s3.title": "Vendre !",
    "steps.s3.desc": "C'est fini ! Vous pouvez commencer à enregistrer vos ventes et suivre vos stocks.",
    "pricing.title": "Une offre simple, sans surprise",
    "pricing.popular": "POPULAIRE",
    "pricing.free.name": "Gratuit",
    "pricing.free.period": "/à vie",
    "pricing.free.f1": "Jusqu'à 2 boutiques",
    "pricing.free.f2": "25 produits · 15 clients · 50 crédits",
    "pricing.free.f3": "10 rapports PDF",
    "pricing.free.f4": "2 membres d'équipe",
    "pricing.free.f5": "Synchronisation Cloud",
    "pricing.free.cta": "Commencer gratuitement",
    "pricing.pro.period": "/mois",
    "pricing.pro.f1": "Jusqu'à 3 boutiques",
    "pricing.pro.f2": "Produits, clients et crédits illimités",
    "pricing.pro.f3": "Rapports PDF illimités",
    "pricing.pro.f4": "Jusqu'à 5 membres d'équipe",
    "pricing.pro.f5": "Synchronisation Cloud",
    "pricing.pro.cta": "Solliciter",
    "stats.shop": "Boutique créée",
    "stats.sale": "Par vente",
    "stats.start": "Pour démarrer",
    "faq.title": "Questions fréquentes",
    "faq.q1": "C'est vraiment gratuit ?",
    "faq.a1": "Oui ! L'offre de base est 100% gratuite et le restera. Vous pouvez gérer jusqu'à 2 boutiques, 25 produits, 15 clients et 50 crédits sans jamais payer un franc.",
    "faq.q2": "Est-ce que ça marche sans internet ?",
    "faq.a2": "Absolument. YemX est conçu pour fonctionner 100% hors-ligne. Toutes vos données sont stockées directement sur votre téléphone. La connexion internet n'est nécessaire que pour la synchronisation cloud.",
    "faq.q3": "C'est quoi un fichier APK ?",
    "faq.a3": "Un APK est un fichier d'installation pour les téléphones Android. C'est comme un .exe sur un ordinateur. Après le téléchargement, ouvrez le fichier et suivez les instructions d'installation. Vous devrez peut-être autoriser les « sources inconnues » dans vos paramètres.",
    "faq.q4": "Mes données sont-elles en sécurité ?",
    "faq.a4": "Oui. Vos données sont stockées localement sur votre téléphone et ne sont partagées avec personne. Aucune carte bancaire n'est requise pour utiliser l'application.",
    "faq.q5": "Est-ce que ça marche sur iPhone ?",
    "faq.a5": "Pas encore. YemX est aujourd'hui disponible sur Android, via Google Play ou en téléchargeant l'APK. La version iPhone arrive bientôt sur l'App Store.",
    "faq.q6": "Comment mettre à jour l'application ?",
    "faq.a6": "Si vous avez installé YemX depuis Google Play, les mises à jour se font automatiquement. Si vous utilisez l'APK, téléchargez la dernière version depuis ce site et installez-la par-dessus. Dans les deux cas, vos données sont conservées.",
    "faq.q7": "Google Play ou APK : que choisir ?",
    "faq.a7": "Nous recommandons Google Play : l'installation est plus simple et les mises à jour sont automatiques. L'APK reste disponible sur ce site si vous n'avez pas le Play Store sur votre téléphone ou si vous préférez installer sans passer par un compte Google.",
    "cta.title": "Prêt à moderniser votre commerce avec YemX ?",
    "cta.subtitle": "Rejoignez les commerçants qui ont dit adieu au cahier papier. Installez YemX maintenant — c'est gratuit.",
    "cta.or": "ou installation directe",
    "cta.button": "Télécharger l'APK",
    "cta.version": "Version",
    "cta.older": "Téléphone Android plus ancien (32 bits)",
    "cta.note": "L'APK est un fichier d'installation direct pour Android, utile si vous n'avez pas accès au Play Store. Vous devrez peut-être autoriser les \"sources inconnues\" dans vos paramètres.",
    "about.title": "YemX — La startup camerounaise du cahier numérique des commerçants",
    "about.desc": "YemX est une startup née à Yaoundé avec une mission simple : remplacer le cahier papier des commerçants camerounais par un outil numérique fiable, gratuit et qui fonctionne sans internet.",
    "footer.tagline": "L'allié digital de tous les commerçants d'Afrique.",
    "footer.links": "Liens rapides",
    "footer.install": "Installation",
    "footer.follow": "Suivez-nous",
    "footer.rights": "Tous droits réservés.",
    "bottomnav.features": "Fonctions",
    "bottomnav.install": "Installer",
  },
  en: {
    "nav.features": "Features",
    "nav.how": "How it works",
    "nav.pricing": "Pricing",
    "nav.download": "Download",
    "hero.title": '<span class="text-primary font-extrabold text-5xl md:text-6xl lg:text-7xl tracking-tight mb-6 block md:mb-8">YemX</span>The digital ledger <span class="text-primary italic">for merchants.</span>',
    "hero.subtitle": "Manage your sales, inventory and customer credits right from your phone. Simple, fast and 100% offline — built in Cameroon for merchants.",
    "hero.apk": "Or download the APK",
    "hero.badge": "Built for Africa",
    "store.available": "Get it on",
    "store.soon": "Coming soon to",
    "problem.title": "Sound familiar?",
    "problem.notebook.title": "Messy notebook",
    "problem.notebook.desc": "Torn pages, unreadable writing or a wet notebook? Stop losing your precious data.",
    "problem.calc.title": "Endless calculator",
    "problem.calc.desc": "Spending hours recalculating the day's totals with mistakes that cost you money.",
    "problem.debt.title": "Lost debts",
    "problem.debt.desc": "Forgetting who owes what and when. Small uncollected credits are killing your business.",
    "features.tag": "Innovation",
    "features.title": "YemX: everything you need to manage your business",
    "features.sales.title": "Quick sales",
    "features.sales.desc": "Record a sale in under 3 seconds. Your customers won't wait anymore.",
    "features.stock.title": "Real-time inventory",
    "features.stock.desc": "Get alerted when a product runs out. Never be caught off guard by a stockout again.",
    "features.credits.title": "Credit management",
    "features.credits.desc": "Track your customers' tabs and send payment reminders with one tap.",
    "features.offline.title": "Offline-first",
    "features.offline.desc": "No internet? No problem. The app works 100% without any connection.",
    "features.multi.title": "Multi-shop",
    "features.multi.desc": "Manage multiple stores from a single account. Perfect for entrepreneurs.",
    "features.pdf.title": "Professional PDF Reports",
    "features.pdf.desc": "Generate weekly or monthly reports in PDF for a precise analysis of your growth.",
    "features.pdf.cta": "See an example",
    "preview.tag": "Preview",
    "preview.title": "See YemX in action",
    "preview.dashboard": "Dashboard",
    "preview.stock": "Inventory management",
    "preview.report": "PDF Report",
    "preview.journal": "Activity log",
    "steps.title": "Get started with YemX in 3 steps",
    "steps.s1.title": "Install YemX",
    "steps.s1.desc": "Install the app from Google Play, or download the APK directly from this site.",
    "steps.s2.title": "Create your shop",
    "steps.s2.desc": "Enter your business name and add your first products.",
    "steps.s3.title": "Start selling!",
    "steps.s3.desc": "That's it! You can start recording sales and tracking inventory.",
    "pricing.title": "Simple pricing, no surprises",
    "pricing.popular": "POPULAR",
    "pricing.free.name": "Free",
    "pricing.free.period": "/forever",
    "pricing.free.f1": "Up to 2 shops",
    "pricing.free.f2": "25 products · 15 clients · 50 debts",
    "pricing.free.f3": "10 PDF reports",
    "pricing.free.f4": "2 team members",
    "pricing.free.f5": "Cloud sync",
    "pricing.free.cta": "Get started for free",
    "pricing.pro.period": "/month",
    "pricing.pro.f1": "Up to 3 shops",
    "pricing.pro.f2": "Unlimited products, clients & debts",
    "pricing.pro.f3": "Unlimited PDF reports",
    "pricing.pro.f4": "Up to 5 team members",
    "pricing.pro.f5": "Cloud sync",
    "pricing.pro.cta": "Request access",
    "stats.shop": "Shop setup",
    "stats.sale": "Per sale",
    "stats.start": "To start",
    "faq.title": "Frequently asked questions",
    "faq.q1": "Is it really free?",
    "faq.a1": "Yes! The basic plan is 100% free and always will be. You can manage up to 2 shops, 25 products, 15 clients and 50 debts without ever paying a thing.",
    "faq.q2": "Does it work without internet?",
    "faq.a2": "Absolutely. YemX is designed to work 100% offline. All your data is stored directly on your phone. Internet is only needed for cloud sync.",
    "faq.q3": "What is an APK file?",
    "faq.a3": "An APK is an installation file for Android phones. It's like a .exe on a computer. After downloading, open the file and follow the installation instructions. You may need to allow \"unknown sources\" in your settings.",
    "faq.q4": "Is my data secure?",
    "faq.a4": "Yes. Your data is stored locally on your phone and is not shared with anyone. No credit card is required to use the app.",
    "faq.q5": "Does it work on iPhone?",
    "faq.a5": "Not yet. YemX is currently available on Android, via Google Play or by downloading the APK. The iPhone version is coming soon to the App Store.",
    "faq.q6": "How do I update the app?",
    "faq.a6": "If you installed YemX from Google Play, updates happen automatically. If you use the APK, download the latest version from this site and install it over the old one. Either way, your data is preserved.",
    "faq.q7": "Google Play or APK: which should I choose?",
    "faq.a7": "We recommend Google Play: installation is simpler and updates are automatic. The APK stays available on this site if you don't have the Play Store on your phone, or if you'd rather install without a Google account.",
    "cta.title": "Ready to modernize your business with YemX?",
    "cta.subtitle": "Join the merchants who have said goodbye to paper. Install YemX now — it's free.",
    "cta.or": "or install directly",
    "cta.button": "Download APK",
    "cta.version": "Version",
    "cta.older": "Older Android phone (32-bit)",
    "cta.note": "The APK is a direct installation file for Android, useful if you don't have access to the Play Store. You may need to allow \"unknown sources\" in your settings.",
    "about.title": "YemX — The Cameroonian startup behind the merchants' digital ledger",
    "about.desc": "YemX is a startup born in Yaoundé with a simple mission: replace the paper ledger of Cameroonian merchants with a digital tool that is reliable, free and works without internet.",
    "footer.tagline": "The digital ally of every merchant in Africa.",
    "footer.links": "Quick links",
    "footer.install": "Installation",
    "footer.follow": "Follow us",
    "footer.rights": "All rights reserved.",
    "bottomnav.features": "Features",
    "bottomnav.install": "Install",
  }
};

let currentLang = localStorage.getItem('yemx-lang') || 'fr';

function setLang(lang) {
  currentLang = lang;
  localStorage.setItem('yemx-lang', lang);
  document.documentElement.lang = lang;
  document.title = lang === 'fr'
    ? 'YemX — Le cahier numérique des commerçants | Cameroun'
    : 'YemX — The digital ledger for merchants | Cameroon';

  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    var key = el.getAttribute('data-i18n');
    var text = translations[lang] && translations[lang][key];
    if (text) {
      if (el.getAttribute('data-i18n-html') === 'true') {
        el.innerHTML = text;
      } else {
        el.textContent = text;
      }
    }
  });

  document.querySelectorAll('#lang-fr, .lang-fr-btn').forEach(function (b) {
    b.classList.toggle('active', lang === 'fr');
  });
  document.querySelectorAll('#lang-en, .lang-en-btn').forEach(function (b) {
    b.classList.toggle('active', lang === 'en');
  });
}

if (currentLang !== 'fr') setLang(currentLang);

// ========== NAVIGATION ==========
var navbar = document.getElementById('navbar');
window.addEventListener('scroll', function () {
  navbar.classList.toggle('nav-scrolled', window.scrollY > 50);
}, { passive: true });

// ========== MOBILE MENU ==========
var menuToggle = document.getElementById('menu-toggle');
var menuClose = document.getElementById('menu-close');
var mobileMenu = document.getElementById('mobile-menu');

menuToggle.addEventListener('click', function () {
  mobileMenu.classList.add('open');
  document.body.style.overflow = 'hidden';
});

function closeMobileMenu() {
  mobileMenu.classList.remove('open');
  document.body.style.overflow = '';
}

menuClose.addEventListener('click', closeMobileMenu);

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') closeMobileMenu();
});

// ========== SCROLL REVEAL ==========
var observer = new IntersectionObserver(function (entries) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

document.querySelectorAll('.reveal').forEach(function (el) {
  observer.observe(el);
});

// ========== PREVIEW MODAL ==========
var previewSlides = [
  { src: 'screenshot/landing-screens/dashboard-screen.webp', label: 'Tableau de bord', labelEn: 'Dashboard' },
  { src: 'screenshot/landing-screens/stock-screen.webp', label: 'Gestion du stock', labelEn: 'Inventory management' },
  { src: 'screenshot/landing-screens/generated-report-screen.webp', label: 'Rapport PDF', labelEn: 'PDF Report' },
  { src: 'screenshot/landing-screens/actuvity-log-screen.webp', label: "Journal d'activité", labelEn: 'Activity log' }
];
var previewModal = document.getElementById('preview-modal');
var previewImg = document.getElementById('preview-modal-img');
var previewLabel = document.getElementById('preview-modal-label');
var previewDots = document.getElementById('preview-modal-dots');
var previewIndex = 0;

function openPreviewModal(index) {
  previewIndex = index;
  updatePreviewSlide();
  previewModal.classList.add('open');
  previewModal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function closePreviewModal() {
  previewModal.classList.remove('open');
  previewModal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

function updatePreviewSlide() {
  var slide = previewSlides[previewIndex];
  previewImg.src = slide.src;
  previewImg.alt = slide.label;
  previewLabel.textContent = currentLang === 'en' ? slide.labelEn : slide.label;
  previewDots.innerHTML = '';
  previewSlides.forEach(function (_, i) {
    var dot = document.createElement('button');
    dot.className = 'w-2.5 h-2.5 rounded-full transition-all duration-200 ' +
      (i === previewIndex ? 'bg-primary w-6 rounded-md' : 'bg-white/40 hover:bg-white/60');
    dot.setAttribute('aria-label', 'Slide ' + (i + 1));
    dot.addEventListener('click', function () {
      previewIndex = i;
      updatePreviewSlide();
    });
    previewDots.appendChild(dot);
  });
}

function previewNext() {
  previewIndex = (previewIndex + 1) % previewSlides.length;
  updatePreviewSlide();
}

function previewPrev() {
  previewIndex = (previewIndex - 1 + previewSlides.length) % previewSlides.length;
  updatePreviewSlide();
}

document.querySelectorAll('.preview-phone').forEach(function (el) {
  el.addEventListener('click', function () {
    openPreviewModal(parseInt(el.getAttribute('data-preview-index')));
  });
  el.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      openPreviewModal(parseInt(el.getAttribute('data-preview-index')));
    }
  });
});

document.getElementById('preview-modal-close').addEventListener('click', closePreviewModal);
document.getElementById('preview-modal-backdrop').addEventListener('click', closePreviewModal);
document.getElementById('preview-modal-prev').addEventListener('click', previewPrev);
document.getElementById('preview-modal-next').addEventListener('click', previewNext);

document.addEventListener('keydown', function (e) {
  if (!previewModal.classList.contains('open')) return;
  if (e.key === 'Escape') closePreviewModal();
  if (e.key === 'ArrowRight') previewNext();
  if (e.key === 'ArrowLeft') previewPrev();
});

// Touch swipe for preview modal
(function () {
  var touchStartX = 0;
  var touchEndX = 0;
  var content = document.getElementById('preview-modal-content');
  content.addEventListener('touchstart', function (e) {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  content.addEventListener('touchend', function (e) {
    touchEndX = e.changedTouches[0].screenX;
    var diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 50) {
      if (diff > 0) previewNext();
      else previewPrev();
    }
  }, { passive: true });
})();

// ========== FAQ ACCORDION ==========
document.querySelectorAll('.faq-question').forEach(function (button) {
  button.addEventListener('click', function () {
    var item = button.closest('.faq-item');
    var isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(function (i) {
      i.classList.remove('open');
    });
    if (!isOpen) item.classList.add('open');
  });
});
