from django.contrib.auth import backends, get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from .models import Profile

class AuthenticationBackend(backends.ModelBackend):
    def authenticate(self, request,  username=None, password=None, **kwargs):
        usermodel = get_user_model()
        print(usermodel)
       
        try:
            user = usermodel.objects.get(Q(username__iexact=username) | Q(
                email__iexact=username) | Q(profile__number__iexact=username))
            if user.check_password(password):
                return user
        except :
            pass




# class AuthBackend(object):
 

#     def get_user(self):
#        try:
#           return usermodel.objects.get()
#        except usermodel.DoesNotExist:
#           return None

#     def authenticate(self, username, password):
#         try:
#             user = usermodel.objects.get(
#                 Q(username=username) | Q(email=username)
#             )
#         except usermodel.DoesNotExist:
#             return None

#         return user if user.check_password(password) else None
