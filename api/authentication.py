from __future__ import unicode_literals

from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.authtoken.models import Token
from api.models import App

__author__ = 'stefano'
class TokenAppAuthentication(BaseAuthentication):
    """
        App token authentication, modified from TokenBase Authentication

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

        Now the token is of the application, rather than of the user.
        Each user can have more than one application,
        with the app token here you get the owner and corresponding application
    """

    model = App
    """
        Change this with your model, has to have the field 'owner'
        or change the rest of the code accordingly
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        # here we pass the request, this is needed to add the app.
        # No better solution found so far
        return self.authenticate_credentials(auth[1], request)

    def authenticate_credentials(self, key,request):
        try:
            # get the app via key
            app = self.model.objects.get(token=key)
            # get the token via the app owner, which is a user
            token = Token.objects.get(user=app.owner)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        # not sure this is correct
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        # just in case,
        except Exception:
            raise exceptions.AuthenticationFailed('Not known')

        if not app.owner.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        # add the app to the request, is this correct?
        request.app=app
        # return user and token, don't know where this goes but it's required.
        return (app.owner, token)

    def authenticate_header(self, request):
        return 'Token'