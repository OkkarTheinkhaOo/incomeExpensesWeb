from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expenses', views.add_expenses, name='add_expenses'),
    path('editExpense/<int:id>', views.editExpense, name='editExpense'),
    path('deleteExpense/<int:id>', views.deleteExpense, name="deleteExpense"),
    path('search-expenses', csrf_exempt(views.searchExpenses), name='searchExpenses')
]

    