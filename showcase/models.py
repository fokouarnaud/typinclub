from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, URLValidator
from pathlib import Path
from urllib.parse import urlsplit
import uuid
from django.conf import settings


def validate_https(value):
    URLValidator(schemes=['https'])(value)
    parsed = urlsplit(value)
    if parsed.username or parsed.password:
        raise ValidationError('Credentials are not allowed in public URLs.')


class ValidatedModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class LocalizedText(ValidatedModel):
    key = models.CharField(max_length=120, unique=True)
    fr = models.TextField()
    en = models.TextField()

    def clean(self):
        errors = {lang: 'Translation required.' for lang in ('fr', 'en') if not getattr(self, lang).strip()}
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.key


class ExternalLink(ValidatedModel):
    key = models.CharField(max_length=120, unique=True)
    url = models.URLField(max_length=1000, validators=[validate_https])
    label = models.ForeignKey(LocalizedText, on_delete=models.PROTECT)

    def __str__(self):
        return self.key


class Asset(ValidatedModel):
    key = models.CharField(max_length=120, unique=True)
    path = models.CharField(max_length=250)
    alt = models.ForeignKey(LocalizedText, on_delete=models.PROTECT)
    source_url = models.URLField(max_length=1000, validators=[validate_https])

    def clean(self):
        root = Path(__file__).parent / 'static'
        supplied = root / 'showcase' / 'assets'
        candidate = (root / self.path).resolve()
        if '\\' in self.path or not candidate.is_relative_to(supplied.resolve()) or not candidate.is_file():
            raise ValidationError({'path': 'Select a supplied local asset.'})

    def __str__(self):
        return self.key


class Preview(ValidatedModel):
    key = models.CharField(max_length=120, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    caption = models.ForeignKey(LocalizedText, on_delete=models.PROTECT)
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.key


class FAQ(ValidatedModel):
    key = models.CharField(max_length=120, unique=True)
    question = models.ForeignKey(LocalizedText, on_delete=models.PROTECT, related_name='faq_questions')
    answer = models.ForeignKey(LocalizedText, on_delete=models.PROTECT, related_name='faq_answers')
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.key


class Offer(ValidatedModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.ForeignKey(LocalizedText, on_delete=models.PROTECT, related_name='offer_names')
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    period = models.ForeignKey(LocalizedText, on_delete=models.PROTECT, related_name='offer_periods')
    highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(unique=True)
    cta_anchor = models.CharField(max_length=50, blank=True)
    external_link = models.ForeignKey(ExternalLink, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['order']
        constraints = [models.CheckConstraint(condition=models.Q(price__gte=0), name='offer_nonnegative_price')]

    def clean(self):
        if bool(self.cta_anchor) == bool(self.external_link_id):
            raise ValidationError('Choose exactly one CTA: download anchor or external link.')
        if self.cta_anchor and self.cta_anchor != '#download':
            raise ValidationError({'cta_anchor': 'The only permitted CTA anchor is #download.'})

    @property
    def cta_url(self):
        return self.cta_anchor or self.external_link.url

    def __str__(self):
        return self.code


class OfferBenefit(ValidatedModel):
    key = models.CharField(max_length=120, unique=True, default=uuid.uuid4, editable=False)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT, related_name='benefits')
    text = models.ForeignKey(LocalizedText, on_delete=models.PROTECT)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        constraints = [models.UniqueConstraint(fields=['offer', 'order'], name='unique_benefit_order')]

    def __str__(self):
        return f'{self.offer}: {self.text}'


class AdminOTPChallenge(models.Model):
    """One outstanding challenge per administrator, never a plaintext code."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    digest = models.CharField(max_length=64, blank=True)
    session_digest = models.CharField(max_length=64, blank=True)
    sent_at = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(null=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True)
