from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _, get_language
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from allauth.socialaccount.models import SocialAccount
from .forms import PhoneLoginForm


from .models import (
    SocialMediaEmbed,
    Employee,
    Creator,
    EmployeeTablePluginModel,
    ConverterPluginModel,
    GoogleLoginPluginModel,
    TermsPluginModel,
    PrivacyPluginModel,
    FacebookLoginPluginModel,
    ContinueWithEmailPluginModel,
    TikTokLoginPluginModel,
    CMSPlugin
)


@plugin_pool.register_plugin
class EmployeeTablePlugin(CMSPluginBase):
    model = EmployeeTablePluginModel
    name = _("Employee Table Plugin")
    render_template = "employees/employee_table.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == "POST" and "delete_employee" in request.POST:
            employee_id = request.POST.get("delete_employee")
            employee = get_object_or_404(Employee, id=employee_id)
            employee.delete()
            return HttpResponseRedirect(request.path)
        context["employees"] = instance.get_employees()
        return context


@plugin_pool.register_plugin
class CurrencyConverterPlugin(CMSPluginBase):
    model = ConverterPluginModel
    name = _("Currency Converter")
    render_template = "employees/plugin.html"
    cache = False


@plugin_pool.register_plugin
class SocialMediaEmbedPlugin(CMSPluginBase):
    model = SocialMediaEmbed
    name = _("Social Media Embed")
    render_template = "employees/social_media_embed.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class TikTokProfilePlugin(CMSPluginBase):
    model = SocialMediaEmbed
    name = _("TikTok Profile Plugin (TEMP)")
    render_template = "employees/social_media_embed.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class FacebookProfilePlugin(CMSPluginBase):
    model = SocialMediaEmbed
    name = _("Facebook Profile Embed")
    render_template = "employees/social_media_embed.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class InstagramProfilePlugin(CMSPluginBase):
    model = SocialMediaEmbed
    name = _("Instagram Profile Embed")
    render_template = "employees/social_media_embed.html"
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


# Creator plugin model (بسيط وورث CMSPlugin)
class CreatorPluginModel(CMSPlugin):
    pass


@plugin_pool.register_plugin
class CreatorListPlugin(CMSPluginBase):
    model = CreatorPluginModel
    name = _("Creator List")
    render_template = "employees/creator_list.html"
    cache = False

    def render(self, context, instance, placeholder):
        return context

@plugin_pool.register_plugin
class GoogleLoginCMSPlugin(CMSPluginBase):
    model = GoogleLoginPluginModel
    name = _("Google Login Button")
    render_template = "employees/google_login.html"
    cache = False

    def render(self, context, instance, placeholder):
        request = context['request']
        user = request.user

        google_account = None

        if user.is_authenticated:
            google_account = SocialAccount.objects.filter(user=user, provider="google").first()

        context.update({
            "google_account": google_account,
            "user": user,
        })
        return context

@plugin_pool.register_plugin
class TermsPlugin(CMSPluginBase):
    model = TermsPluginModel
    name = _("Terms of Service Plugin")
    render_template = "employees/terms_plugin.html"
    cache = False



@plugin_pool.register_plugin
class PrivacyPlugin(CMSPluginBase):
    model = PrivacyPluginModel
    name = _("Privacy Policy Plugin")
    render_template = "employees/privacy.html"
    cache = False



# @plugin_pool.register_plugin
# class TikTokLoginCMSPlugin(CMSPluginBase):
#     model = TikTokLoginPluginModel
#     name = _("TikTok oLogin Button")
#     render_template = "employees/buttton.html"
#     cache = False

#     def render(self, context, instance, placeholder):
#         context['button_text'] = instance.button_text
#         return context




@plugin_pool.register_plugin
class FacebookLoginPlugin(CMSPluginBase):
    model = FacebookLoginPluginModel
    name = _("Facebook Login Button")
    render_template = "employees/facebook_login_plugin.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        user = request.user

        facebook_account = None

        if user.is_authenticated:
            facebook_account = SocialAccount.objects.filter(user=user, provider="facebook").first()

        context.update({
            "facebook_account": facebook_account,
            "user": user,
        })
        return context


@plugin_pool.register_plugin
class ContinueWithEmailPlugin(CMSPluginBase):
    model = ContinueWithEmailPluginModel  # link to the model
    module = _("Authentication")
    name = _("Continue with Email Button")
    render_template = "employees/button.html"
    cache = False

    def render(self, context, instance, placeholder):
    # Hardcode the URL as a safe fallback
        context['login_url'] = "/accounts/login/"
        context['button_text'] = instance.button_text
        return context



@plugin_pool.register_plugin
class PhoneSendPasswordPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Send SMS Password Form")
    render_template = "employees/send_password.html"
    cache = False

    def render(self, context, instance, placeholder):
        return context



@plugin_pool.register_plugin
class PhoneLoginCMSPlugin(CMSPluginBase):
    model = CMSPlugin
    render_template = "employees/login_form.html"
    name = _("Phone Number Login")
    cache = False  # مهم عشان التغييرات تبان مباشرة

    def render(self, context, instance, placeholder):
        request = context['request']

        if request.method == 'POST':
            form = PhoneLoginForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                # هنا تحطي منطق تسجيل الدخول الحقيقي
                print(f"Phone: {phone}, Password: {password}")  # للمراجعة
                # ممكن تعملي redirect أو تظهر رسالة نجاح
        else:
            form = PhoneLoginForm()

        context['form'] = form



@plugin_pool.register_plugin
class PhoneEnterPasswordPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Enter Password Form")
    render_template = "employees/enter_password.html"
    cache = False

    def render(self, context, instance, placeholder):
        # return context

        return context






