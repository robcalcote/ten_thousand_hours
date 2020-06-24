from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

#views
from . import views
from tracker.views import GraphData

app_name = 'tracker'
urlpatterns = [
    #authentication url
    path('login/', views.user_login, name='user login'),
    path('register/', views.user_register, name='user register'),
    path('logout/', views.user_logout, name='user logout'),

    #localhost:8000/tracker/<INSERT PATH BELOW HERE>
    path('dashboard/', views.dashboard, name='dashboard'),

    #detail urls
    path('goal_detail/<int:goal_id>/', views.goal_detail, name='goal detail'),
    path('<int:goal_id>/milestone_detail/<int:milestone_id>/', views.milestone_detail, name='milestone detail'),
    path('<int:goal_id>/reward_detail/<int:reward_id>/', views.reward_detail, name='reward detail'),
    path('<int:goal_id>/session_detail/<int:session_id>/', views.session_detail, name='session detail'),

    #record add urls
    path('goal_add/', views.goal_add, name='goal add'),
    path('<int:goal_id>/milestone_add/', views.milestone_add, name='milestone add'),
    path('<int:goal_id>/reward_add/', views.reward_add, name='reward add'),
    path('<int:goal_id>/session_add/', views.session_add, name='session add'),

    #record edit urls
    path('goal_edit/<int:goal_id>/', views.goal_edit, name='goal edit'),
    path('<int:goal_id>/milestone_edit/<int:milestone_id>/', views.milestone_edit, name='milestone edit'),
    path('<int:goal_id>/reward_edit/<int:reward_id>/', views.reward_edit, name='reward edit'),
    path('<int:goal_id>/session_edit/<int:session_id>/', views.session_edit, name='session edit'),

    #Testing a graph page - trying to find a graph library I like
    path('<int:goal_id>/graph/', views.graph, name='graph'),

    # Testing REST interface
    path('api/graph/data/', GraphData.as_view())
]


#serializers & routers
from rest_framework import routers
from tracker.api import GoalViewSet
router = routers.DefaultRouter()
router.register('api/goals', GoalViewSet, 'goals')

#api endpoints
urlpatterns += router.urls

