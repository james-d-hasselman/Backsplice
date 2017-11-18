from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class BackspliceBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        else:
            # Always check everything to mitigate the possibility of 
            # malicious attackers timing authentication responses to identify 
            # valid user accounts
            is_valid_password = user.check_password(password)
            password = None # dump password from memory ASAP
            is_active = getattr(user, 'is_active', False)
            is_approved = getattr(user, 'is_approved', False)
            if is_active and is_approved and is_valid_password:
                return user
        return None

