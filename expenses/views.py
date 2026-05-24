from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from datetime import datetime, timedelta
import csv

from .models import Expense, Income, Category
from .forms import RegisterForm, ExpenseForm, IncomeForm, CategoryForm


def register(request):
    """User Registration View"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create default categories for new user
            default_categories = ['Food', 'Travel', 'Shopping', 'Bills', 'Others']
            for cat_name in default_categories:
                Category.objects.create(name=cat_name, user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Expense Manager.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard View with Summary"""
    user = request.user
    
    # Calculate totals
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount'))['total'] or 0
    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum('amount'))['total'] or 0
    balance = total_income - total_expenses
    
    # Recent transactions
    recent_expenses = Expense.objects.filter(user=user)[:5]
    recent_incomes = Income.objects.filter(user=user)[:5]
    
    # Monthly data (current month)
    today = datetime.now()
    current_month_expenses = Expense.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    current_month_income = Income.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'total_expenses': total_expenses,
        'total_income': total_income,
        'balance': balance,
        'recent_expenses': recent_expenses,
        'recent_incomes': recent_incomes,
        'current_month_expenses': current_month_expenses,
        'current_month_income': current_month_income,
    }
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list(request):
    """List all expenses with filtering and search"""
    expenses = Expense.objects.filter(user=request.user)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        expenses = expenses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        expenses = expenses.filter(category_id=category_id)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)
    
    # Pagination
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_create(request):
    """Create new expense"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_update(request, pk):
    """Update existing expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def expense_delete(request, pk):
    """Delete expense"""
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


@login_required
def income_list(request):
    """List all incomes"""
    incomes = Income.objects.filter(user=request.user)
    
    # Pagination
    paginator = Paginator(incomes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'expenses/income_list.html', {'page_obj': page_obj})


@login_required
def income_create(request):
    """Create new income"""
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'expenses/income_form.html', {'form': form, 'title': 'Add Income'})


@login_required
def income_update(request, pk):
    """Update existing income"""
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'expenses/income_form.html', {'form': form, 'title': 'Edit Income'})


@login_required
def income_delete(request, pk):
    """Delete income"""
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Income deleted successfully!')
        return redirect('income_list')
    return render(request, 'expenses/income_confirm_delete.html', {'income': income})


@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def category_update(request, pk):
    """Update existing category"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenses/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required
def category_delete(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'expenses/category_confirm_delete.html', {'category': category})


@login_required
def reports(request):
    """Generate reports"""
    user = request.user
    
    # Monthly summary (last 6 months)
    today = datetime.now()
    monthly_data = []
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30*i)
        month_expenses = Expense.objects.filter(
            user=user,
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        month_income = Income.objects.filter(
            user=user,
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_data.append({
            'month': month_date.strftime('%B %Y'),
            'expenses': month_expenses,
            'income': month_income,
        })
    
    # Category-wise expenses
    category_expenses = Expense.objects.filter(user=user).values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Total summary
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount'))['total'] or 0
    total_income = Income.objects.filter(user=user).aggregate(
        total=Sum('amount'))['total'] or 0
    
    context = {
        'monthly_data': monthly_data,
        'category_expenses': category_expenses,
        'total_expenses': total_expenses,
        'total_income': total_income,
    }
    return render(request, 'expenses/reports.html', context)


@login_required
def export_expenses_csv(request):
    """Export expenses to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Category', 'Date', 'Description'])
    
    expenses = Expense.objects.filter(user=request.user).values_list(
        'title', 'amount', 'category__name', 'date', 'description'
    )
    
    for expense in expenses:
        writer.writerow(expense)
    
    messages.success(request, 'Expenses exported successfully!')
    return response
