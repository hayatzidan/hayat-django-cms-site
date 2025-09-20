from django.apps import AppConfig
from decouple import config


class EmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'


    def ready(self):
        import employees.signals  # make sure to import this



class MyAppConfig(AppConfig):
    name = 'cmsprojecct' 

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError
        try:
            # Google
            google_app, _ = SocialApp.objects.get_or_create(provider="google")
            google_app.client_id = config("GOOGLE_CLIENT_ID")
            google_app.secret = config("GOOGLE_CLIENT_SECRET")
            google_app.name = "Google Login"
            google_app.save()

            # Facebook
            fb_app, _ = SocialApp.objects.get_or_create(provider="facebook")
            fb_app.client_id = config("FACEBOOK_CLIENT_ID")
            fb_app.secret = config("FACEBOOK_CLIENT_SECRET")
            fb_app.name = "Facebook Login"
            fb_app.save()

            # TikTok
            tiktok_app, _ = SocialApp.objects.get_or_create(provider="tiktok")
            tiktok_app.client_id = config("TIKTOK_CLIENT_KEY")
            tiktok_app.secret = config("TIKTOK_CLIENT_SECRET")
            tiktok_app.name = "TikTok"
            tiktok_app.save()

        except (OperationalError, ProgrammingError):
            pass