from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from events.models import Bet  # Assuming you have a Bet model
import random
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client
from account.models import UserProfile  # Ensure this import is correct


def user_dashboard(request):
    user = request.user
    user_bets = Bet.objects.filter(user=user)
    
    
    context = {
        'user_bets': user_bets,
    }
    return render(request, 'account/user_dashboard.html', context)


def send_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

def user_profile(request):
    user = request.user
    profile = user.userprofile  # Ensure this is linked correctly

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')

        # Update the profile fields first
        profile.first_name = first_name
        profile.last_name = last_name
        profile.address = address
        profile.date_of_birth = date_of_birth

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        # Check if the phone number has changed
        if profile.phone_number != phone_number:
            otp = f"{random.randint(100000, 999999)}"
            profile.otp_code = otp
            profile.otp_expires_at = timezone.now() + timedelta(minutes=10)
            profile.is_phone_verified = False
            send_otp(phone_number, otp)
            messages.info(request, 'A verification code has been sent to your new phone number.')

            # Temporarily save the new phone number in the session
            request.session['new_phone_number'] = phone_number
            profile.save()
            return redirect('verify_phone_number')

        # If phone number is not changed, save the profile directly
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('user_profile')

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'account/user_profile.html', context)

def verify_phone_number(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        profile = user.userprofile

        if profile.otp_code == otp and profile.otp_expires_at > timezone.now():
            profile.otp_code = otp
            profile.otp_expires_at = None
            profile.is_phone_verified = True
            # Retrieve the new phone number from the session
            new_phone_number = request.session.get('new_phone_number')
            if new_phone_number:
                profile.phone_number = new_phone_number
                del request.session['new_phone_number']  # Clear the session data
            print(profile.is_phone_verified)
            profile.save()
            messages.success(request, 'Phone number verified successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Invalid or expired verification code.')

    return render(request, 'account/verify_phone_number.html')


def user_balance(request):
    return render(request, 'account/user_balance.html')


def user_betting_history(request):
    return render(request, 'account/user_betting_history.html')


# # views.py
# from django.shortcuts import render, redirect, HttpResponse
# from django.conf import settings
# from .forms import PhoneNumberForm
# from twilio.rest import Client
# import random

# client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# def generate_otp():
#     return str(random.randint(100000, 999999))

# def send_sms(phone_number, otp):
#     message = client.messages.create(
#         body=f'Your OTP code is {otp}',
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=phone_number
#     )
#     return message.sid

# def send_otp(request):
#     if request.method == 'POST':
#         form = PhoneNumberForm(request.POST)
#         if form.is_valid():
#             phone_number = form.cleaned_data['phone_number']
#             otp = generate_otp()
#             send_sms(phone_number, otp)
#             request.session['otp'] = otp
#             request.session['phone_number'] = phone_number
#             return redirect('verify_otp')
#     else:
#         form = PhoneNumberForm()
#     return render(request, 'account/send_otp.html', {'form': form})

# def verify_otp(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if otp == request.session.get('otp'):
#             # OTP is correct
#             phone_number = request.session.get('phone_number')
#             # Verify the user phone number here
#             return redirect('user_profile')
#         else:
#             # OTP is incorrect
#             error_message = 'Incorrect OTP. Please try again.'
#             return render(request, 'account/verify_otp.html', {'error_message': error_message})
#     return render(request, 'account/verify_otp.html')

# def success(request):
#     return render(request, 'account/success.html')