from django.urls import path

from . import views

app_name = 'tracker'
urlpatterns = [
    #localhost:8000/tracker/<INSERT PATH BELOW HERE>
    path('dashboard/', views.dashboard, name='dashboard'),
    path('goal_view/<int:goal_id>/', views.goal_view, name='goal view'),
    path('goal_edit/<int:goal_id>/', views.goal_edit, name='goal edit'),
    path('goal_add/', views.goal_add, name='goal add'),
    path('<int:goal_id>/milestone_view/<int:milestone_id>/', views.milestone_view, name='milestone view'),
    path('<int:goal_id>/milestone_edit/<int:milestone_id>/', views.milestone_edit, name='milestone edit'),
    path('<int:goal_id>/milestone_add/', views.milestone_add, name='milestone add'),
    path('<int:goal_id>/reward_view/<int:reward_id>/', views.reward_view, name='reward view'),
    path('<int:goal_id>/reward_edit/<int:reward_id>/', views.reward_edit, name='reward edit'),
    path('<int:goal_id>/reward_add/', views.reward_add, name='reward add'),
    path('<int:goal_id>/session_edit/<int:session_id>/', views.session_edit, name='session edit'),
    path('<int:goal_id>/session_add/', views.session_add, name='session add'),

    path('<int:goal_id>/process_totals/', views.process_totals, name='process totals'),
    path('<int:goal_id>/updated/', views.updated, name='updated'),
]