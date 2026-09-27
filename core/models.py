from decimal import Decimal
from django.conf import settings
from django.db import models

class Profile(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
 phone=models.CharField(max_length=30,blank=True)
 referral_code=models.CharField(max_length=20,unique=True)
 referred_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,related_name="referred_users")
 is_verified=models.BooleanField(default=False)
 created_at=models.DateTimeField(auto_now_add=True)

class Wallet(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wallet")
 balance=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal("0"))
 lifetime_earnings=models.DecimalField(max_digits=14,decimal_places=2,default=Decimal("0"))
 updated_at=models.DateTimeField(auto_now=True)

class Transaction(models.Model):
 TYPE=[("credit","Credit"),("reward","Reward"),("debit","Debit"),("withdrawal","Withdrawal"),("refund","Refund")]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="transactions")
 type=models.CharField(max_length=20,choices=TYPE)
 amount=models.DecimalField(max_digits=14,decimal_places=2)
 description=models.CharField(max_length=255)
 reference=models.CharField(max_length=80,unique=True)
 created_at=models.DateTimeField(auto_now_add=True)

class Withdrawal(models.Model):
 STATUS=[("pending","Pending"),("approved","Approved"),("paid","Paid"),("rejected","Rejected")]
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="withdrawals")
 amount=models.DecimalField(max_digits=14,decimal_places=2)
 bank_name=models.CharField(max_length=120)
 account_name=models.CharField(max_length=120)
 account_number=models.CharField(max_length=40)
 status=models.CharField(max_length=20,choices=STATUS,default="pending")
 note=models.TextField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)

class Task(models.Model):
 title=models.CharField(max_length=180)
 description=models.TextField()
 reward=models.DecimalField(max_digits=12,decimal_places=2)
 max_completions=models.PositiveIntegerField(default=100)
 completions=models.PositiveIntegerField(default=0)
 is_active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)

class TaskSubmission(models.Model):
 STATUS=[("pending","Pending"),("approved","Approved"),("rejected","Rejected")]
 task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name="submissions")
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="task_submissions")
 proof=models.TextField()
 status=models.CharField(max_length=20,choices=STATUS,default="pending")
 created_at=models.DateTimeField(auto_now_add=True)

class Product(models.Model):
 seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="products")
 name=models.CharField(max_length=180)
 slug=models.SlugField(unique=True)
 description=models.TextField()
 price=models.DecimalField(max_digits=12,decimal_places=2)
 image=models.ImageField(upload_to="products/",blank=True,null=True)
 is_active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)
