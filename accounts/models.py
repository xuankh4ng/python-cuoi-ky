from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField("Họ và tên", max_length=255, blank=True)
    gender = models.CharField("Giới tính", max_length=10, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField("Ngày sinh", null=True, blank=True)
    phone = models.CharField("Số điện thoại", max_length=20, blank=True)
    address = models.CharField("Địa chỉ", max_length=255, blank=True)
    avatar = models.ImageField("Avatar", upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'Profile: {self.user.username}'
