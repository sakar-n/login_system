from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.views import APIView
from Base.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from .serializers import TaskSerializer
from rest_framework import status, filters
from Base.renderers import UserRenderer
from django.contrib.auth import login, logout
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User,Task
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from Base.pagination import LargeResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration Successful"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)

                return Response(
                    {"token": token, "msg": "Login Success"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["email or password is not valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, fromat=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password Changed Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes =[UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "Password reset link sent please check your email"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context ={"uid":uid, "token":token})
        print(token)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg": "password reset successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SearchAPIView(generics.ListAPIView):
    
    filter_backends = [filters.SearchFilter]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ['title']

   

@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "List": "/task-list/",
        "Detail View": "/task-detail/<str:pk>/",
        "Create": "/task-create/",
        "Update": "/task-update/<str:pk>/",
        "Delete": "/task-delete/<str:pk>/",
    }
    return Response(api_urls)




@api_view(["GET"])

def taskList(request):
    paginator = LargeResultsSetPagination()
    tasks = Task.objects.all()
    paginated_tasks = paginator.paginate_queryset(tasks, request)
    serializer = TaskSerializer(paginated_tasks, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    
   
    serializer = TaskSerializer(tasks)
    return Response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])

def taskCreate(request):
    
    serializer = TaskSerializer(data=request.data)
    serializer.is_valid()

    
    if request.user == serializer.validated_data.get("user"):
            serializer.save(user=request.user)
    
    if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
    return Response(serializer.errors)



@api_view(["POST"])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)

    if request.user != task.user:
        return Response("You are not allowed to update this task.", status=status.HTTP_403_FORBIDDEN)
    serializer = TaskSerializer(instance=task, data=request.data)


    

    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
    



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])

def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
   
    if request.user != task.user:
        return Response("You are not allowed to delete this task.", status=status.HTTP_403_FORBIDDEN)
    task.delete()
    
    return Response("item deleted")




