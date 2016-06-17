from django.db import models
from django.contrib.auth.models import User

# import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'


class Invoice(models.Model):
    """
    Defines invoice model. 
    Contains amounts, status and dates of payments done by linked users.
    """
    dt_created = models.DateTimeField(auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, editable=False)
    # Improvement: payment method might be smth like this:
    # paid_by = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-dt_created']


class Service(models.Model):
    """
    Defines service model.
    Contains names and prices of services.
    """
    name  = models.CharField(max_length=254, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # Improvement: status (available/not) 
    # might be helpful to show only available ones at the frontend
    # available = models.Boolean(default=True)

    class Meta:
        ordering = ['name']


class Subscription(models.Model):
    """
    Defines subscribtion model.
    Contains dt_created, dt_modified, service and user.
    """
    dt_created = models.DateTimeField(auto_now_add=True, editable=False)
    dt_renewed = models.DateTimeField(auto_now=True)
    service = models.ForeignKey(Service)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-dt_created']
        

# Customizing User Model if needed email as username field.
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 

# class LugatiUserManager(BaseUserManager):
#     """ 
#     Unlike in standart UserManager, username .
#     """
#     use_in_migrations = True

#     def _create_user(self, email, password,
#                      is_staff, is_superuser, **extra_fields):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         now = timezone.now()
#         if not email:
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(email=email,
#                           is_staff=is_staff, is_active=True,
#                           is_superuser=is_superuser,
#                           date_joined=now, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, False, False, 
#                                 **extra_fields)

#     def create_superuser(self, email, password, **extra_fields):
#         return self._create_user(email, password, True, True, 
#                                 **extra_fields)


# class LugatiUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = LugatiUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def get_full_name(self):
#         return self.email

#     def get_short_name(self):
#         return self.email

#     def __str__(self):
#         return self.email


