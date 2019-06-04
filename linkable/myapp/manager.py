from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password



class MyUserManager(BaseUserManager):
    def create_user(self,username, password, email,name, **extra_fields):
        """
        일반사용자 생성 메서드
        """
        try:
            user = self.model(
                username=username,
                name=name,
                email=email if email else "",
                password=make_password(password),
            )
            extra_fields.setdefault('is_staff', False)
            extra_fields.setdefault('is_superuser', False)
            user.is_active = True
            user.save()
            return user
        except ValidationError:
            raise ValidationError({'detail': 'Enter a proper Email Account'})

    def create_superuser(self,name,email, username=None, password=None, **extra_fields):
        """
        관리자 생성 메서드
        """
        try:
            superuser = self.create_user(
                username=username,
                name=name,
                password=password,
                email = email
            )
            superuser.is_admin = True
            superuser.is_superuser = True
            superuser.is_active = True
            superuser.is_staff = True
            superuser.save()
            return superuser
        except ValidationError:
            raise ValidationError({"detail": "Enter a proper Email Account"})