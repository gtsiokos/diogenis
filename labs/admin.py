from diogenis.labs.models import *
#from diogenis.accounts.models import *
from django.contrib import admin


admin.site.register(Lesson)
admin.site.register(Lab)
admin.site.register(Teacher)
admin.site.register(TeacherToLab)
admin.site.register(StudentToLesson)
admin.site.register(StudentSubscription)
