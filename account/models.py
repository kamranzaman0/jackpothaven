from django.contrib.auth.models import User
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='user_profile_pictures/', blank=True)
    otp_code = models.CharField(max_length=6, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Balance"

# class Transaction(models.Model):
#     TRANSACTION_TYPES = (
#         ('deposit', 'Deposit'),
#         ('withdrawal', 'Withdrawal'),
#         ('bet_placed', 'Bet Placed'),
#         ('winnings', 'Winnings')
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     description = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s {self.get_transaction_type_display()}"

# class PaymentMethod(models.Model):
#     PAYMENT_METHOD_TYPES = (
#         ('credit_card', 'Credit Card'),
#         ('paypal', 'PayPal'),
#         ('bank_transfer', 'Bank Transfer')
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     payment_method_type = models.CharField(max_length=20, choices=PAYMENT_METHOD_TYPES)
#     payment_method_details = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s {self.get_payment_method_type_display()}"

# class SecuritySettings(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     two_factor_authentication_enabled = models.BooleanField(default=False)
#     password_reset_options = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s Security Settings"

# class ActivityLog(models.Model):
#     ACTIVITY_TYPES = (
#         ('login_attempt', 'Login Attempt'),
#         ('password_change', 'Password Change'),
#         ('profile_update', 'Profile Update')
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username}'s {self.get_activity_type_display()}"

# class NotificationSettings(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     notification_type = models.CharField(max_length=100)
#     notification_preferences = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s Notification Settings"
