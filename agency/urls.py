from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^signup/$',views.signup, name='signup'),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page='login') , name='logout'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^password_reset/$',auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    url(r'^update/profile$', views.update_profile, name='update_profile'),
    url(r'displayprofile/(\d+)',views.display_profile,name='displayprofile'),
    url(r'house/(\d+)',views.single_house,name='singlehouse'),
    url(r'^new/review$', views.make_review, name='make_review'),
    url(r'^searchlocation/',views.search_location,name='searchlocation'),
    url(r'^searchcontract/',views.search_contract,name='searchcontract'),
    path('contact/',views.contact,name='contact'),
    url(r'^send_email/$',views.send_email, name="send_email"), 
    path('displaywishlist/',views.displaywishlist,name='displaywishlist'),
    url(r'addtowishlist/(\d+)',views.addtowishlist,name='addtowishlist'),
    url(r'deletefromwishlist/(\d+)',views.deletefromwishlist,name='deletefromwishlist'),
    path('displaycart/',views.displaycart,name='displaycart'),
    url(r'^makebooking/$',views.make_booking,name="makebooking"),
    url(r'deletefrombooking/(\d+)',views.delete_from_booking,name='deletefrombooking'),
    url(r'^process_payment/$', views.process_payment, name='process_payment'),
    url(r'^payment-done/$', views.payment_done, name='payment_done'),
    url(r'payment-cancelled/$', views.payment_cancelled, name='payment_cancelled'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

