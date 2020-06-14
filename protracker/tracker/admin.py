from django.contrib import admin

from .models import Goal, Milestone, Reward, Session

# Register your models here.
admin.site.register(Goal)
admin.site.register(Milestone)
admin.site.register(Reward)
admin.site.register(Session)

admin.site.site_url = "//localhost:8000/tracker/dashboard/"