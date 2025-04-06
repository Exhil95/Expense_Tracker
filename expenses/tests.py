from django.test import TestCase, Client
from .models import Expense 
from datetime import date
from .forms import ExpenseForm
from django.urls import reverse

class ExpenseModelTest(TestCase):
    """
    Test dla modelu Expense.
    """
    def test_expense_str(self):
        expense = Expense.objects.create(
            name="Kebsik",
            amount=25.50,
            category="food",
            date=date.today()
        )
        self.assertEqual(str(expense), "Kebsik - 25.5")


class ExpenseFormTest(TestCase):
    """
    Testy dla ExpenseForm.
    """

    def test_valid_form(self):
        """
        Test walidacji dla formularza ExpenseForm.
        """
    
        form_data = {
            "name": "Bilet na tramwaj",
            "amount": 3.50,
            "category": "transport",
            "date": "2025-06-04",
        }
        form = ExpenseForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        
    def test_invalid_form(self):
        """
        Test sprawdzający wychwytywanie błędnych danych w formularzu ExpenseForm.
        """
        form_data = {
            "name": "",
            "amount": "",
            "category": "",
            "date": "",
        }
        form = ExpenseForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        
class ExpenseViewTest(TestCase):
    """
    testy dla widoków Expense.
    """
    def setUp(self):
        """
        Stworzenie klienta testowego i wydatku
        """
        self.client = Client()
        self.expense = Expense.objects.create(
            name="testowy wydatek",
            amount=99.99,
            category="utilities",
            date=date(2024, 4, 1)
        )

    def test_expense_list_view(self):
        """
        Test widoku listy wydatków, testuje odpowieź serwera, sprawdza którą template używa i czy zawiera testowy wydatek.
        """
        response = self.client.get(reverse("expense_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expenses/expense_list.html")
        self.assertContains(response, "testowy wydatek")