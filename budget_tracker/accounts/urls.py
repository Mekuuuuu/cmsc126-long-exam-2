from django.urls import path
from . import views
from transactions import views as transactions_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('add-category/', views.add_category, name='add_category'),
]