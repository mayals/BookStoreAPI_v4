from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, viewsets,  permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from.models import UserProfile, SMSCode
from .serializers import UserRegistrationSerializer, UserModelSerializer,EmailConfirmSerializer, UserProfileSerializer, SMSCodeConfirmSerializer ,CustomTokenObtainPairSerializer
from common import permissions as custom_permissions
# https://github.com/GeeWee/django-auto-prefetching
import django_auto_prefetching
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
from rest_framework_simplejwt.views import TokenObtainPairView


"""""
AutoPrefetchViewSetMixin is a mixin for Django REST Framework viewsets that automatically prefetches the needed objects from the database, based on the viewset's queryset and serializer_class. This can help to improve performance by reducing the number of database queries that need to be made.
To use AutoPrefetchViewSetMixin, you need to import it and then add it as the base class for your viewset.
For example:

from django_auto_prefetching import AutoPrefetchViewSetMixin

class MyViewSet(AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer

AutoPrefetchViewSetMixin will automatically prefetch all of the related objects that are needed by the serializer.
For example, if the serializer includes a field for MyModel.user, AutoPrefetchViewSetMixin will prefetch the User object that is related to the MyModel object.
You can also override the following methods on your viewset to explicitly specify which fields should be prefetches:
get_prefetch_fields()
get_exclude_fields()
"""




###################################################### UserModel #################################################################################
#Register
class UserViewSet(django_auto_prefetching.AutoPrefetchViewSetMixin, viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CustomPagination

    # Define a get_queryset method that returns only active users for non-superusers
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset() 
        # return super().get_queryset().filter(user=self.request.user)
        raise PermissionDenied("You do not have permission to access the list of users.")

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action    
    def get_permissions(self):
        if self.action == 'destroy':
            return {permissions.IsAuthenticated(), permissions.IsAdminUser()}
        if self.action == 'create':
            return {permissions.AllowAny()}
        return super().get_permissions()


#1 register new user in database  ----- register ----  class userviewset[POST]  in views.py
#2 signal work and make hard alink that contain the code and pk and give it to celary as a task ------------------------------ signals.py
#3 task work and send email to the user  -------------------------------task.by
#4 uset receve email and clik the link that reach him to run class ConfirmEmailView(APIView) ----views.py
#5 when class ConfirmEmailView(APIView) run is recollect the pk and token and chech is belong the same user
#  and make the user is acive = true and is_varified email = true
#6 now user has verivied email and active so can doing login by jwt to optain access token 


# check before login - work after the email reach to user and he clik the link inside it 
###################### EmailConfirmAPIView #################
class EmailConfirmAPIView(APIView):
    queryset = get_user_model().objects.all()
    serializer_class = EmailConfirmSerializer
    permission_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            return Response({"error": "Invalid user ID"}, status=400)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verifiedEmail = True
            user.save()
            return Response({"message": "Email confirmation successful"})
        else:
            return Response({"error": "Invalid token"}, status=400)
    

# LOGIN 
###################### JWT CUSTOM VIEW ################# login/get-token/
class CustomTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer








###################################################### UserProfile #################################################################################
class UserProfileViewSet(django_auto_prefetching.AutoPrefetchViewSetMixin,viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser :
           return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)
     
    def get_permissions(self):
        if self.action in ['retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), custom_permissions.IsOwnerOrReadOnly(),]
        if self.action in ['destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser(),]
        return super().get_permissions()
         
    



  ###################################################### SMSCode #################################################################################
class SMSCodeConfirmAPIView(APIView):

    def get(self, request):
        sms_codes = SMSCode.objects.all()
        serializer = SMSCodeConfirmSerializer(sms_codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SMSCodeConfirmSerializer(data=request.data)
        if serializer.is_valid():
            OTP_code = serializer.validated_data['OTP_code']
            try:
                sms_code = SMSCode.objects.get(OTP_code=OTP_code)
            except SMSCode.DoesNotExist:
                return Response({"error": "SMS code not found"}, status=status.HTTP_404_NOT_FOUND)
            if sms_code.is_expired():
                return Response({"error": "SMS code has expired"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "SMS code confirmed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    