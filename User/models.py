from django.db import models


class UserModel(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    otp_code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.email
