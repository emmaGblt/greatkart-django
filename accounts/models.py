from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(first_name, last_name, email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=False
    )  # To be active, the user needs to validate its email
    is_superuser = models.BooleanField(default=False)  # FIXME: keep it?

    USERNAME_FIELD = "email"  # the unique field used to log in (default: username)
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]  # fields to provide when using createsuperuser command (must not contain the USERNAME_FIELD)

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
