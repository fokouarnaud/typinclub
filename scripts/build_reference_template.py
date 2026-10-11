"""Adapt the saved public reference to Django editorial bindings.

Developer tool, not a runtime dependency. Re-running regenerates home.html.
"""
from pathlib import Path
from bs4 import BeautifulSoup, Comment

root = Path(__file__).resolve().parents[1]
soup = BeautifulSoup((root / 'evidence/reference.html').read_text(encoding='utf-8'), 'html.parser')
body = soup.body
for node in body.find_all(string=lambda s: isinstance(s, Comment)):
    node.extract()
for script in body.select('script'):
    script.decompose()
for node in body.find_all(True):
    for attr in list(node.attrs):
        if attr.startswith('on'):
            del node[attr]

main = body.main
main['id'] = 'main'
main['tabindex'] = '-1'
sections = main.find_all('section', recursive=False)
for section, identifier in zip(sections, ['intro', 'problems', 'features', 'app-preview', 'how-it-works', 'pricing', 'stats', 'faq', 'download', 'about']):
    section['id'] = identifier

# Preserve icons in translated navigation by translating only its label span.
for node in list(body.select('[data-i18n]')):
    key = node['data-i18n']
    if key == 'hero.title':
        del node['data-i18n']
        node.attrs.pop('data-i18n-html', None)
        node.clear()
        node.append(BeautifulSoup('<span class="text-primary font-extrabold text-5xl md:text-6xl lg:text-7xl tracking-tight mb-6 block md:mb-8">YemX</span><span data-hero="lead">{% hero_line "lead" %}</span> <span class="text-primary italic" data-hero="emphasis">{% hero_line "emphasis" %}</span>', 'html.parser'))
        continue
    icons = [icon.extract() for icon in node.select('.material-symbols-outlined')]
    node.clear()
    for icon in icons:
        node.append(icon)
    if icons:
        label = soup.new_tag('span', attrs={'data-i18n': key})
        label.string = '{% text "' + key + '" %}'
        node.attrs.pop('data-i18n', None)
        node.append(label)
    else:
        node.string = '{% text "' + key + '" %}'

source_to_key = {'logo-yemx/yemx-logo-no-name-remove-background.com.webp': 'logo',
 'screenshot/landing-screens/dashboard-screen.webp': 'dashboard',
 'screenshot/landing-screens/stock-screen.webp': 'stock',
 'screenshot/landing-screens/generated-report-screen.webp': 'report',
 'screenshot/landing-screens/actuvity-log-screen.webp': 'journal'}
for image in body.select('img'):
    key = source_to_key.get(image.get('src'))
    if key:
        image['src'] = '{% static assets.' + key + '.path %}'
        image['alt'] = '{% text assets.' + key + '.alt.key %}'
        image['data-i18n-alt'] = '{{ assets.' + key + '.alt.key }}'

destinations = {'https://play.google.com/store/apps/details?id=com.yemxapp.app':'play',
 'apk/yemx-latest.apk':'apk', 'docs/exemple-rapport.pdf':'pdf',
 'https://www.facebook.com/people/YemX/61572368152527/':'facebook',
 '/mentions-legales.html':'mentions','/politique-confidentialite.html':'privacy','/cgu.html':'terms','/cgv.html':'sales'}
for link in body.select('a[href]'):
    destination = destinations.get(link['href'])
    if link['href'].startswith('https://wa.me/'):
        destination = 'whatsapp'
    if destination:
        link['href'] = '{{ links.' + destination + '.url }}'
        link['data-link'] = destination
        link.attrs.pop('download', None)
        if link.has_attr('data-apk-old'):
            link['data-link'] = 'apk-older'
        if destination in ('mentions', 'privacy', 'terms', 'sales'):
            link['data-legal'] = ''
        if destination not in ('play', 'facebook') and not link.has_attr('data-apk-old'):
            label = link.select_one('[data-i18n]') or link
            label['data-i18n'] = '{{ links.' + destination + '.label.key }}'
            label.clear()
            label.string = '{% text links.' + destination + '.label.key %}'
        if destination == 'play':
            label = link.select_one('.store-btn-bottom')
            if label:
                label['data-i18n'] = '{{ links.play.label.key }}'
                label.string = '{% text links.play.label.key %}'
    if link.get('href') == '#faq' and not link.has_attr('data-i18n'):
        link.append(BeautifulSoup('<span data-i18n="nav.faq">{% text "nav.faq" %}</span>', 'html.parser'))
        for text in list(link.find_all(string=True, recursive=False)):
            if 'FAQ' in text:
                text.extract()

# Localized, accessible language links retain a no-JavaScript fallback.
for button in list(body.select('.lang-toggle button')):
    lang = button.get_text(strip=True).lower()
    button.name = 'a'
    button['href'] = '?lang=' + lang
    button['lang'] = lang
    button['data-language'] = lang
    button['class'] = ['language-option']

