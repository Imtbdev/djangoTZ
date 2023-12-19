from django.contrib import admin
from .models import Equipment, IssueType, Request, WorkAssignment, UserProfile, Notification


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'message', 'created_at')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class IssueTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('request', 'author', 'text', 'created_at')


class RequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'date_added', 'equipment', 'issue_type', 'description', 'client', 'status', 'date_closed')
    search_fields = ('number', 'client__user__username')
    list_filter = ('status', 'equipment', 'issue_type', 'client')


class WorkAssignmentAdmin(admin.ModelAdmin):
    list_display = ('request', 'assigned_to', 'completion_date')


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(IssueType, IssueTypeAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(WorkAssignment, WorkAssignmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
