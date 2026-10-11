from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from pathlib import Path
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.db import models
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import LocalizedText, Asset, Preview, FAQ, Offer, OfferBenefit, ExternalLink


class HttpsURLField(forms.URLField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('assume_scheme', 'https')
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        # URLField normally normalizes //host and bare domains to HTTPS.
        # Require an explicit absolute destination before normalization.
        if value and not str(value).strip().lower().startswith('https://'):
            raise ValidationError('Enter an absolute HTTPS URL.')
        return super().to_python(value)


class EditorialAdmin(ModelAdmin):
    actions = None
    formfield_overrides = {models.URLField: {'form_class': HttpsURLField}}

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('code',) if isinstance(obj, Offer) else ('key',)
        return ()


@admin.register(LocalizedText)
class TextAdmin(EditorialAdmin):
    list_display = ('key', 'fr', 'en')
    search_fields = ('key', 'fr', 'en')


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        field_classes = {'source_url': HttpsURLField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        root = Path(__file__).parent / 'static'
        choices = [(path.relative_to(root).as_posix(), path.name)
                   for path in sorted((root / 'showcase' / 'assets').glob('*.webp'))]
        self.fields['path'] = forms.ChoiceField(choices=choices, label='Supplied local asset')


@admin.register(Asset)
class AssetAdmin(EditorialAdmin):
    form = AssetForm
    list_display = ('key', 'path', 'alt')


@admin.register(Preview)
class PreviewAdmin(EditorialAdmin):
    list_display = ('key', 'caption', 'asset', 'order')


@admin.register(FAQ)
class FAQAdmin(EditorialAdmin):
    list_display = ('key', 'question', 'answer', 'order')


@admin.register(Offer)
class OfferAdmin(EditorialAdmin):
    list_display = ('code', 'name', 'price', 'period', 'order')


@admin.register(OfferBenefit)
class BenefitAdmin(EditorialAdmin):
    list_display = ('offer', 'text', 'order')


@admin.register(ExternalLink)
class LinkAdmin(EditorialAdmin):
    list_display = ('key', 'url', 'label')


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
