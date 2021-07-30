from django.db import models
from django.db.models.aggregates import Min
from django.forms.formsets import MIN_NUM_FORM_COUNT
from PIL import Image
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



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
    # other fields...


    def __str__(self):
        return f'{self.user.username} profile'


    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 125 or img.width>125:
            output_size = (125, 125)
            img.thumbnail(output_size)
            img.save(self.image.path)


    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class House(models.Model):
    houseName = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='houses')
    location = models.CharField(max_length=100)
    rooms = models.IntegerField()
    price = models.IntegerField()
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.houseName












