from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404,HttpResponse,HttpResponseRedirect
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
from .forms import SignUpForm,ProfileForm,NewReviewForm
from .tokens import account_activation_token
from .models import Profile, House,Reviews,Wishlist,Cart,BookedHouse
from django.db import transaction
from getmac import get_mac_address as gma
from django.conf import settings
import uuid 
import random
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.
def welcome(request):
    try:
        all_houses=House.objects.all()
        allreviews=Reviews.objects.all()
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'welcome.html',{"all_houses":all_houses,"reviews":allreviews})

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

def single_house(request,houseid):
    '''
    Shows the details of a single house that has been posted 
    '''
    try:
        single_house=House.objects.get(id=houseid)
    except ObjectDoesNotExist:
        raise Http404()
    print('**************************single house*************')
    print(single_house)
    return render(request,'singlehouse.html',{"single_house":single_house})

def make_review(request):
    current_user = request.user
    current_id=request.user.id
    print('...................I am the current user....................')
    print(current_id)
    if request.method == 'POST':
        form = NewReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = current_user
            review.save()
        return redirect('welcome')

    else:
        form = NewReviewForm()
    return render(request, 'make_review.html', {"form": form})


def search_location(request):
    if 'locationsearch' in request.GET and request.GET["locationsearch"]:
        search_term=request.GET.get("locationsearch")
        try:
            searched_location=House.search_by_location(search_term)
            message = f"{search_term}"
            return render(request, 'searchlocation.html',{"message":message,"location_results":searched_location})
            
        except House.DoesNotExist:
            messages.info(request,'No house found')
            return redirect('welcome')

    else:
        messsage="You haven't searched for a specific location"
        return render(request,'searchlocation.html',{"message":message})

def search_contract(request):
    if 'contractsearch' in request.GET and request.GET["contractsearch"]:
        search_term=request.GET.get("contractsearch")
        try:
            searched_contract=House.search_by_contract(search_term)
            message = f"{search_term}"
            return render(request, 'searchcontract.html',{"message":message,"contract_results":searched_contract})
            
        except House.DoesNotExist:
            messages.info(request,'No house found')
            return redirect('welcome')

    else:
        messsage="You haven't searched for a specific contract"
        return render(request,'searchcontract.html',{"message":message})

def contact(request):
    return render(request,'contact.html')

