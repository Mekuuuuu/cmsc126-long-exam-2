from django.db.models.signals import post_migrate
from django.dispatch import receiver
from transactions.models import Category

@receiver(post_migrate)
def create_default_template_categories(sender, **kwargs):
    if Category.objects.filter(user__isnull=True).exists():
        return

    default_categories = [
        {'name': 'Salary', 'type': 'income'},
        {'name': 'Allowance', 'type': 'income'},
        {'name': 'Freelance', 'type': 'income'},
        {'name': 'Investments', 'type': 'income'},
        {'name': 'Gifts', 'type': 'income'},
        {'name': 'Food', 'type': 'expense'},
        {'name': 'Transportation', 'type': 'expense'},
        {'name': 'Healthcare', 'type': 'expense'},
        {'name': 'Clothing', 'type': 'expense'},
        {'name': 'Education', 'type': 'expense'},
        {'name': 'Entertainment', 'type': 'expense'},
        {'name': 'Personal Care', 'type': 'expense'},
        {'name': 'Vacation', 'type': 'expense'},
        {'name': 'Utilities', 'type': 'expense'},
        {'name': 'Insurance', 'type': 'expense'},
        {'name': 'Subscriptions', 'type': 'expense'},
        {'name': 'Charity', 'type': 'expense'},
        {'name': 'Pets', 'type': 'expense'},
        {'name': 'Miscellaneous', 'type': 'expense'},
    ]

    for cat in default_categories:
        Category.objects.get_or_create(name=cat['name'], type=cat['type'], user=None)