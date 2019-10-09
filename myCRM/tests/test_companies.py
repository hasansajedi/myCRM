from django.test import TestCase
from companies.models import Company
from django.utils import timezone
from companies.forms import CompanyForm


# models test
class CompanyTest(TestCase):
    def create_company(self, name="", manager_name="", website="", email="", phone="", address="",
                       description="", created_by="", is_active="", deleted="", uuid=""):
        return Company.objects.create(name=name, manager_name=manager_name, website=website, email=email, phone=phone,
                                      address=address, description=description, created_by=created_by,
                                      is_active=is_active, deleted=deleted, uuid=uuid, createdon=timezone.now())

    def test_whatever_creation(self):
        w = self.create_company(name="only a test", manager_name="test manager", website="https://www.test.com",
                                 email="info@test.com", phone="+989140526532", address="test address",
                                 description="test desciption", created_by=None, is_active=True, deleted=False)
        self.assertTrue(isinstance(w, Company))
        self.assertEqual(w.__unicode__(), w.name)