nav = body.select_one('#navbar nav')
faq = soup.new_tag('a', attrs={'href':'#faq','class':'nav-faq text-on-surface-variant hover:text-primary font-medium','data-i18n':'nav.faq'})
faq.string = '{% text "nav.faq" %}'
nav.select_one('a[href="#download"]').insert_before(faq)

# The structure belongs to templates; editorial rows remain database-driven.
gallery = body.select_one('#app-preview .preview-phone').parent
gallery.clear()
gallery.append(BeautifulSoup('''{% for preview in previews %}
<figure class="text-center shrink-0 snap-center preview-phone">
<button type="button" class="preview-trigger" data-preview-index="{{ forloop.counter0 }}" aria-label="{% text 'preview.open' %}: {% text preview.caption.key %}">
<span class="phone-preview relative block w-[220px] h-[454px] bg-gray-900 rounded-[2rem] p-2 shadow-lg shadow-black/20 ring-1 ring-gray-700/50 mb-4 transition-transform duration-200 hover:scale-[1.03]">
<span class="absolute top-[10px] left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-800 rounded-full z-10 ring-1 ring-gray-700"></span>
<span class="block w-full h-full rounded-[1.5rem] overflow-hidden bg-surface"><img src="{% static preview.asset.path %}" alt="{% text preview.asset.alt.key %}" data-i18n-alt="{{ preview.asset.alt.key }}" class="w-full h-full object-cover object-top" loading="lazy"></span></span></button>
<figcaption class="text-sm font-semibold text-on-surface" data-i18n="{{ preview.caption.key }}">{% text preview.caption.key %}</figcaption></figure>{% endfor %}''', 'html.parser'))

pricing = body.select_one('#pricing .grid')
pricing.clear()
pricing.append(BeautifulSoup('''{% for offer in offers %}
<article class="p-8 md:p-10 rounded-3xl bg-white relative overflow-hidden card-hover offer-card {% if offer.highlighted %}border-4 border-primary shadow-xl{% else %}border border-outline-variant shadow-sm{% endif %}">
{% if offer.highlighted %}<div class="absolute top-0 right-0 bg-primary text-on-primary py-1.5 px-4 rounded-bl-xl font-bold text-xs" data-i18n="pricing.popular">{% text 'pricing.popular' %}</div>{% endif %}
<h3 class="text-2xl font-bold mb-2" data-i18n="{{ offer.name.key }}">{% text offer.name.key %}</h3>
<div class="flex items-baseline gap-1 mb-6 md:mb-8"><span class="text-3xl md:text-4xl font-extrabold tracking-tight">{{ offer.price }} FCFA</span> <span class="text-on-surface-variant text-sm" data-i18n="{{ offer.period.key }}">{% text offer.period.key %}</span></div>
<ul class="space-y-3 md:space-y-4 mb-8 md:mb-10">{% for benefit in offer.benefits.all %}<li class="flex items-center gap-3 text-sm md:text-base"><svg class="icon text-primary text-xl" aria-hidden="true"><use href="{% static 'showcase/icons/sprite.svg' %}#check_circle"></use></svg><span data-i18n="{{ benefit.text.key }}">{% text benefit.text.key %}</span></li>{% endfor %}</ul>
<a class="w-full h-12 md:h-14 rounded-full flex items-center justify-center font-bold active:scale-[0.97] transition-all duration-200 text-sm md:text-base {% if offer.highlighted %}bg-primary text-on-primary shadow-lg hover:bg-emerald-700{% else %}bg-surface-container-highest text-on-surface border border-primary/20 hover:bg-primary hover:text-on-primary{% endif %}" href="{{ offer.cta_url }}" target="{{ offer.external_link|yesno:'_blank,_self' }}" rel="noopener noreferrer" data-i18n="{% if offer.external_link %}{{ offer.external_link.label.key }}{% else %}pricing.{{ offer.code }}.cta{% endif %}">{% if offer.external_link %}{% text offer.external_link.label.key %}{% else %}{% field_text 'pricing' offer.code 'cta' %}{% endif %}</a>
</article>{% endfor %}''', 'html.parser'))

faq_list = body.select_one('#faq .faq-item').parent
faq_list.clear()
faq_list.append(BeautifulSoup('''{% for faq in faqs %}<details class="faq-item bg-white rounded-xl overflow-hidden shadow-sm">
<summary class="faq-question w-full text-left px-6 py-5 flex items-center justify-between font-semibold text-base md:text-lg" aria-expanded="false"><span data-i18n="{{ faq.question.key }}">{% text faq.question.key %}</span><svg class="icon faq-icon text-primary shrink-0 ml-4" aria-hidden="true"><use href="{% static 'showcase/icons/sprite.svg' %}#expand_more"></use></svg></summary>
<div class="faq-answer px-6 text-on-surface-variant text-sm md:text-base leading-relaxed"><p data-i18n="{{ faq.answer.key }}">{% text faq.answer.key %}</p></div></details>{% endfor %}''', 'html.parser'))

