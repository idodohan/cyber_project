from django.db import models
from django.contrib.auth.models import User


class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class LoginAttempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=0)
