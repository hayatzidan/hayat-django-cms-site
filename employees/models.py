from django.db import models
from cms.models.pluginmodel import CMSPlugin
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError




class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class GoogleAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.google_id}"


class UserPlatformProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=100)  
    profile_type = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.user.username} - {self.account_type} - {self.profile_type}"


# CMS Plugin Model
class EmployeeTablePluginModel(CMSPlugin):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def get_employees(self):
        return Employee.objects.all()

class ConverterPluginModel(CMSPlugin):
    pass  # You can add options later if needed

class GoogleLoginPluginModel(CMSPlugin):
    pass

class SocialMediaEmbed(CMSPlugin):
    title = models.CharField(max_length=100, blank=True)
    embed_code = models.TextField("Embed HTML Code")


class TermsPluginModel(CMSPlugin):
    title = models.CharField(max_length=200, default="Terms of Service")
    last_updated = models.DateField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title




class PrivacyPluginModel(CMSPlugin):
    title = models.CharField(max_length=200, default="Privacy Policy")
    last_updated = models.DateField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return self.title



class TikTokLoginPluginModel(CMSPlugin):
    button_text = models.CharField(max_length=100, default="Login with TikTok")




class FacebookLoginPluginModel(CMSPlugin):
    pass  # No fields needed for now



class ContinueWithEmailPluginModel(CMSPlugin):
    button_text = models.CharField(max_length=50, default="Continue with Email")

    def __str__(self):
        return self.button_text


class Creator(models.Model):
    CATEGORY_CHOICES = [
        ('Travel', 'Travel'),
        ('Education', 'Education'),
        ('Music', 'Music'),
        ('Religion', 'Religion'),
        ('News', 'News'),
        ('Country', 'Country'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    instagram_profile_link = models.URLField(blank=True, null=True, max_length=500)
    facebook_profile_link = models.URLField(blank=True, null=True, max_length=500)
    tiktok_profile_link = models.URLField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name


class LinkedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)  # Google, Facebook
    provider_account_id = models.CharField(max_length=200)
    date_linked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username} | Type: {self.provider} | ID: {self.provider_account_id} | Date: {self.date_linked.strftime('%Y-%m-%d %H:%M')}"



class ButtonClick(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clicked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} clicked: {self.clicked}"


