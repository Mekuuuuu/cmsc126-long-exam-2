from django.contrib import admin
from transactions.models import Category, Transaction

admin.site.register(Transaction)
admin.site.register(Category)
