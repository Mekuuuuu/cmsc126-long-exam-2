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
    full_transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    income = full_transactions.filter(type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
    expense = full_transactions.filter(type='expense').aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

    total_balance = income - expense
    
    recent_transactions = full_transactions[:5]
    
    categories = Category.objects.all()
    context = {
        'transactions': recent_transactions,
        'total_balance': total_balance,
        'categories': categories,
        
    }
    return render(request, 'auth1_app/home.html', context)

# Protected View
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'registration/protected.html')
    
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