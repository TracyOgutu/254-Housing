from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from django.contrib import messages
import requests
from django.core.validators import validate_email
from django.core.mail import send_mail,BadHeaderError
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm,ProfileForm
from .tokens import account_activation_token
from .models import Profile, House
from django.db import transaction


# Create your views here.
def welcome(request):
    try:
        all_houses=House.objects.all()
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'welcome.html',{"all_houses":all_houses})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your +254 Housing Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def account_activation_sent(request):
    return render(request,'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Registration was successful!')
        return redirect('welcome')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,('Your profile was successfully updated!'))
            return redirect('welcome')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {
        'profile_form': profile_form
    })

@login_required
def display_profile(request,user_id):
    '''
    View for displaying the profile for a single user
    '''
    try:
        single_profile=Profile.single_profile(user_id)              
        return render(request,'profiledisplay.html',{"profile":single_profile})
    except Profile.DoesNotExist:
        messages.info(request,'The user has not set a profile yet')
        return redirect('welcome')

'''def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            current_site = get_current_site(request)
            return redirect('welcome')
    else:
        print("hello")
        form = ProfileForm()
    return render(request, 'user-profile/edit_profile.html', {'form': form})
'''

def profile (request):
      if request.method == 'POST':
            u_form = Userupdateform(request.POST,instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                       request.FILES,
                                       instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your profile has been updated successfully!')
                return redirect('welcome')
      else:
            u_form = Userupdateform(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)


      context={
            'u_form':u_form,
            'p_form':p_form,
        }
      return render(request,'user-profile/edit_profile.html',context)












    









    


                







    




