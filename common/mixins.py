from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

from diogenis.schools.models import School

def user_is_school(user):
    try:
        request_user = School.objects.get(user=user)
        return user.is_authenticated() and request_user.is_school
    except:
        return False

class AuthenticatedSchoolMixin(object):
    
    @method_decorator(user_passes_test(user_is_school, login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        username = kwargs.get('username')
        if username != request.user.username: raise Http404
        return super(AuthenticatedSchoolMixin, self).dispatch(request, *args, **kwargs)
