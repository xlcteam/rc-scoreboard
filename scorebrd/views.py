# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from annoying.decorators import render_to
from .models import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.contrib import messages


@render_to('scorebrd/index.html')
def index(request):
    return {'user': request.user}

@render_to('scorebrd/login.html')
def my_login(request, url='index'):
    
    if 'next' in request.POST:
        url = request.POST['next']
    
    def errorHandle(error):
        form = LoginForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        c['error'] = error
        return c

    if request.user.is_authenticated():
        return redirect(url)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # Redirect to a success page.
                    login(request, user)
                    return redirect(url)
            else:
                error = u'Invalid login'
                return errorHandle(error)	
        else:
            return errorHandle(u'Invalid login')
    else:
        form = LoginForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
        return c

def my_logout(request):
    if request.user.is_authenticated():
        logout(request)       

        messages.success(request, 'You have been successfuly logged out.'
                                    ' See you next time!')
        
    return redirect('index')
