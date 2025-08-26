from django.shortcuts import render
from .serializers import (UserSerializer,SignupSerializer, UserDetailSerializer)
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Follow
from django.shortcuts import redirect
from django.views import View
# from common.aws import send_follow_event

# Create your views here.

User = get_user_model()

class RootRedirectView(View):
    def get(self, request):
        return redirect('api/auth/login/')
    
class SignupView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message" : "User created Successfully.",
                "status" : True,
                "data" : serializer.data
            }, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response ({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token" : str(refresh.access_token),
            "refresh_token" : str(refresh)
        }, status= status.HTTP_202_ACCEPTED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "id"


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        target = generics.get_object_or_404(User, id=id)

        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

     
        obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target,
        )
        if created:
            # send_follow_event(request.user.id,target.id)
            return Response({"detail": "Followed"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Already following"}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        target = generics.get_object_or_404(User, id=id)

        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        deleted, _ = Follow.objects.filter(
            follower=request.user,
            following=target,
        ).delete()
        if deleted:
            return Response({"detail": "Unfollowed"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not following"}, status=status.HTTP_404_NOT_FOUND)



