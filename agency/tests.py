from django.test import TestCase

# Create your tests here.
from .models import Profile,Destination,Package,Order

class ProfileTestClass(TestCase):
    # Set up method
    def setUp(self):
        self.rita=Profile(custname='rita',email='rita@gmail.com')

    #testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.rita,Customer))
    
    #testing the save method
    def test_save_method(self):
        self.rita.save_customer()
        customers=Customer.objects.all()
        self.assertTrue(len(customers)>0)

    

    
