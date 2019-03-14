from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import pre_save, post_save, m2m_changed
# from django.db.models.signals import 
from django.dispatch import receiver

class Inventory(models.Model):
    
    product_name = models.CharField(max_length=30)
    product_id = models.IntegerField(null=True,blank=True)
    vendor = models.CharField(max_length=30)
    mrp = models.FloatField()
    batch_number = models.CharField(max_length=30)
    quantity = models.IntegerField()
    batch_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30,choices=(('pending','Pending'),('approved','Approved')), default='pending')
    operation = models.CharField(max_length=30,choices=(('create','Create'),('update','Update'),('delete','Delete')), default='create')

    def __str__(self):
        return self.product_name


class UserRole(models.Model):
    name = models.CharField(max_length=30)
    is_manager = models.BooleanField()  
    is_assistant = models.BooleanField()
    users = models.ManyToManyField('User', blank=True)


    def __str__(self):
        return self.name

@receiver(m2m_changed, sender=UserRole.users.through)
def users_callback(sender, instance, action, **kwargs):
    users = instance.users.all()
    if action == 'post_add':
        for user in User.objects.all():
            if user in users:
                if instance not in user.role.all():
                    user.role.add(instance)
            else:
                if instance in user.role.all():
                    user.role.remove(instance)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = kwargs.get('username')
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, *args, **kwargs):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username = kwargs.get('username')
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username = kwargs.get('username')
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    role = models.ManyToManyField(UserRole, blank=True)
    username = models.CharField(max_length=30, null=True, unique=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active 


@receiver(m2m_changed, sender=User.role.through)
def roles_callback1(sender, instance, action, **kwargs):
    roles = instance.role.all()
    if action == 'post_add':
        for role in UserRole.objects.all():
            if role in roles:
                if instance not in role.users.all():
                    role.users.add(instance)
            else:
                if instance in role.users.all():
                    role.users.remove(instance)


