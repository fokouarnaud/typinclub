import pytest
from django.contrib import admin
from django.urls import reverse
from unfold.admin import ModelAdmin
from showcase.models import LocalizedText, Asset, Preview, FAQ, Offer, OfferBenefit, ExternalLink
from django.forms.models import model_to_dict
from django.contrib.auth.models import Permission
from django.test import Client
from django.contrib.auth.models import User, Group

pytestmark = pytest.mark.django_db


def test_us09_editorial_models_use_unfold():
    for model in (LocalizedText, Asset, Preview, FAQ, Offer, OfferBenefit, ExternalLink):
        assert model in admin.site._registry, f'{model.__name__} needs an editorial admin'
        assert isinstance(admin.site._registry[model], ModelAdmin)


def test_us09_admin_edit_appears_on_next_public_request(admin_client, client, seeded):
    text = LocalizedText.objects.get(key='hero.subtitle')
    response = admin_client.post(reverse('admin:showcase_localizedtext_change', args=[text.pk]), {
        'key': text.key, 'fr': 'Nouveau contenu FR', 'en': 'New EN content', '_save': 'Save'})
    assert response.status_code == 302
    text.refresh_from_db()
    assert text.fr == 'Nouveau contenu FR'
    assert b'Nouveau contenu FR' in client.get('/').content
    assert b'New EN content' in client.get('/?lang=en').content


@pytest.mark.parametrize('model', [LocalizedText, Asset, Preview, FAQ, Offer, OfferBenefit, ExternalLink])
def test_us10_anonymous_and_unprivileged_staff_cannot_edit(client, django_user_model, seeded, model):
    obj = model.objects.first()
    url = reverse(f'admin:showcase_{model._meta.model_name}_change', args=[obj.pk])
    assert client.post(url, {'key': 'tampered'}).status_code == 302
    user = django_user_model.objects.create_user('reader', password='test-only', is_staff=True)
    client.force_login(user)
    assert client.get(url).status_code == 403
    assert client.post(url, {'key': 'tampered'}).status_code == 403


@pytest.mark.parametrize('model', [LocalizedText, Asset, Preview, FAQ, Offer, OfferBenefit, ExternalLink])
def test_required_editorial_records_cannot_be_deleted_even_by_superuser(admin_client, seeded, model):
    obj = model.objects.first()
    url = reverse(f'admin:showcase_{model._meta.model_name}_delete', args=[obj.pk])
    assert admin_client.post(url, {'post': 'yes'}).status_code == 403
    assert model.objects.filter(pk=obj.pk).exists()


@pytest.mark.parametrize('kind', ['asset', 'preview', 'faq', 'offer', 'benefit', 'link'])
def test_us09_each_content_family_can_be_edited_and_rendered(admin_client, client, seeded, kind):
    new_text = LocalizedText.objects.create(key='edited', fr='Édition visible', en='Visible edit')
    if kind == 'asset':
        obj = Asset.objects.get(key='stock')
        changes = {'path': 'showcase/assets/journal.webp', 'alt': new_text.pk}
        expected = '/static/showcase/assets/journal.webp'
    elif kind == 'preview':
        obj = Preview.objects.get(key='dashboard')
        changes = {'caption': new_text.pk, 'order': 99}
        expected = 'Édition visible'
    elif kind == 'faq':
        obj = FAQ.objects.first()
        changes = {'question': new_text.pk, 'answer': new_text.pk, 'order': 99}
        expected = 'Édition visible'
    elif kind == 'offer':
        obj = Offer.objects.get(code='pro')
        changes = {'price': 3000, 'name': new_text.pk, 'period': new_text.pk}
        expected = '3000 FCFA'
    elif kind == 'benefit':
        obj = OfferBenefit.objects.first()
        changes = {'text': new_text.pk, 'order': 99}
        expected = 'Édition visible'
    else:
        obj = ExternalLink.objects.get(key='apk')
        changes = {'url': 'https://yemxapp.com/apk/updated.apk', 'label': new_text.pk}
        expected = 'Édition visible'
    data = {key: '' if value is None else value for key, value in model_to_dict(obj).items()}
    data.update(changes)
    response = admin_client.post(reverse(f'admin:showcase_{obj._meta.model_name}_change', args=[obj.pk]), data)
    assert response.status_code == 302
    obj.refresh_from_db()
    for key, value in changes.items():
        assert getattr(obj, key + '_id' if key in ('alt', 'caption', 'question', 'answer', 'name', 'period', 'text', 'label') else key) == value
    assert expected in client.get('/').content.decode()
    assert 'Visible edit' in client.get('/?lang=en').content.decode()
    if kind == 'link':
        assert 'https://yemxapp.com/apk/updated.apk' in client.get('/').content.decode()


def test_us10_staff_with_only_text_permission_can_edit_text_not_links(client, django_user_model, seeded):
    user = django_user_model.objects.create_user('editor', password='test-only', is_staff=True)
    user.user_permissions.add(Permission.objects.get(codename='change_localizedtext'))
    client.force_login(user)
    text = LocalizedText.objects.get(key='hero.subtitle')
    assert client.post(reverse('admin:showcase_localizedtext_change', args=[text.pk]), {
        'fr': 'Modification autorisée', 'en': 'Permitted edit'}).status_code == 302
    text.refresh_from_db()
    assert text.fr == 'Modification autorisée'
    link = ExternalLink.objects.get(key='apk')
    assert client.post(reverse('admin:showcase_externallink_change', args=[link.pk]), {
        'url': 'https://bad.example/'}).status_code == 403


def test_us10_admin_post_requires_csrf_token(admin_user, seeded):
    client = Client(enforce_csrf_checks=True)
    client.force_login(admin_user)
    text = LocalizedText.objects.first()
    assert client.post(reverse('admin:showcase_localizedtext_change', args=[text.pk]), {
        'fr': 'Unsafe mutation', 'en': 'Unsafe mutation'}).status_code == 403


def test_admin_invalid_data_is_rejected_without_saving(admin_client, seeded):
    text = LocalizedText.objects.get(key='hero.subtitle')
    old = text.en
    response = admin_client.post(reverse('admin:showcase_localizedtext_change', args=[text.pk]), {'fr': 'FR', 'en': '   '})
    assert response.status_code == 200
    assert response.context['adminform'].form.errors
    text.refresh_from_db()
    assert text.en == old


def test_builtin_administrative_user_and_group_forms_use_unfold(admin_client):
    assert isinstance(admin.site._registry[User], ModelAdmin)
    assert isinstance(admin.site._registry[Group], ModelAdmin)
    assert admin_client.get(reverse('admin:auth_user_add')).status_code == 200
