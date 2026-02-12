from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expenses', views.add_expenses, name='add_expenses'),
    path('editExpense/<int:id>', views.editExpense, name='editExpense'),
    path('deleteExpense/<int:id>', views.deleteExpense, name="deleteExpense")
]

    