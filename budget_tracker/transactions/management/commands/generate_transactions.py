import random
from faker import Faker
from datetime import timedelta, timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transactions.models import Transaction, Category

class Command(BaseCommand):
    help = "Generates transactions for testing"
    
    def handle(self, *args, **options):
        fake = Faker()
        
        # Define categories for both income and expense
        income_categories = [
            'Salary',
            'Allowance',
        ]
        
        expense_categories = [
            'Food',
            'Transport',
            'Education',
            'Social',
            'Medical',
            'Personal',
            'Apparel',
            'Vacation',
        ]
        
        gmt8 = timezone(timedelta(hours=8))
        
        # Create categories in the database
        for category in income_categories:
            Category.objects.get_or_create(name=category, type='income')
        
        for category in expense_categories:
            Category.objects.get_or_create(name=category, type='expense')
            
        user = User.objects.filter(username='test@gmail.com').first()
        if not user:
            user = User.objects.create_superuser(username='test@gmail.com', password='test')
        
        # Retrieve all categories from the database
        income_categories_db = Category.objects.filter(type='income')
        expense_categories_db = Category.objects.filter(type='expense')
        
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        
        for i in range(20):
            transaction_type = random.choice(types)
            
            # Choose category based on the transaction type
            if transaction_type == 'income':
                category = random.choice(income_categories_db)
            else:
                category = random.choice(expense_categories_db)
                
            # Generate a name for the transaction
            if transaction_type == 'income':
                name = f"{category.name} Payment"
            else:
                name = f"{category.name} Expense"
            
            # Create the transaction
            Transaction.objects.create(
                category=category,
                user=user,
                name=name,
                amount=random.uniform(1, 2500),
                date=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=gmt8),
                type=transaction_type
            )