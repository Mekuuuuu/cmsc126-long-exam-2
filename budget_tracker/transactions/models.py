from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPE_CHOICES, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('user', 'name')
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)  # income or expense (user manually selects first)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"{self.name}/{self.type.title()}: of {self.amount} on {self.date} by {self.user.first_name} {self.user.last_name}"
    
    


