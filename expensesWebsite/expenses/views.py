from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
#to render the Category
from .models import *
from django.contrib import messages

# Create your views here.

@never_cache
@login_required(login_url='login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    return render(request, 'expenses/index.html', {'categories': categories, 'expenses': expenses})

@never_cache
@login_required(login_url='login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'values': request.POST}
    if request.method == 'POST':
        
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/add_expense.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/add_expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, "Expense saved successfully")
        return redirect("expenses")
    return render(request, 'expenses/add_expense.html', context)

def editExpense(request, id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/editExpense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, 'expenses/editExpense.html', context)
        
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        
        if not description:
            messages.error(request, "Description is required")
            return render(request, 'expenses/editExpense.html', context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, "Expense Updated successfully")
        return redirect("expenses")    
    
def deleteExpense(request, id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect('expenses')