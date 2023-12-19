from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('jobs/', views.job_list, name='jobs'),
    path('requests/', views.request_list, name='request_list'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('requests/create', views.create_request, name='create_request'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/assign_work/', views.assign_work, name='assign_work'),
    path('requests/<int:request_pk>/disassign/', views.delete_work_assignment, name='delete_work_assignment'),
    path('requests/<int:pk>/edit', views.edit_request, name='edit_request'),
    path('requests/<int:pk>/delete/', views.delete_request, name='delete_request'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('statistics/', views.statistics, name='statistics')
]
