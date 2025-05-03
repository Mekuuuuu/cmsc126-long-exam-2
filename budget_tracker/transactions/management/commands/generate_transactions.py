import random
from faker import Faker
from datetime import timedelta, timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transactions.models import Transaction, Category

class Command(BaseCommand):
    help = "Generates fake transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()
        gmt8 = timezone(timedelta(hours=8))

        # Create or get test user
        user, created = User.objects.get_or_create(username='test@gmail.com', defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@gmail.com',
        })
        if created:
            user.set_password('test')
            user.is_superuser = True
            user.is_staff = True
            user.save()

        income_categories = ['Salary', 'Allowance']
        expense_categories = ['Food', 'Transport', 'Education', 'Social', 'Medical', 'Personal', 'Apparel', 'Vacation']

        # Ensure user-specific categories exist
        for name in income_categories:
            Category.objects.get_or_create(name=name, type='income', user=user)

        for name in expense_categories:
            Category.objects.get_or_create(name=name, type='expense', user=user)

        # Fetch from DB for reference
        income_categories_db = Category.objects.filter(type='income', user=user)
        expense_categories_db = Category.objects.filter(type='expense', user=user)

        for _ in range(100):
            transaction_type = random.choice(['income', 'expense'])

            if transaction_type == 'income':
                category = random.choice(income_categories_db)
                name = f"{category.name} Payment"
            else:
                category = random.choice(expense_categories_db)
                name = f"{category.name} Expense"

            amount = round(random.uniform(50, 2500), 2)
            date = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=gmt8)
            description = fake.sentence(nb_words=6)

            Transaction.objects.create(
                user=user,
                name=name,
                type=transaction_type,
                category=category,
                amount=amount,
                date=date,
                description=description
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully generated 100 transactions."))
