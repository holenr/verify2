# verify/views.py

from django.views.generic import ListView, DetailView, TemplateView # new
from .models import Dashboard

from django.shortcuts import render, redirect # new, taken from tp-pbi-embedded

# From Verify API Documentation:
from twilio.rest import Client # required

# Roland's Twilio Account Details to use Twilio services: (send sms, emails, voicecall etc.)
# Note: Not ideal to store here! Find a better place to store/ retrieve them (i.e. settings.py)
TWILIO_ACCOUNT_SID = 'AC313e28cfd8f0ef11c59b56184b91dccc' #required
TWILIO_AUTH_TOKEN = '532f80cfeb39a76c1bac46117376aa5b'    #required
    


# Shortcut: access data in database directly without proper authentication (see views below).
# display a list representation of all the objects associated with the specified model in the database belonging to a user:
class DashboardListView(ListView):
    model = Dashboard
    template_name = 'home.html'

# try to use an instance of the DashboardListView class based view as a function based view:
# home_view = DashboardListView.as_view() # does not work...


# display a single object from the model belonging to the user
class DashboardDetailView(DetailView): # new
    model = Dashboard
    template_name = 'dashboard_detail.html'

# login view
class LoginView(TemplateView): # new
    template_name = 'enter_login_details.html'


# function based view version:
# works !
# receive (read) user's phone number from the request and
# request from the Twilio Verify API a new verify token to be sent
# by SMS to this phone number 
def requestToken(request): # new

    number = request.GET.get('cellnum', '')
    print(number) # debugging, works!

    # Request new token from Twilio Verify API:
    # (required to send verification token:)
    #     - A verification service must be created in administrator's (Roland's) Twilio account.
    #     - this gives a verification service (VA) number as for example: 'VAf6e05c76e10c29f0453bc1cf5911a668'
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    verification = client.verify \
                     .services('VAedf528bd6cebfe97bcfd677258fe1038') \
                     .verifications \
                     .create(to=number, channel='sms')

    print(verification.status) # should be pending, works!

    context = {}
    context['num'] = number
    return render(request, 'enter_verify_token.html', context) # as used in tp-pbi-embedded

# ------------------------------------------------------------------------------------
# currently DISABLED in verify.urls.py !
# Alternative class based view version of above function based view: Would be better!

# receive (read) user's phone number from the request and
# request from the Twilio Verify API a new verify token to be sent
# by SMS to this phone number 
class EnterTokenView(TemplateView): # new

    # def getToken(self, **kwargs):
    #     number = self.kwargs['cellnum']
    #     print(number)
    
    def get_context_data(self, **kwargs):
        context = super(EnterTokenView, self).get_context_data(**kwargs)
        context['cellnum'] = self.kwargs['cellnum']
        print(context['cellnum'])
        return context

    template_name = 'enter_verify_token.html' #placeholder
# ------------------------------------------------------------------------------------


# works !
# function based view version:
# handle receiving the token entered by the user and authenticate it.
def verifyToken(request):

    # get entered 6-digit code from request query URL:
    token = request.GET.get('code', '')
    print(token) # debugging, works!

    # get phone from request query URL:
    number = request.GET.get('cellnum', '')
    print(number) # debugging, works!

    context = {}
    context['num'] = number

    if (len(token) != 6):
        # wrong token lenth. go back to page to enter token again: 
        return render(request, 'enter_verify_token.html', context) # back to page to try to enter code again.

    
    # request verification of token from Twilio Verify API
    # using the received 6-digit code for the specific phone number.
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    verification_check = client.verify \
                           .services('VAedf528bd6cebfe97bcfd677258fe1038') \
                           .verification_checks \
                           .create(to=number, code=token)

    print(verification_check.status)

    # handle verification_check.status 'APPROVED' vs 'PENDING':
    if (verification_check.status == "approved"):
        
        # ToDo: add relevent user data to context object, to make user's data available in home page
        # context = {}
        # return render(request, 'home.html', context) # old -> go to home page
        # return redirect(home_view) # does not work!

        # alternative, redirect to '' (home page view) where user's data can be retrieved:
        return redirect("home")

    else:
        return render(request, 'enter_verify_token.html', context) # back to page to try to enter code again.



# ------------------------------------------------------------------------------------
# currently DISABLED in verify.urls.py !
# class based view version of above function based view:
# handle receiving the token entered by the user and authenticate it.
class VerifyTokenView(ListView):
    model = Dashboard
    template_name = 'home.html'  

# ------------------------------------------------------------------------------------


# send a test message to myself (Roland):
def send_test_sms(request):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
    to="+41767910019", 
    from_="+12513599564",
    body="Hello test message from Roland's Django App!")
    print(message.sid)
    return render(request, 'test_sms_sent.html', {}) # as used in tp-pbi-embedded

# send a random verification token to myself (Roland):
def send_verification_token(request):
    #Todo: extract user's phone number from the request somehow.
    #      (probably sent in request through a form)
    #      and use that as 'to' variable below!

    #required to send verification token:
    #     - A verification service must be created in administrator's (Roland's) Twilio account.
    #     - this gives a verification service (VA) number as for example: 'VAf6e05c76e10c29f0453bc1cf5911a668'
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    verification = client.verify \
                     .services('VAedf528bd6cebfe97bcfd677258fe1038') \
                     .verifications \
                     .create(to='+41767910019', channel='sms')

    print(verification.status)

    return render(request, 'verification_token_sent.html', {}) # as used in tp-pbi-embedded


# send a test message to myself (Roland):
def check_verification_token(request):
    #Todo: extract user's phone number and the entered verificatio code
    # from the request somehow and use in the calls below.
    # (probably will be retrievable in request through a form)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    verification_check = client.verify \
                           .services('VAedf528bd6cebfe97bcfd677258fe1038') \
                           .verification_checks \
                           .create(to='+41767910019', code='979046')

    print(verification_check.status)

    return render(request, 'verification_token_checked.html', {}) # as used in tp-pbi-embedded

# old code....
# @twilio_view
# def send_sms(request):
#     r = MessagingResponse()
#     r.message('Test message for Roland!')
#     return r

# @twilio_view
# def inbound_view(request):

#     response = MessagingResponse()

#     # Create a new TwilioRequest object
#     twilio_request = decompose(request)

#     # See the Twilio attributes on the class
#     twilio_request.to
#     # >>> '+44123456789'

#     # Discover the type of request
#     if twilio_request.type is 'message':
#         response.message('Thanks for the message!')
#         return response

#     # Handle different types of requests in a single view
#     if twilio_request.type is 'voice':
#         return voice_view(request)

#     return response

