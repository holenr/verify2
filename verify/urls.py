# verify/urls.py
from django.urls import path
from .views import DashboardListView, DashboardDetailView, send_test_sms, send_verification_token, check_verification_token, LoginView, EnterTokenView, requestToken, verifyToken, VerifyTokenView


urlpatterns = [
    path('dashboard/<int:pk>/', DashboardDetailView.as_view(), name='dashboard_detail'), # new
    path('', DashboardListView.as_view(), name='home'), # access dashboards (heart of page) directly
    path('smslogin/', LoginView.as_view(), name='sms_login'), # 'login' page with form for user to enter login details
    path('entertoken/', requestToken, name='entertoken'), # page to enter verify token received by sms
    # path('entertoken/', EnterTokenView.as_view(), name='entertoken'), # page to enter verify token received by sms (old class based view)
    path('verifytoken/', verifyToken, name='verifytoken'), # handle verification using submitted login data of user
    # path('verifytoken/', VerifyTokenView.as_view(), name='verifytoken'), # handle verification using submitted login data of user (old class based view)
    
    # Practice to try Twilio 'Verify' service....
    path('sms/', send_test_sms, name='sms'),
    path('sendtoken/', send_verification_token, name='send_token'),
    path('checktoken/', check_verification_token, name='check_token'),
    # path('message/', inbound_view, name='message'),   
    
    # url to send simple (welcome) sms to the user from here directly,
    # as per django-twilio documentation:
    # does not work unfortunately...
    # path('message/', 'django_twilio.views.message', {
    #     'message': 'Test message for Roland from Twilio.',
    #     'to': '+41767910019',
    #     'sender': '+12513599564',
    #     'status_callback': '/message/completed/',
    # }),

    
]