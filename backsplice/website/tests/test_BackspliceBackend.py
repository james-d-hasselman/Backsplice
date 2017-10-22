from django.test import TestCase
from django.contrib.auth import get_user_model
from website.util.auth.backends import BackspliceBackend

class TestBackspliceBackend(TestCase):

    backsplice_backend = BackspliceBackend()
    UserModel = get_user_model()

    def setUp(self):
        self.backsplice_backend = TestBackspliceBackend.backsplice_backend
        self.UserModel = TestBackspliceBackend.UserModel
        
    def test_no_account_login(self):
        """
        Test attempting to login with incorrect user name and password.
        """

        result = self.backsplice_backend.authenticate('invalid', 'invalid')
        self.assertIsNone(result)

    def test_invalid_password_login(self):
        """
        Test attempting to login with a correct user name and incorrect 
        password.
        """

        user = self.UserModel.objects.create_user('test@no-replies.com', 
                                                  'test1')
        user.save()
        result = self.backsplice_backend.authenticate('test@no-replies.com', 
                                                      'test2')
        self.assertIsNone(result)

    def test_inactive_login(self):
        """
        Test attempting to login with valid credentials, but an inactive 
        account. 
        """

        user = self.UserModel.objects.create_user('test@no-replies.com', 
                                                  'test1')
        setattr(user, 'is_active', False)
        setattr(user, 'is_approved', False)
        user.save()
        result = self.backsplice_backend.authenticate('test@no-replies.com', 
                                                      'test1')
        self.assertIsNone(result)

        user = self.UserModel.objects.create_user('test2@no-replies.com', 
                                                  'test3')
        setattr(user, 'is_active', False)
        setattr(user, 'is_approved', True)
        user.save()
        result = self.backsplice_backend.authenticate('test2@no-replies.com', 
                                                      'test3')
        self.assertIsNone(result)

    def test_unapproved_login(self):
        """
        Test attempting to login with valid credentials, but an unapproved 
        account.
        """

        user = self.UserModel.objects.create_user('test@no-replies.com', 
                                                  'test1')
        setattr(user, 'is_active', False)
        setattr(user, 'is_approved', False)
        user.save()
        result = self.backsplice_backend.authenticate('test@no-replies.com', 
                                                      'test1')
        self.assertIsNone(result)

        user = self.UserModel.objects.create_user('test2@no-replies.com', 
                                                  'test3')
        setattr(user, 'is_active', True)
        setattr(user, 'is_approved', False)
        user.save()
        result = self.backsplice_backend.authenticate('test2@no-replies.com', 
                                                      'test3')
        self.assertIsNone(result)

    def test_valid_login(self):
        """
        Test attempting to login with valid credentials and an approved and 
        active account.
        """

        user = self.UserModel.objects.create_user('test@no-replies.com', 
                                                  'test1')
        setattr(user, 'is_active', True)
        setattr(user, 'is_approved', True)
        user.save()
        result = self.backsplice_backend.authenticate('test@no-replies.com', 
                                                      'test1')
        self.assertIsNotNone(result)