def send_email(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['citronsjinja@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('contact')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

@login_required
def displaywishlist(request):
    try:
        wishlist_items=Wishlist.objects.filter(user_mac=gma())
    except Wishlist.DoesNotExist:
        wishlist_items=[]   
    return render(request,'wishlist.html',{"wishitems":wishlist_items})

@login_required
def addtowishlist(request,id):
    houseobj=House.objects.get(id=id)
    try:
        wishlist_exists=Wishlist.objects.get(user_mac=gma(),house=houseobj)
        messages.info(request,"This property is already in your wishlist")
        return redirect("displaywishlist")
    
    except Wishlist.DoesNotExist:
        new_wishlist=Wishlist(house=houseobj,user_mac=gma())
        new_wishlist.save()
        messages.info(request,"The property has been added to your wishlist")
        return redirect('displaywishlist')

@login_required
def deletefromwishlist(request,id):
    try:
        house_del=Wishlist.objects.get(user_mac=gma(),house=id)
        house_del.delete()
        messages.info(request,"The property has been successfully deleted from your wishlist")

        return redirect('displaywishlist')
    except ObjectDoesNotExist:
        raise Http404()

@login_required
def displaycart(request):
    try:
        cart_items=Cart.objects.filter(user_mac=gma(),ordered=False)
    except Cart.DoesNotExist:
        cart_items=[]
    
    return render(request,'cartdisplay.html',{"cartitems":cart_items})

@login_required
@csrf_protect
def make_booking(request):
    house_id=request.POST.get("house_id")
    user_house=House.objects.get(id=house_id)
    print('****************USER_HOUSE******************')
    print(user_house)
    try:
        usercart=Cart.objects.get(user_mac=gma(),ordered=False)
        if usercart.ordered==False:
            housecart=usercart.house.all()
            all_items=[]
            for onehouse in housecart:
                all_items.append(onehouse.housename)
            
            if user_house.housename in all_items:
                messages.info(request,'Destination already exist.')
                return redirect('welcome')
            else:                       
                new_booking=BookedHouse(bookedhouse=user_house,user_mac=gma())
                new_booking.save()
                sub_total=user_house.booking_fee
                usercart.house.add(user_house.id)
                usercart.total+=sub_total
                usercart.save()
                messages.info(request,'The property successfully added to cart.Continue exploring or click cart to proceed to payment')
                return redirect('welcome')

    except Cart.DoesNotExist:
        new_booking=BookedHouse(bookedhouse=user_house,user_mac=gma())
        new_booking.save()

        sub_total=user_house.booking_fee
        new_cart=Cart(user_mac=gma(),total=sub_total)
        new_cart.save()
        new_cart.house.add(user_house)
        new_cart.save()
        messages.info(request,'The property successfully added to your cart.Continue exploring or cart to proceed to payment')
        return redirect('welcome')  

@login_required
@csrf_protect
def delete_from_booking(request,id):
    house=House.objects.get(id=id)
    item_tobe_deleted=BookedHouse.objects.get(bookedhouse=id,user_mac=gma(),paid=False)
    cost=house.booking_fee

    user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
    allhouses=user_cart.house.all()
    if len(allhouses)==1:
        newtotal=0
        user_cart.total=newtotal
        user_cart.house.remove(house.id)
        user_cart.delete()
        item_tobe_deleted.delete()
        messages.info(request,'You have cleared your cart')
        return redirect('displaycart')
    else:
        newtotal=user_cart.total-cost
        user_cart.total=newtotal
        user_cart.house.remove(house.id)
        user_cart.save()
        item_tobe_deleted.delete()

        messages.info(request,'Item successfully deleted from your cart')
        return redirect('displaycart')

@login_required
@csrf_exempt
def process_payment(request):
    #Converting Kenya shillings to US Dollars
    API_KEY= settings.FIXER_ACCESS_KEY 
    url="http://data.fixer.io/api/latest?access_key="+API_KEY+"&symbols=KES,USD"
    response=requests.request("GET",url)
    html=response.json()
    kes=html['rates']['KES']
    usd=html['rates']['USD']
    final_usd=kes/usd

    #Checking out
    try:
        book_house=BookedHouse.objects.filter(user_mac=gma(),paid=False)
    except BookedHouse.DoesNotExist:
        book_house=[]

    try:
        user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
        print('******************USER CART OBJECT***************')
        
        print(user_cart)
        # setting mac address to profile
        current_user=Profile.objects.get(user=request.user)    
        user_cart.user_mac=current_user.user_mac
        current_user.save()
    except Cart.DoesNotExist:
        user_cart=[]

    
    total_in_usd=user_cart.total/final_usd
    list_of_houses=[]
    for house in book_house:
        list_of_houses.append(house.bookedhouse.housename)

    host=request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':'%.2f' % total_in_usd,
        'item_name':'{}'.format(list_of_houses),
        'invoice': str(random.randint(00000,99999)),
        'currency_code':'USD',
        'notify_url':'http://{}{}'.format(host,'-gdgdj-travel-kahndbfh-gshdnhdjf-ksndshdj'),
        'return_url':'http://{}{}'.format(host,'/payment-done/'),
        'cancel_return':'http://{}{}'.format(host,'/payment-cancelled/'),
    }
    form=PayPalPaymentsForm(initial=paypal_dict)
    #End of paypal
    return render(request,'checkout.html',{"form":form,"book_house":book_house,"cart":user_cart})

@login_required
@csrf_exempt
def payment_done(request):
    user_cart=Cart.objects.get(user_mac=gma(),ordered=False)
    book_house=BookedHouse.objects.filter(user_mac=gma(),paid=False)
    user_cart.ordered=True
    user_cart.receipt_no=uuid.uuid4().hex[:6].upper()
    user_cart.payment_method="Paypal"
    user_cart.save()

    for house in book_house:
        house.paid=True
        house.save()
    messages.info(request,'Your booking has been made successfully.Thank you for choosing +254 Housing')
    return redirect('welcome')

@login_required
@csrf_exempt
def payment_cancelled(request):
    messages.info(request,'Payment has been cancelled successfully')
    return redirect('welcome')

@login_required
@csrf_exempt
def payment_error(request):
    messages.info(request,'Your payment process incurred an error.Please contact us to report the matter.')
    return redirect('welcome')








    


                







    




