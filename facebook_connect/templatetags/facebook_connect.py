from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
    
register = template.Library()
    
class FacebookClientScriptNode(template.Node):
    def render(self, context):

        scope = getattr(settings, "FACEBOOK_SCOPE", "email")
        redirect = getattr(settings, "FACEBOOK_LOGIN_REDIRECT", "/")

        facebook_app_id = settings.FACEBOOK_APP_ID
        channel_url = reverse('channel_url')

        params = {
            "scope":scope,
            "facebook_app_id":facebook_app_id,
            "channel_url":channel_url,
            "redirect":redirect
        }

        return """

<div id="fb-root"></div>
<script type="text/javascript"> 
    
    function facebook_login(){ 
        FB.login(function(response){
            send_response_to_server(response)
        }, {scope:"%(scope)s"}
       )
    }

    function facebook_connect(){
        FB.getLoginStatus(function(response) {

            if (response.status == "connected") {
                send_response_to_server(response);
            } else {
                facebook_login();
            }   

        });
    }

    function send_response_to_server(response){

        var ajax_data = {"access_token" : response.authResponse.accessToken,
                         "sig"          : response.authResponse.signedRequest,
                         "id"           : response.authResponse.userID}

        $.ajax({
            type:"POST",
            url: "/facebook_connect/facebook_connect/",
            dataType: "json",
            data: ajax_data,
            success: function(msg){
                window.location = "%(redirect)s";
            }
        })
    }

    window.fbAsyncInit = function() {
        FB.init({
            appId: '%(facebook_app_id)s',
            status : true,
            cookie: true,
            xfbml : true,
            channelURL : '%(channel_url)s'
        })
    };
    (function(d){
        var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement('script'); js.id = id; js.async = true;
        js.src = "//connect.facebook.net/en_US/all.js";
        ref.parentNode.insertBefore(js, ref);
    }(document));
</script>
""" % params

class FacebookLoginButtonNode(template.Node):
    def render(self, context): 
        return """

<input
    onclick="facebook_connect()"
    type="image"
    src="http://static.ak.fbcdn.net/images/fbconnect/login-buttons/connect_light_large_long.gif" alt="Facebook Connect" />
"""

def register_tag(tag_func):
    """
    Decorator for registering tags.
    """
    def new_tag_func(*args, **kwargs):
        return tag_func(*args, **kwargs)

    register.tag(tag_func)
    return new_tag_func

@register_tag
def facebook_script(parser, token): 
    return FacebookClientScriptNode()

@register_tag
def facebook_button(parser, token): 
    return FacebookLoginButtonNode()
