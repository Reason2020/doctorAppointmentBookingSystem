from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group not in allowed_roles:
                return HttpResponse('<h1>You are not authorized to view this page</h1>')
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorators 

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        elif group == 'patient':
            return redirect('user')
        elif group == 'doctor':
            return redirect('doctor')
    return wrapper_func
            
