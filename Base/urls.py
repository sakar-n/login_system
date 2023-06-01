from django.contrib import admin
from django.urls import path, include
from .  import views
from Base.views import UserRegistrationView, UserLoginView ,UserProfileView ,UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView
from django.http import JsonResponse
from rest_framework.response import Response




        

urlpatterns = [
               path("", views.apiOverview, name="api-overview"),
               path("register/", UserRegistrationView.as_view(), name="register"),
               path("login/",UserLoginView.as_view(), name="login"),
               path("changepassword/",UserChangePasswordView.as_view(), name="changepassword"),
               path("send-reset-password-email/",SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
               path("reset-password/<uid>/<token>/",UserPasswordResetView.as_view(), name="reset-password"),
               path("profile/",UserProfileView.as_view(), name="profile"),
               path("task-list/", views.taskList, name="task-list"),
               path("task-detail/<str:pk>/", views.taskDetail, name="task-detail"),
               path("task-create/", views.taskCreate, name="task-create"),
               path("task-update/<str:pk>/", views.taskUpdate, name="task-update"),
               path("task-delete/<str:pk>/", views.taskDelete, name="task-delete"),     

]