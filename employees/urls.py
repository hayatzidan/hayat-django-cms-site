from django.urls import path
from . import views

urlpatterns = [
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),  # ✅ fixed here
    path('phone_login_view', views.phone_login_view, name='phone_login_plugin'),
    path('login/send-password/', views.phone_send_password_view, name='phone_send_password'),
    path('login/enter-password/', views.phone_password_login_view, name='phone_password_login'),
    path('visit/', views.count_visit, name='visit'),
    path('show-id/', views.show_user_id, name='show_user_id'),
    path('accounts/connections/', views.social_connections, name='social_connections'),
    path('delete_account/', views.delete_account, name='account_delete'),
    path("settings/", views.accountt_settings, name="accountt_settings"),
    path("unlink/<int:account_id>/", views.unlink_account, name="unlink_account"),
    path("button/", views.button_view, name="button_view"),
]
