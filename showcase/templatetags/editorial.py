from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def text(context, key):
    return context['texts'].get(key, '')


@register.simple_tag(takes_context=True)
def field_text(context, prefix, item, suffix):
    return context['texts'].get(f'{prefix}.{item}.{suffix}', '')


@register.simple_tag(takes_context=True)
def hero_line(context, part):
    title = context['texts'].get('hero.title', '').removeprefix('YemX ')
    suffix = 'for merchants.' if context['language'] == 'en' else 'des commerçants.'
    if title.endswith(suffix):
        return suffix if part == 'emphasis' else title[:-len(suffix)].rstrip()
    return '' if part == 'emphasis' else title
