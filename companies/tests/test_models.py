# Create your tests here.
from django.test import TestCase
from companies.models import Company
from django.utils import timezone

from myCRM.settings import INSTALLED_APPS, AUTH_USER_MODEL


# models test
class CompanyTest(TestCase):
    def setUp(self):
        self.name = "only_test"
        self.manager_name = "test manager"
        self.website = "https://www.test.com"
        self.email = "info@test.com"
        self.phone = "+989140526532"
        self.address = "test address"
        self.description = "test desciption"
        self.created_by = None
        self.is_active = True
        self.deleted = False
        self.uuid = "short uuid"

        Company.objects.create(name=self.name, manager_name=self.manager_name, website=self.website, email=self.email,
                               phone=self.phone,
                               address=self.address, description=self.description, created_by=self.created_by,
                               is_active=self.is_active, deleted=self.deleted, uuid=self.uuid, createdon=timezone.now())

    def test_company_create(self):
        company = Company.objects.get(name="only_test")
        self.assertEqual(company.name, self.name)

    def test_company_list(self):
        company = Company.objects.all()
        self.assertIsNotNone(company, msg="Hello")
