from django.test import TestCase

from budget.models import Project,Category,Expense

class TestModels(TestCase):

    def setUp(self) -> None:
        self.project1 = Project.objects.create(
            name = 'Project 1',
            budget = 10000
        )
    
    def test_project_is_assigned_slug_on_creation(self):
        #self.assertEquals(self.project1.slug,'Project 1') # Error 
        self.assertEquals(self.project1.slug,'project-1')
    
    def test_budget_left(self):
        cat1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 5000,
            category = cat1
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense2',
            amount = 3000,
            category = cat1
        )
        self.assertEquals(self.project1.budget_left,2000)

    def test_total_transcation_count(self):
        project2 = Project.objects.create(
            name = 'Project2',
            budget = 20000
        )
        cat1 = Category.objects.create(
            project = self.project1,
            name = 'development'
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 5000,
            category = cat1
        )
        Expense.objects.create(
            project = project2,
            title = 'expense2',
            amount = 3000,
            category = cat1
        )
        Expense.objects.create(
            project = self.project1,
            title = 'expense3',
            amount = 5000,
            category = cat1
        )
        #self.assertEquals(project2.total_transactions,1)
        self.assertEquals(self.project1.total_transactions,2)
