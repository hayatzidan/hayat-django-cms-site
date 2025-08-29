from allauth.socialaccount.models import SocialToken, SocialAccount
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_youtube_profile(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        token = SocialToken.objects.get(account=social_account)
        access_token = token.token
        creds = Credentials(token=access_token)
        youtube = build('youtube', 'v3', credentials=creds)

        request = youtube.channels().list(
            part="snippet,statistics",
            mine=True
        )
        response = request.execute()
        return response

    except Exception as e:
        print("❌ Error fetching YouTube data:", e)
        return None