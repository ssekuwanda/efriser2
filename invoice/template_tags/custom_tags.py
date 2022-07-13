from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def lower(value):
    y = ''
    for x in ['1','2','3']:
        y=x
    return y