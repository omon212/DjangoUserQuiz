from django.contrib import admin

from .models import UserModel

admin.site.register(UserModel,
                    list_display=['email','password','otp_code'],
                    search_fields=['email','otp_code'])
