from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from transactions.models import Transaction, Category
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict


from django.core.paginator import Paginator

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(password)
            
            # Create user with email as username
            user = User.objects.create_user(
                username=email,  # Using email as username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')  # already logged in, go to home
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

# Home View
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home_view(request):
    # Get all transactions for the user
    full_transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Calculate income and expense totals
    income = full_transactions.filter(type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
    expense = full_transactions.filter(type='expense').aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    total_balance = income - expense

    # Prepare chart data
    dates = set()
    income_data = defaultdict(float)
    expense_data = defaultdict(float)

    for txn in full_transactions:
        date_str = txn.datetime.strftime('%Y-%m-%d')
        dates.add(date_str)
        if txn.type == 'income':
            income_data[date_str] += txn.amount
        else:
            expense_data[date_str] += txn.amount

    sorted_dates = sorted(dates)

    # Prepare other data
    recent_transactions = full_transactions[:5]
    categories = Category.objects.all()

    # Combine all data in one context
    context = {
        'transactions': recent_transactions,
        'total_balance': total_balance,
        'categories': categories,
        'labels': sorted_dates,
        'income_totals': [income_data[date] for date in sorted_dates],
        'expense_totals': [expense_data[date] for date in sorted_dates],
    }

    return render(request, 'auth1_app/home.html', context)

# Protected View
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'registration/protected.html')

# Protected View
class TransactionsView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        # Get all transactions for the logged-in user, ordered by date
        filter_type = request.GET.get('type', 'all')  # can be 'income', 'expense', or 'all'
        category_id = request.GET.get('category', 'all')
        page_number = request.GET.get('page', 1)
        
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        
        # Filter by type
        if filter_type in ['income', 'expense']:
            transactions = transactions.filter(type=filter_type)
            categories = Category.objects.filter(type=filter_type)
        else:
            categories = Category.objects.all()
            
        # Filter by category
        if category_id != 'all':
            transactions = transactions.filter(category_id=category_id)
        
        paginator = Paginator(transactions, 20)
        page_obj = paginator.get_page(page_number)
        

        return render(request, 'auth1_app/transactions.html', {
            'transactions': page_obj.object_list,
            'page_obj': page_obj,
            'categories': categories,
            'filter_type': filter_type,
            'selected_category': category_id,
        })
        
        
    
@login_required
def add_transaction(request):
    if request.method == "POST":
        Transaction.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            type=request.POST.get("type"),
            category=Category.objects.get(id=request.POST.get("category")),
            amount=request.POST.get("amount"),
            description=request.POST.get("description")
        )
    return redirect('home')

@csrf_exempt
@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_type = request.POST.get('type')
        new_category = Category.objects.create(name=category_name, type=category_type)
        # Return the new category ID and name as JSON
        return JsonResponse({
            'category_id': new_category.id,
            'category_name': new_category.name
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)