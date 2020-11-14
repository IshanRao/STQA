from django.urls import path
from . import views


app_name = 'stqa'

urlpatterns = [
    path('',views.index,name="index"),
    path('group_signup',views.gr_signup,name="group_signup"),
    path('group_login',views.gr_login,name="group_login"),
    path('group_logout',views.gr_logout,name="group_logout"),
    path('manager_logout',views.manager_logout,name="manager_logout"),
    path('manager_login',views.manager_login,name="manager_login"),
    path('add_projects',views.add_projects,name="add_projects"),
    path('group_project_page',views.group_project_page,name="group_project_page"),
    path('manager_project_page',views.manager_project_page,name="manager_project_page"),
    path('project_info',views.project_info,name="project_info"),
    path('group_info',views.group_info,name="group_info"),
   
]