import uuid
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404,redirect,render
from .forms import RegisterForm
from .models import *

def home(request): return render(request,"home.html",{"tasks":Task.objects.filter(is_active=True)[:6],"products":Product.objects.filter(is_active=True)[:8]})

def register(request):
 form=RegisterForm(request.POST or None)
 if request.method=="POST" and form.is_valid():
  u=form.save()
  code=form.cleaned_data.get("referral_code","").strip().upper()
  ref=Profile.objects.filter(referral_code=code).first() if code else None
  Profile.objects.create(user=u,referral_code=uuid.uuid4().hex[:10].upper(),referred_by=ref.user if ref else None)
  Wallet.objects.create(user=u)
  messages.success(request,"Account created. You can now sign in.")
  return redirect("login")
 return render(request,"auth/register.html",{"form":form})

def login_view(request):
 if request.method=="POST":
  u=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
  if u: login(request,u); return redirect("dashboard")
  messages.error(request,"Invalid username or password.")
 return render(request,"auth/login.html")

def logout_view(request): logout(request); return redirect("home")

@login_required
def dashboard(request):
 wallet, _=Wallet.objects.get_or_create(user=request.user)
 return render(request,"dashboard.html",{"wallet":wallet,"transactions":request.user.transactions.all()[:8],"withdrawals":request.user.withdrawals.all()[:5],"tasks":Task.objects.filter(is_active=True)[:6]})

@login_required
def tasks(request): return render(request,"tasks.html",{"tasks":Task.objects.filter(is_active=True)})

@login_required
def submit_task(request,task_id):
 task=get_object_or_404(Task,id=task_id,is_active=True)
 if request.method=="POST":
  if TaskSubmission.objects.filter(task=task,user=request.user).exists(): messages.error(request,"You already submitted this task.")
  else: TaskSubmission.objects.create(task=task,user=request.user,proof=request.POST.get("proof","")); messages.success(request,"Proof submitted for admin review.")
 return redirect("tasks")

def marketplace(request): return render(request,"marketplace.html",{"products":Product.objects.filter(is_active=True)})

@login_required
@transaction.atomic
def withdraw(request):
 if request.method!="POST": return redirect("dashboard")
 amount=Decimal(request.POST.get("amount","0"))
 wallet=Wallet.objects.select_for_update().get(user=request.user)
 if amount<500 or amount>wallet.balance: messages.error(request,"Minimum withdrawal is ₦500 and balance must be sufficient."); return redirect("dashboard")
 w=Withdrawal.objects.create(user=request.user,amount=amount,bank_name=request.POST.get("bank_name",""),account_name=request.POST.get("account_name",""),account_number=request.POST.get("account_number",""))
 wallet.balance-=amount; wallet.save()
 Transaction.objects.create(user=request.user,type="withdrawal",amount=amount,description=f"Withdrawal request #{w.id}",reference=f"WD-{w.id:08d}")
 messages.success(request,"Withdrawal request submitted."); return redirect("dashboard")

@login_required
def profile(request):
 p=request.user.profile
 if request.method=="POST": p.phone=request.POST.get("phone",p.phone); request.user.email=request.POST.get("email",request.user.email); request.user.save(); p.save(); messages.success(request,"Profile updated.")
 return render(request,"profile.html")
