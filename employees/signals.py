from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.contrib.auth.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from allauth.socialaccount.models import SocialToken
from employees.youtube_utils import get_youtube_profile
from datetime import date
from employees.models import GoogleAccount, UserPlatformProfile, LinkedAccount

# ✅ لما المستخدم يضيف حساب Google لأول مرة
@receiver(social_account_added)
def create_google_account(sender, request, sociallogin, **kwargs):
    print("🔥 Signal Triggered: social_account_added")
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        google_id = sociallogin.account.uid
        if not GoogleAccount.objects.filter(user=user).exists():
            GoogleAccount.objects.create(user=user, google_id=google_id)
            print(f"✅ GoogleAccount created for {user.email}")
        else:
            print(f"ℹ GoogleAccount already exists for {user.email}")

# ✅ عند تسجيل دخول المستخدم، نتحقق من وجود GoogleAccount ونعمل له إدخال إذا مش موجود
@receiver(user_logged_in)
def ensure_google_account(sender, request, user, **kwargs):
    print("🔥 Signal Triggered: user_logged_in")
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        if not GoogleAccount.objects.filter(user=user).exists():
            GoogleAccount.objects.create(user=user, google_id=social_account.uid)
            print(f"✅ GoogleAccount created during login for {user.email}")
        else:
            print(f"ℹ GoogleAccount already exists for {user.email}")
    except SocialAccount.DoesNotExist:
        print(f"❌ No Google SocialAccount found for {user.email}")



@receiver(user_logged_in)
def create_user_profile(sender, request, user, **kwargs):
    # تأكدي إنه ما يتكررش
    if not UserPlatformProfile.objects.filter(user=user).exists():
        # هنا تقدري تحددي أنواع الحسابات حسب ما تحبي
        UserPlatformProfile.objects.create(
            user=user,
            account_type="YouTube",
            profile_type="Education"
        )


@receiver(user_logged_in)
def show_facebook_profile(sender, request, user, **kwargs):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='facebook')
        extra_data = social_account.extra_data
        name = extra_data.get("name")
        profile_pic = extra_data.get("picture", {}).get("data", {}).get("url")

        print("🎉 Facebook Login Successful!")
        print(f"👤 Name: {name}")
        print(f"🖼 Profile Picture: {profile_pic}")
    except SocialAccount.DoesNotExist:
        print("❌ No Facebook account found.")


@receiver(user_logged_in)
def handle_login(sender, request, user, **kwargs):
    print("🔥 Signal Triggered: user_logged_in")

    youtube_data = get_youtube_profile(user)
    if youtube_data:
        print("📺 YouTube Data:", youtube_data)
        items = youtube_data.get('items', [])
        if items:
            channel_info = items[0]['snippet']
            statistics = items[0]['statistics']

            print(f"👤 Channel Name: {channel_info['title']}")
            print(f"📷 Thumbnail: {channel_info['thumbnails']['default']['url']}")
            print(f"📊 Subscribers: {statistics.get('subscriberCount', 'N/A')}")
        else:
            print("⚠️ No YouTube channel found for this user.")
    else:
        print("❌ Could not fetch YouTube profile.")



@receiver(user_logged_in)
def add_user_to_loggedin_group(sender, request, user, **kwargs):
    group_name = 'LoggedInUsers'
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


@receiver([social_account_added, social_account_updated])
def save_linked_account(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    provider = sociallogin.account.provider  # 'google' or 'facebook'
    provider_account_id = sociallogin.account.uid  # unique id from provider

    # لو الحساب موجود بالفعل ما نضيفش نسخة جديدة
    LinkedAccount.objects.update_or_create(
        user=user,
        provider=provider,
        defaults={"provider_account_id": provider_account_id}
    )


@receiver(social_account_added)
def limit_social_accounts(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    provider = sociallogin.account.provider

    # Count how many accounts of this provider the user already has
    count = SocialAccount.objects.filter(user=user, provider=provider).count()

    if count > 2:  # Already has 2, prevent new one
        # Rollback this linking
        sociallogin.account.delete()
        raise ValidationError(
            f"You can only link up to 2 {provider.capitalize()} accounts."
        )


@receiver(user_logged_in)
def redirect_after_login(request, user, **kwargs):
    return redirect('/en/employeess/')