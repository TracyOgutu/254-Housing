from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField



# class CustomUserManager(BaseUserManager):
#     def create_user(self, registration_no, email, password=None):

        
#         if not email:
#             raise ValueError('A valid email address must be given!')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, registration_no, email, password):
#         user = self.create_user(
#             email,
#             password=password,
#             )
#         user.is_admin = True
#         user.save(using=self._db)
#         return 

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
    housename=models.CharField(max_length=30)
    price=models.DecimalField(max_digits=8,decimal_places=2,null=True)
    housename=models.CharField(max_length=100)
    house_image=models.ImageField(upload_to='images/',null=True,blank=True)
    description=HTMLField(blank=True,null=True)
    pub_date=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.housename














