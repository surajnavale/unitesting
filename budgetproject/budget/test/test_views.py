
from django.http import response
from django.test import TestCase,Client
from django.urls.base import reverse
from budget.models import Project,Category,Expense
import json
class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name = 'project1',
            budget = 10000
        )

    
    def test_project_list_GET(self):
        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-list.html')
    
    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'budget/project-detail.html')
    
    def test_project_detail_add_new_expence_POST(self):
        Category.objects.create(
            project = self.project1,
            name = 'Devops'
        )

        response = self.client.post(self.detail_url,{
            'title':'expense1',
            'amount':1000,
            'category':'Devops'
        }
        
        )

        self.assertEquals(response.status_code,302)
        #self.assertTemplateUsed(response,'budget/project-detail.html')
        self.assertEquals(self.project1.expenses.first().title,'expense1') # expenses is related name
    
    def test_project_detail_no_expence_POST(self):
        Category.objects.create(
            project = self.project1,
            name = 'Devops'
        )

        

        response = self.client.post(self.detail_url)

        self.assertEquals(response.status_code,302)
        self.assertEquals(self.project1.expenses.count(),0)
    
    def test_project_detail_delete_expence_with_id_POST(self):
        cat1 = Category.objects.create(
            project = self.project1,
            name = 'Devops'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = cat1
        )
        response = self.client.delete(self.detail_url, json.dumps({'id':1}))

        self.assertEquals(response.status_code,204) # views.py delete method returns status code 204
        self.assertEquals(self.project1.expenses.count(),0)

    
    def test_project_detail_delete_expence_no_id_POST(self):
        cat1 = Category.objects.create(
            project = self.project1,
            name = 'Devops'
        )

        Expense.objects.create(
            project = self.project1,
            title = 'expense1',
            amount = 1000,
            category = cat1
        )
        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code,404) # views.py delete method returns status code 404
        self.assertEquals(self.project1.expenses.count(),1) # as id is not provided for delete expence count is 1


    def test_project_create_add(self):
        url = reverse('add')
        #As in setup func we created project1,
        response = self.client.post(url,{
            'name':'project2', 
            'budget':10000,
            'categoriesString':'design,development'
        }
        )

        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name,'project2')
        fst_cat = Category.objects.get(id = 1)
        self.assertEquals(fst_cat.project.name,'project2')
        self.assertEquals(fst_cat.name,'design')