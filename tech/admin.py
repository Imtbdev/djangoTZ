from django.contrib import admin
from .models import Equipment, IssueType, Request, WorkAssignment, UserProfile

# Register your models here.

admin.site.register(Equipment)
admin.site.register(IssueType)
admin.site.register(Request)
admin.site.register(WorkAssignment)
admin.site.register(UserProfile)
