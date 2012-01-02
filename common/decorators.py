#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: UTF-8
import urlparse
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs

def request_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the request passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                        settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator


from django.core.cache import cache
from diogenis.settings import CACHES as caches
from diogenis.local_settings import REDIS_CACHES_VIEWS as redis_is_caching

class cache_view(object):
    '''
    Custom decorator, uses django low-level cache api for caching views.
    
    Key example: '/students/[username]/'
    Current use: diogenis.students.views -> display_labs
    '''

    def __init__(self, timeout=caches['default']['TIMEOUT']):
        """
        This decorator should be used with parentheses, even if no arguments are assigned.
        
        Example: @cache_view()
                 def my_view(...
        """
        self.timeout = timeout

    def __call__(self, func):
        
        def wrap(*args, **kwargs):
            #application = func.__module__.split('.')[1]
            #username = kwargs.get('username', '')
            #key = u':'.join([application, username, func.__name__])
            request = args[0]
            key = request.path
            
            def cache_response():
                response = cache.get(key)
                if response == None:
                    response = func(*args, **kwargs)
                    cache.set(key, response, self.timeout)
                return response
            
            response = cache_response() if redis_is_caching else func(*args, **kwargs)
            return response
        return wrap
    