modal = body.select_one('#preview-modal')
modal.name = 'dialog'
modal.attrs.pop('aria-hidden', None)
modal['aria-modal'] = 'true'
modal['aria-labelledby'] = 'preview-modal-label'
modal.attrs.pop('aria-label', None)
modal['class'] = ['preview-modal']
modal.select_one('#preview-modal-img')['src'] = '{% static assets.dashboard.path %}'
modal.select_one('#preview-modal-img')['alt'] = '{% text assets.dashboard.alt.key %}'
modal.select_one('#preview-modal-label').string = '{% text "preview.dashboard" %}'
modal.select_one('#preview-modal-dots').insert_after(BeautifulSoup('<p id="preview-modal-position" class="text-white text-sm mt-4" aria-live="polite"></p>', 'html.parser'))

labels = {'menu-toggle':'menu.open','menu-close':'menu.close','preview-modal-close':'preview.close','preview-modal-prev':'preview.previous','preview-modal-next':'preview.next'}
for identifier, key in labels.items():
    node = body.select_one('#' + identifier)
    node['aria-label'] = '{% text "' + key + '" %}'
    node['data-i18n-aria'] = key
    node['type'] = 'button'
body.select_one('#menu-toggle')['aria-expanded'] = 'false'
body.select_one('#menu-toggle')['aria-controls'] = 'mobile-menu'
body.select_one('#mobile-menu')['hidden'] = ''
body.select_one('#mobile-menu')['aria-label'] = '{% text "nav.mobile" %}'
body.select_one('#mobile-menu')['data-i18n-aria'] = 'nav.mobile'
body.select_one('#mobile-menu > div')['id'] = 'mobile-menu-backdrop'
body.select_one('#year').string = '2026'
body.select_one('footer').find_next_sibling('div')['id'] = 'bottom-nav'
home = body.select_one('#navbar > a')
home['aria-label'] = '{% text "home.label" %}'
home['data-i18n-aria'] = 'home.label'
mission = body.select_one('#about p:not([data-i18n])')
mission['data-i18n'] = 'about.mission'
mission.string = '{% text "about.mission" %}'
support = next(node for node in body.select('footer h4') if node.get_text(strip=True) == 'Support')
support['data-i18n'] = 'footer.support'
support.string = '{% text "footer.support" %}'
offline = next(node for node in body.select('#stats div') if node.get_text(strip=True) == 'Offline')
offline['data-i18n'] = 'stats.offline'
offline.string = '{% text "stats.offline" %}'
play_footer = body.select_one('footer a[data-link="play"]')
play_footer['data-i18n'] = '{{ links.play.label.key }}'
play_footer.string = '{% text links.play.label.key %}'
for badge in body.select('.store-btn-soon'):
    badge['data-store'] = 'apple'
    badge['aria-label'] = '{% text "store.apple" %}'
    badge['data-i18n-aria'] = 'store.apple'
for node in body.select('nav[aria-label]'):
    key = 'nav.main' if node.find_parent(id='navbar') else 'nav.mobile' if node.find_parent(id='mobile-menu') else 'nav.legal' if node.select_one('[data-legal]') else 'nav.footer'
    node['aria-label'] = '{% text "' + key + '" %}'
    node['data-i18n-aria'] = key
for link in body.select('a[data-link="play"]'):
    link['aria-label'] = '{% text links.play.label.key %}'
    link['data-i18n-aria'] = '{{ links.play.label.key }}'
for link in body.select('a[data-link="facebook"]'):
    link['aria-label'] = '{% text links.facebook.label.key %}'
    link['data-i18n-aria'] = '{{ links.facebook.label.key }}'

for icon in list(body.select('.material-symbols-outlined')):
    name = icon.get_text(strip=True)
    svg = soup.new_tag('svg', attrs={'class': ['icon', *[c for c in icon.get('class', []) if c != 'material-symbols-outlined']], 'aria-hidden':'true','focusable':'false'})
    use = soup.new_tag('use', attrs={'href':"{% static 'showcase/icons/sprite.svg' %}#" + name})
    svg.append(use)
    icon.replace_with(svg)

body.insert(0, BeautifulSoup('<a class="skip" href="#main" data-i18n="skip.content">{% text "skip.content" %}</a>', 'html.parser'))
output = '''{% load static editorial %}
<!doctype html><html lang="{{ language }}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>YemX</title><meta name="description" content="{% text 'hero.subtitle' %}">
<link rel="icon" href="{% static assets.logo.path %}">
<link rel="stylesheet" href="{% static 'showcase/fonts/lexend.css' %}">
<link rel="stylesheet" href="{% static 'showcase/reference.css' %}">
<link rel="stylesheet" href="{% static 'showcase/site.css' %}">
<script src="{% static 'showcase/site.js' %}" defer></script></head>
''' + str(body) + '''{{ translations|json_script:'editorial-translations' }}</html>'''
output = output.replace('&gt;', '>').replace('&lt;', '<')
(root / 'showcase/templates/showcase/home.html').write_text(output, encoding='utf-8')
(root / 'showcase/static/showcase/reference.css').write_bytes((root / 'evidence/reference.css').read_bytes())
print('Template adapted from reference; assets and editorial bindings are local.')
