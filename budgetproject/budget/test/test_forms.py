from django.test import SimpleTestCase
from budget.forms import ExpenseForm

class TestForms(SimpleTestCase):

    def test_expense_form_valid_data(self):
        form = ExpenseForm(data={
            'title' :'Devep',
            'amount':1000,
            'category':'development'
        })

        #self.assertFalse(form.is_valid())
        self.assertTrue(form.is_valid())


    def test_expense_form_no_data(self):
        form = ExpenseForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),3)
        #self.assertEquals(len(form.errors),2)


    