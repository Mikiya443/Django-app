from django.urls import path
from . import views
urlpatterns=[path("",views.home,name="home"),path("register/",views.register,name="register"),path("login/",views.login_view,name="login"),path("logout/",views.logout_view,name="logout"),path("dashboard/",views.dashboard,name="dashboard"),path("tasks/",views.tasks,name="tasks"),path("tasks/<int:task_id>/submit/",views.submit_task,name="submit_task"),path("marketplace/",views.marketplace,name="marketplace"),path("wallet/withdraw/",views.withdraw,name="withdraw"),path("profile/",views.profile,name="profile")]
