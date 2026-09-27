from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from core.models import *
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  u,_=User.objects.get_or_create(username="demo",defaults={"email":"demo@example.com"})
  if not u.has_usable_password(): u.set_password("demo12345"); u.save()
  if not hasattr(u,"profile"): Profile.objects.create(user=u,referral_code="DEMO2026")
  Wallet.objects.get_or_create(user=u)
  Task.objects.get_or_create(title="Welcome task",defaults={"description":"Complete your profile and submit proof.","reward":100})
  Product.objects.get_or_create(slug="starter-pack",defaults={"seller":u,"name":"Starter Digital Pack","description":"Demo product.","price":1500})
  self.stdout.write(self.style.SUCCESS("Demo data created."))
