from django.contrib import admin
from .models import UserModel, SMSCode, UserProfile


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display  = ['email', 'first_name', 'last_name']
    list_filter   = ['created_at', 'is_verifiedEmail']
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user','bio', 'profile_image', 'date_of_birth','gender', 'phone_number','address','created_at']
    list_filter   = ['user','bio', 'profile_image', 'date_of_birth','gender', 'phone_number','address','created_at']
    search_fields = ['user','bio', 'profile_image', 'date_of_birth','gender', 'phone_number','address','created_at']




admin.site.register(SMSCode)
