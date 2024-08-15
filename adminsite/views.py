from django.shortcuts import render, redirect
from django.contrib import messages

# -------------------for email---------------------
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from jackpothaven.config import BASE_DOMAIN
from account.models import UserProfile
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='/login/')
def dashboard(request):
    return render(request, 'adminsite/dashboard.html')

#User Login and Signup Process
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:  # Check if the user is active
                login(request, user)
                # Redirect to a success page or dashboard
                return redirect('index')  # Change 'dashboard' to your desired URL
            else:
                messages.error(request, 'Your account is not active.')
        else:
            # Invalid login
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'adminsite/login.html')

def signup(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = False 
                user.save()

                send_verification_email(request, user)

                messages.success(request, 'Account created successfully. Please check your email to activate your account.')
                return redirect('login')  
        else:
            messages.error(request, 'Passwords do not match.')
        
        

    return render(request, 'adminsite/signup.html')

def check_user_exists(request):
    email = request.GET.get('email', None)
    username = request.GET.get('username', None)
    data = {
        'email_exists': User.objects.filter(email=email).exists(),
        'username_exists': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('adminsite/email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    user.email_user(subject, message)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now login.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('signup')
    
def logout_view(request):
    logout(request)
    return redirect('index')


#Checkout with webhook and fulfil method || sucess and cancel message from stripe
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Bet, Team
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url=settings.LOGIN_URL)
def checkout(request, id):
    event = Event.objects.get(id=id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment')
        bet_team = request.POST.get('bet_team')
        winning_amount = request.POST.get('winnings-amount')

        if payment_method == 'stripe':
            # Create a Checkout Session with Stripe
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Bet for {event.team1} vs {event.team2}',
                            },
                            'unit_amount': int(event.betting_price * 100),  # Amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'https://{BASE_DOMAIN}/admin/success/',
                cancel_url=f'https://{BASE_DOMAIN}/admin/cancel/',
                metadata={
                    'event_id': event.id,
                    'user_id': request.user.id,  # Assuming the user is logged in
                    'predict_winner_id' : bet_team,
                    'potential_payout' : winning_amount,
                    'status': 'pending',
                }
            )
            print('chckout'+winning_amount)

            return redirect(session.url)


    context = {
        'eventdata': event,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'adminsite/checkout.html', context)


logger = logging.getLogger(__name__)
@csrf_exempt
def webhook(request):
    logger.info("Received webhook request with headers: %s", request.META)
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    if sig_header is None:
        logger.error("Missing Stripe signature header")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret, tolerance=900  # Adjusted tolerance to 900 seconds (15 minutes)
        )
        logger.info(f"Webhook event constructed: {event}")
    except ValueError as e:
        logger.error(f"ValueError: {e}, Payload: {payload}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"SignatureVerificationError: {e}, Signature Header: {sig_header}, Payload: {payload}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}, Payload: {payload}")
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        logger.info(f"Processing checkout session completed for session: {session}")

        try:
            fulfill_bet(session)
        except Exception as e:
            logger.error(f"Error fulfilling bet: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)
def fulfill_bet(session):
    event_id = session['metadata']['event_id']
    user_id = session['metadata']['user_id']
    predicted_team_id = session['metadata']['predict_winner_id']
    status = session['metadata']['status']
    potential_payout = session['metadata']['potential_payout']
    print('fulfill'+potential_payout)

    logger.info(f"Fulfilling bet for event_id: {event_id}, user_id: {user_id}, predicted_team_id: {predicted_team_id}")

    try:
        # Fetch the related objects
        event = Event.objects.get(id=event_id)
        predicted_team = Team.objects.get(id=predicted_team_id)

        # Create the Bet object
        Bet.objects.create(
            user_id=user_id,
            predicted_winner=predicted_team,
            event=event,
            amount=session['amount_total'] / 100,
            potential_payout=potential_payout,
            status=status
            
        )
        logger.info(f"Bet created successfully for user_id: {user_id}, event_id: {event_id}")
    except Event.DoesNotExist:
        logger.error(f"Event with id {event_id} does not exist")
        raise
    except Team.DoesNotExist:
        logger.error(f"Team with id {predicted_team_id} does not exist")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def success(request):
    return render(request, 'adminsite/success.html')

def cancel(request):
    return render(request, 'adminsite/cancel.html')



#User show list
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .forms import UserRoleForm
from account.models import UserProfile

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'adminsite/user_list.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def change_user_role(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserRoleForm(instance=user)
    return render(request, 'adminsite/change_user_role.html', {'form': form, 'user': user})

def user_profile_list(request):
    users = UserProfile.objects.all()
    return render(request, 'adminsite/user_profile_list.html', {'users': users})








