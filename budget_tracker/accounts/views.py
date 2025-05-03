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
import csv
from django.http import HttpResponse
from django.utils.dateparse import parse_date
import platform
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek, TruncYear
from datetime import datetime
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
    
    user = request.user
    today = now()
    
    # Get all transactions for the user
    full_transactions = Transaction.objects.filter(user=user).order_by('-date')

    # Calculate income and expense totals
    income = full_transactions.filter(type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
    expense = full_transactions.filter(type='expense').aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0
    total_balance = income - expense

    # Daily grouping (e.g., this week)
    daily = (
        Transaction.objects.filter(user=user, date__month=today.month, date__year=today.year)
        .annotate(day=TruncDay('date'))
        .values('day', 'type')
        .annotate(total=Sum('amount'))
        .order_by('day')
    )
    
    # Monthly grouping (e.g., this year)
    monthly = (
        Transaction.objects.filter(user=user, date__year=today.year)
        .annotate(month=TruncMonth('date'))
        .values('month', 'type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Weekly grouping (this month)
    weekly = (
        Transaction.objects.filter(user=user, date__month=today.month, date__year=today.year)
        .annotate(week=TruncWeek('date'))
        .values('week', 'type')
        .annotate(total=Sum('amount'))
        .order_by('week')
    )

    # Yearly grouping (last 5 years)
    yearly = (
        Transaction.objects.filter(user=user, date__year__gte=today.year - 4)
        .annotate(year=TruncYear('date'))
        .values('year', 'type')
        .annotate(total=Sum('amount'))
        .order_by('year')
    )
    
    def build_chart_data(grouped_data, key):
        income = []
        expense = []
        labels = []

        seen = set()
        for entry in grouped_data:
            if key == 'month':
                label = entry[key].date().strftime('%B')
            elif key == 'week':
                week_start = entry[key].date()
                week_end = week_start + timedelta(days=6)
                label = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}"
            elif key == 'day':
                label = entry[key].date().strftime('%b %d')
            else:
                label = entry[key].strftime('%Y')

            if label not in seen:
                seen.add(label)
                labels.append(label)
                income.append(0)
                expense.append(0)
            idx = labels.index(label)
            if entry['type'] == 'income':
                income[idx] = float(entry['total'])
            else:
                expense[idx] = float(entry['total'])
        return labels, income, expense

    # Build chart data for monthly, weekly, and yearly data
    month_labels, month_income, month_expense = build_chart_data(monthly, 'month')
    day_labels, day_income, day_expense = build_chart_data(daily, 'day')
    week_labels, week_income, week_expense = build_chart_data(weekly, 'week')
    year_labels, year_income, year_expense = build_chart_data(yearly, 'year')

    # Prepare other data
    recent_transactions = full_transactions[:5]
    categories = Category.objects.all()

    # Combine all data in one context
    context = {
        'transactions': recent_transactions,
        'total_balance': total_balance,
        'categories': categories,
        'labels': {
            'monthly': month_labels,
            'weekly': week_labels,
            'yearly': year_labels,
            'daily': day_labels,
        },
        'income_totals': {
            'monthly': month_income,
            'weekly': week_income,
            'yearly': year_income,
            'daily': day_income,
        },
        'expense_totals': {
            'monthly': month_expense,
            'weekly': week_expense,
            'yearly': year_expense,
            'daily': day_expense,
        },
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
        
        date_str = request.POST.get("datetime")
        transaction_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')  # Format: '2025-05-03T12:30'
        
        Transaction.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            type=request.POST.get("type"),
            category=Category.objects.get(id=request.POST.get("category")),
            amount=request.POST.get("amount"),
            description=request.POST.get("description"),
            date=transaction_date,
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

def export_transactions_csv(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Determine platform-specific date format
    is_windows = platform.system() == 'Windows'
    date_format = '%#m/%#d/%Y %H:%M:%S' if is_windows else '%-m/%-d/%Y %H:%M:%S'

    # Handle range shortcuts
    today = date.today()
    range_type = request.GET.get('range')
    start_date_raw = request.GET.get('start_date')
    end_date_raw = request.GET.get('end_date')

    if range_type == 'monthly':
        start_date = date(today.year, today.month, 1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month.replace(day=1) - timedelta(days=1)

    elif range_type == 'annually':
        start_date = date(today.year, 1, 1)
        end_date = date(today.year, 12, 31)

    else:
        start_date = parse_date(start_date_raw) if start_date_raw else None
        end_date = parse_date(end_date_raw) if end_date_raw else None

    transactions = Transaction.objects.filter(user=request.user).select_related('category')

    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    transactions = transactions.order_by('-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Name', 'Category', 'Amount', 'Type', 'Description'])

    for t in transactions:
        writer.writerow([
            t.date.strftime(date_format),
            t.name,
            t.category.name if t.category else '',
            f"{t.amount:.2f}",
            t.type.capitalize(),
            t.description or ''
        ])

    return response