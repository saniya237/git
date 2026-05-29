from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('workspace/', views.workspace_view, name='workspace'),
    path('analyse/', views.analyse_view, name='analyse'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('session/<int:session_id>/', views.session_detail_view, name='session_detail'),
    path('session/<int:session_id>/delete/', views.session_delete_view, name='session_delete'),
    path('export/feedback/', views.export_feedback_view, name='export_feedback'),
]