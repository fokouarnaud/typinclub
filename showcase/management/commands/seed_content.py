import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction
from showcase.models import LocalizedText, Asset, Preview, FAQ, ExternalLink, Offer, OfferBenefit


class Command(BaseCommand):
    help = 'Load reference editorial content without overwriting existing records.'

    @transaction.atomic
    def handle(self, *args, **options):
        data = json.loads((Path(__file__).parents[2] / 'data' / 'texts.json').read_text(encoding='utf-8'))
        texts = {key: LocalizedText.objects.get_or_create(key=key, defaults=values)[0] for key, values in data.items()}
        paths = {'logo': 'logo-yemx/yemx-logo-no-name-remove-background.com.webp',
                 'dashboard': 'screenshot/landing-screens/dashboard-screen.webp',
                 'stock': 'screenshot/landing-screens/stock-screen.webp',
                 'report': 'screenshot/landing-screens/generated-report-screen.webp',
                 'journal': 'screenshot/landing-screens/actuvity-log-screen.webp'}
        assets = {}
        for key, source in paths.items():
            assets[key], _ = Asset.objects.get_or_create(key=key, defaults={
                'path': f'showcase/assets/{key}.webp', 'alt': texts['alt.logo' if key == 'logo' else f'preview.{key}'],
                'source_url': 'https://yemxapp.com/' + source})
        for order, key in enumerate(('dashboard', 'stock', 'report', 'journal')):
            Preview.objects.get_or_create(key=key, defaults={'asset': assets[key], 'caption': texts[f'preview.{key}'], 'order': order})
        for order, number in enumerate((1, 2, 7, 3, 5, 6)):
            FAQ.objects.get_or_create(key=f'faq{number}', defaults={
                'question': texts[f'faq.q{number}'], 'answer': texts[f'faq.a{number}'], 'order': order})
        destinations = {
            'play': ('https://play.google.com/store/apps/details?id=com.yemxapp.app', 'link.play'),
            'apk': ('https://yemxapp.com/apk/yemx-latest.apk', 'cta.button'),
            'pdf': ('https://yemxapp.com/docs/exemple-rapport.pdf', 'features.pdf.cta'),
            'whatsapp': ('https://wa.me/237694208641?text=Bonjour%2C%20je%20suis%20int%C3%A9ress%C3%A9(e)%20par%20l%27offre%20Pro%20de%20YemX.', 'pricing.pro.cta'),
            'facebook': ('https://www.facebook.com/people/YemX/61572368152527/', 'link.facebook'),
            'mentions': ('https://yemxapp.com/mentions-legales.html', 'legal.mentions'),
            'privacy': ('https://yemxapp.com/politique-confidentialite.html', 'legal.privacy'),
            'terms': ('https://yemxapp.com/cgu.html', 'legal.terms'),
            'sales': ('https://yemxapp.com/cgv.html', 'legal.sales'),
        }
        links = {key: ExternalLink.objects.get_or_create(key=key, defaults={'url': url, 'label': texts[label]})[0]
                 for key, (url, label) in destinations.items()}
        for order, (code, price) in enumerate((('free', 0), ('pro', 2500))):
            offer, _ = Offer.objects.get_or_create(code=code, defaults={
                'name': texts[f'pricing.{code}.name'], 'period': texts[f'pricing.{code}.period'],
                'price': price, 'order': order, 'highlighted': code == 'free',
                'cta_anchor': '#download' if code == 'free' else '',
                'external_link': links['whatsapp'] if code == 'pro' else None})
            for number in range(1, 6):
                OfferBenefit.objects.get_or_create(key=f'{code}.f{number}', defaults={
                    'offer': offer, 'text': texts[f'pricing.{code}.f{number}'], 'order': number})
        self.stdout.write(self.style.SUCCESS('Reference content loaded; existing edits preserved.'))
