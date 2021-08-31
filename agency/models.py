from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
import string
import random

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='profile',default='profile/default.png')
    buyer = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    interestedin= models.CharField(max_length=200, blank=True)
    firstname = models.CharField(max_length=30, blank=True)
    lastname = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    user_mac=models.CharField(max_length=1000,default="empty")
    

    #hooking the create_user_profile and save_user_profile methods to
    #the User model whenever a save event occurs
    #using signals so our Profile model will be automatically 
    #created/updated when we create/update User instances.

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @classmethod
    def single_profile(cls,user_id):
        '''
        function gets a single profile posted by id
        '''
        profile=cls.objects.get(user=user_id)
        return profile

class House(models.Model):
    house_image=models.ImageField(upload_to='images/',null=True,blank=True)
    housename=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    description=HTMLField(blank=True,null=True)
    number_of_bedrooms=models.IntegerField(default=1)
    size=models.CharField(max_length=30)
    contract_type=models.CharField(max_length=30)
    price=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    pub_date=models.DateTimeField(auto_now_add=True)
    house_owner=models.CharField(max_length=30)
    house_owner_contact=models.CharField(max_length=30)
    booking_fee=models.DecimalField(max_digits=8,decimal_places=2,null=True)

    def __str__(self):
        return self.housename

    @classmethod
    def single_house(cls,houseid):
        '''
        Shows details of a single house posted by id
        '''
        house=cls.objects.filter(id=houseid)
        return house
    
    @classmethod
    def search_by_location(cls,search_term):
        house_location=cls.objects.filter(location__icontains=search_term)
        return house_location

    @classmethod
    def search_by_contract(cls,search_term):
        house_contract=cls.objects.filter(contract_type__icontains=search_term)
        return house_contract


class Reviews(models.Model):
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    review=models.CharField(max_length=100)
    review_date=models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    house=models.ForeignKey(House,on_delete=models.CASCADE)
    user_mac=models.CharField(max_length=1000)

    def __str__(self):
        return self.house

class Cart(models.Model):
    user_mac=models.CharField(max_length=1000)
    house=models.ManyToManyField(House)
    total=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    receipt_no=models.CharField(null=True,blank=True,max_length=1000)
    payment_method=models.CharField(default="Other",max_length=100)
    phone_no=models.CharField(null=True,blank=True,max_length=100)
    finished=models.BooleanField(default=False)

    def __str__(self):
        return self.user_mac

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars)for _ in range(size))

class BookedHouse(models.Model):
    bookedhouse=models.ForeignKey(House,on_delete=models.CASCADE)
    user_mac=models.CharField(max_length=1000)
    paid=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    finished=models.BooleanField(default=False)

    def __str__(self):
        return self.bookedhouse.housename














