
def user(request):
    if hasattr(request, 'user'):
        return {'user': request.user }
    return {}

def next(request):
    url = '/'
    if 'next' in request.GET:
        url = request.GET['next']
    return {'next': url, 'request': request}

def settings(request):
    from django.conf import settings
    return {'SITE_NAME': settings.SITE_NAME}
 
