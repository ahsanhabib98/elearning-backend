from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import (
    User,
    Instructor,
    Learner
)
from .serializers import (
    CustomRegisterSerializer,
    ChangePasswordSerializer,
    CustomJwtLoginSerializer,
    UserSerializer,
    InstructorSerializer,
    LearnerSerializer,
    EmailVerificationSerializer
)
from .permissions import (
    IsUserOwnerOrReadOnly,
    IsInstructorOwnerOrReadOnly,
    IsLearnerOwnerOrReadOnly
)
from utils.requestutils import get_current_request
from utils.sendmailutils import SendMailConf

import jwt

# Create your views here.


class UserRegisterView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_active = False
        user.save()
        token = RefreshToken.for_user(user).access_token
        request = get_current_request()
        current_site = request.get_host()
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.email.split('@')[0] + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        SendMailConf.send_email(data)
        return user_data


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verify:
                user.is_verify = True
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomJwtLoginSerializer


class ChangePasswordView(UpdateAPIView):
    lookup_field = "pk"
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsUserOwnerOrReadOnly]


class InstructorViewSet(viewsets.ModelViewSet):
    serializer_class = InstructorSerializer
    queryset = Instructor.objects.all()
    permission_classes = [IsInstructorOwnerOrReadOnly]


class LearnerViewSet(viewsets.ModelViewSet):
    serializer_class = LearnerSerializer
    queryset = Learner.objects.all()
    permission_classes = [IsLearnerOwnerOrReadOnly]


class CurrentLoggedInUser(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user_profile = self.queryset.get(email=request.user.email)
        serializer = self.get_serializer(user_profile)
        return Response({'user': serializer.data})
