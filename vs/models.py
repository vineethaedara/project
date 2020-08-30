from django.db import models
from django import forms
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class Question(models.Model):
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):    
    def __str__(self):
        return self.choice_text    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
  

class State(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

gen_choices=[
    ('M','Male'),
    ('F','Female'),
    ]


class MyAccountManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not username:
            raise ValueError('User must have an username')
        if not email:
            raise ValueError('User must have an email address')
        user    =self.model(
                    username=username,
                    email=self.normalize_email(email),
                )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password):
        user    =self.create_user(
                    username=username,
                    email=self.normalize_email(email),
                    password=password,
                )
        user.is_admin   =   True
        user.is_staff   =   True
        user.is_superuser   =   True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    username        =models.CharField(max_length=40)
    email           =models.EmailField(max_length=50,verbose_name="email",unique=True)
    phonenumber     =models.CharField(max_length=30,unique=True)
    gender          =models.CharField(choices=gen_choices,max_length=20,default='')
    adhaarnumber    =models.CharField(max_length=12,unique=True)
    location        =models.ForeignKey(State, on_delete=models.SET_NULL,null=True)
    DateOfBirth     =models.DateField(null=True, blank=True)
    date_joined     =models.DateTimeField(verbose_name='date.joined',auto_now_add=True)
    last_login      =models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=True)
    is_staff        =models.BooleanField(default=False)
    is_superuser    =models.BooleanField(default=False)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=    ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
class ControlVote(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    position=models.ForeignKey(Question,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.position