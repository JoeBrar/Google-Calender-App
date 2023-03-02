from django.shortcuts import redirect, render
from django.urls import reverse
from django.template import loader
from django.conf import settings
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

x = "a"


def authenticate_btn(request):
    template = loader.get_template('google_calendar/authenticate.html')
    return HttpResponse(template.render())


def google_authenticate(request):
    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'client_secrets.json'),
        scopes=['https://www.googleapis.com/auth/calendar'],
        #redirect_uri=request.build_absolute_uri(reverse('google_authenticate_callback')),
        redirect_uri=
        'https://My-Google-Calendar-App.joebrar.repl.co/google-authenticate-callback/',
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true',
    )
    request.session['google_auth_state'] = state
    print("hello")
    print(authorization_url)
    return redirect(authorization_url)


def google_authenticate_callback(request):
    global x
    state = request.session.get('google_auth_state', None)
    if state is None:
        return redirect(reverse('google_authenticate'))

    flow = Flow.from_client_secrets_file(
        os.path.join(settings.BASE_DIR, 'client_secrets.json'),
        scopes=['https://www.googleapis.com/auth/calendar'],
        #redirect_uri=request.build_absolute_uri(reverse('google_authenticate_callback')),
        redirect_uri=
        'https://My-Google-Calendar-App.joebrar.repl.co/google-authenticate-callback/',
        state=state,
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.user.google_oauth2_credentials = credentials.to_json()
    print(request.user.google_oauth2_credentials)
    #request.user.save()
    x = request.user.google_oauth2_credentials
    return redirect(reverse('my_calendar_view'))


def my_calendar_view(request):
    global x
    print("value of x is :" + x)
    #request.user.google_oauth2_credentials
    credentials = Credentials.from_authorized_user_info(
        json.loads(x),
        scopes=['https://www.googleapis.com/auth/calendar'],
    )
    try:
        service = build('calendar',
                        'v3',
                        credentials=credentials,
                        static_discovery=False)
        events = service.events().list(calendarId='primary').execute().get(
            'items', [])
    except HttpError as error:
        if error.resp.status == 401:
            # The user's credentials have been revoked. Reauthenticate the user.
            return redirect(reverse('google_authenticate'))
        else:
            raise

    return render(request, 'google_calendar/calendar.html', {'events': events})
