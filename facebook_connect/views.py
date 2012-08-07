import datetime
import hashlib
import hmac
import json
import base64

from facebook_python_sdk import facebook

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
    
from facebook_connect.models import FacebookUser

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def facebook_connect(request):
    """
    Create or connect a user via facebook connect.
    """
    try:
        access_token = request.POST["access_token"]
        user_id      = request.POST["id"]
        request_sig = request.POST["sig"]

        sig, expected_sig = get_sig_and_expected_sig(request_sig, settings.FACEBOOK_APP_SECRET)

        if sig == expected_sig:
            try:
                f_user = FacebookUser.objects.get(facebook_id=user_id)

            except FacebookUser.DoesNotExist:

                # Facebook api to get the user profile
                profile = facebook.GraphAPI(access_token).get_object('me')

                first_name  = profile["first_name"]
                last_name   = profile["last_name"]

                # Create the user
                user = User()
                user.save()

                user.username = u"fbuser_%s" % user.id
                user.first_name = first_name
                user.last_name = last_name

                # Attempt to set the email
                try:
                    if "email" in settings.FACEBOOK_SCOPE:
                        email = profile["email"]
                        user.email = email
                except AttributeError:
                    pass

                # Create the facebook user
                f_user = FacebookUser(facebook_id=user_id,
                                      contrib_user=user)

                # Set a password
                temp = hashlib.new('sha1')
                temp.update(str(datetime.datetime.now()))
                password = temp.hexdigest()

                user.set_password(password)
                f_user.contrib_password = password

                # Save
                f_user.save()
                user.save()
                        
            # Authenticate and login
            authenticated_user = auth.authenticate(username=f_user.contrib_user.username,
                                                   password=f_user.contrib_password)
            auth.login(request, authenticated_user)

        else:

            content = {
                "is_error" : True,
                "error_text" : "Error connecting facebook connect user %s " % (user_id)
            }

            return json_response(content, 200)
            
    except Exception, e:
        content = {
            "is_error" : True,
            "error_text" : "Error in ajax call, exception: %s" % e
        }

        return json_response(content, 200)
            

    content = {
        "is_error" : False,
        "error_text" : None
    }

    return json_response(content, 200)

def channel_url(request):
    """
    The channel file contains a script to the javascript sdk.
    This also prevents extra hits to the site (?fb_xd_fragment).
    """
    return render_to_response('channel.html')

def json_response(content, status=200):
    """
    Return a JSON response.
    """
    json_content = json.dumps(content)
    response = HttpResponse(json_content, status=status)
    return response

def base64_url_decode(inp):
    """
    Base64 decode.
    """
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def get_sig_and_expected_sig(signed_request, secret):
    """
    Returns the decoded sig and the expected sig.
    """
    parts = signed_request.split('.', 2)
    encoded_sig = parts[0]
    payload = parts[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    return sig, expected_sig
