import urllib, hashlib

from django import template

# -- Little handler for gravatars
register = template.Library()

@register.inclusion_tag('gravatar.html')
def gravatar_img(email, size=48):
    print email
    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        'size': str(size),
    })

    return {'gravatar': {'url': url, 'size': size}}
