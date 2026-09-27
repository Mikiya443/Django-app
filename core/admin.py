from django.contrib import admin
from django.db import transaction
from .models import *

admin.site.site_header="Earnhubs Control Center"
admin.site.site_title="Earnhubs Admin"
admin.site.index_title="Platform management"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","referral_code","is_verified","created_at")
    search_fields=("user__username","user__email","referral_code")
    list_filter=("is_verified",)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display=("user","balance","lifetime_earnings","updated_at")
    search_fields=("user__username",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=("user","type","amount","reference","created_at")
    list_filter=("type",)
    search_fields=("user__username","reference")

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display=("user","amount","status","bank_name","created_at")
    list_filter=("status",)
    search_fields=("user__username","account_number")
    actions=["approve"]
    @admin.action(description="Approve selected withdrawals")
    def approve(self,request,qs):
        qs.filter(status="pending").update(status="approved")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=("title","reward","completions","max_completions","is_active")
    list_filter=("is_active",)
    search_fields=("title",)

@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display=("task","user","status","created_at")
    list_filter=("status",)
    actions=["approve_submissions"]
    @admin.action(description="Approve and credit selected submissions")
    @transaction.atomic
    def approve_submissions(self,request,qs):
        for s in qs.select_related("task","user").filter(status="pending"):
            w,_=Wallet.objects.select_for_update().get_or_create(user=s.user)
            w.balance+=s.task.reward; w.lifetime_earnings+=s.task.reward; w.save()
            Transaction.objects.create(user=s.user,type="reward",amount=s.task.reward,description=f"Task reward: {s.task.title}",reference=f"TASK-{s.id:08d}")
            s.status="approved"; s.save(update_fields=["status"])
            s.task.completions+=1; s.task.save(update_fields=["completions"])

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("name","seller","price","is_active","created_at")
    list_filter=("is_active",)
    search_fields=("name","seller__username")
    prepopulated_fields={"slug":("name",)}
