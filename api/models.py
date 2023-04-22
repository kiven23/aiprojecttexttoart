from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from guardian.shortcuts import assign_perm
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    address = models.CharField(blank=True, max_length=254),
    job_title = models.CharField(blank=True, max_length=254),
    age = models.CharField(blank=True, max_length=254),
    branch_id = models.IntegerField(null=True),
    company_id = models.IntegerField(null=True),
    extn_email1 = models.CharField(blank=True, max_length=254),
    extn_email2 = models.CharField(blank=True, max_length=254),
    extn_email3 = models.CharField(blank=True, max_length=254),
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def short_name(self):
        return self.first_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
# class Pet(models.Model):
#     name = models.CharField(max_length=255)
#     species = models.CharField(max_length=255)
#     breed = models.CharField(max_length=255)
#     gender = models.CharField(max_length=255)
#     birthdate = models.DateField()
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def give_permissions_to_user(self, user):
#         assign_perm('view_pet', user, self)
#         assign_perm('change_pet', user, self)
#
# class Post(models.Model):
#     content = models.TextField()
#     image = models.ImageField(upload_to='post_images/')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
#     following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class Chatroom(models.Model):
#     name = models.CharField(max_length=255)
#     members = models.ManyToManyField(User, related_name='chatrooms')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
# class Message(models.Model):
#     content = models.TextField()
#     chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
# class Images(models.Model):
#     userid = models.TextField()
#     location = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#NEW MODEL FROM PORTAL.ADDESSA.COM NEW PURCHASING SYSTEM

class Branch(models.Model):
    machine_number = models.IntegerField(null=True)
    bsched_id = models.IntegerField(null=True)
    region_id = models.IntegerField(null=True)
    name = models.CharField(max_length=191)
    whscode = models.CharField(max_length=191, null=True)
    bm_oic = models.CharField(max_length=191, null=True)
    contact = models.CharField(max_length=191, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'branches'


class Company(models.Model):
    name = models.CharField(max_length=191)
    address = models.CharField(max_length=191)
    contact = models.CharField(max_length=191, null=True)
    email = models.CharField(max_length=191, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'companies'



class Department(models.Model):
    division_id = models.IntegerField(null=True)
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'departments'



class Division(models.Model):
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'divisions'



class File(models.Model):
    customer_id = models.IntegerField(null=True)
    name = models.CharField(max_length=191, null=True)
    file = models.TextField()
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    from_field = models.IntegerField(null=True, db_column='from')
    to = models.IntegerField(null=True)
    company_id = models.IntegerField(null=True)
    remarks = models.TextField(null=True)
    po_accesschart_id = models.IntegerField(null=True)
    remarks_by = models.IntegerField(null=True)
    remarks2 = models.TextField(null=True)
    waiting_for = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
    po_number = models.IntegerField(null=True)
    type_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'files'



class Position(models.Model):
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'positions'



class Region(models.Model):
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'regions'


class UserEmployments(models.Model):
    id = models.BigAutoField(primary_key=True)
    sss = models.IntegerField(null=True)
    user_id = models.PositiveIntegerField()
    division_id = models.PositiveIntegerField(null=True)
    department_id = models.PositiveIntegerField(null=True)
    position_id = models.PositiveIntegerField(null=True)
    accesschart_id = models.PositiveIntegerField(null=True)
    branch_id = models.PositiveIntegerField(null=True)
    payroll = models.IntegerField(null=True)
    time_from = models.TimeField(null=True)
    time_to = models.TimeField(null=True)
    remarks = models.CharField(max_length=191, null=True)
    last_date_reported = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mrf_accesschart_id = models.PositiveIntegerField(null=True)
    po_file_accesschart_id = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = 'user_employments'
