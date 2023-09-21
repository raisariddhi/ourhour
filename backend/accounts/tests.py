from django.test import TestCase

from django.contrib.auth.models import User
import json

user_info1 = {
        'username': 'eric',
        'email': 'eric@eric.com',
        'password': '1_Really_good_password',
        're_password': '1_Really_good_password',
        }
user_info2 = {
        'username': 'khalid',
        'email': 'khalid@khalid.com',
        'password': '2_really_good_passwords',
        're_password': '1_Really_good_password',
        }

create_url = '/auth/users/'
token_url = '/auth/jwt/create'




class AuthTest(TestCase):
    def tearDown(self):
        User.objects.all().delete()
    def testCreate(self):
        """
        Test for successfully creating a User
        """

        response = self.client.post(
                create_url,
                user_info1,
                )
        self.assertEqual(response.status_code, 201)
        result = response.data
        user = User.objects.get(id=result['id'])
        self.assertEqual(user.email, user_info1['email'])

    def testLoginSuccess(self):
        """
        Successfully request a JWT token
        """
        
        # create a user
        response = self.client.post(
                create_url,
                user_info1,
                )
        self.assertEquals(response.status_code, 201)
        
        # request a token
        response = self.client.post(
                token_url,
                data={
                    'username': user_info1['username'],
                    'password': user_info1['password'],
                    });
        self.assertEquals(response.status_code, 200)
    def testLoginFail(self):
        """
        Unsuccessfully request a JWT token
        """
        
        # create a user
        response = self.client.post(
                create_url,
                user_info1,
                )
        self.assertEquals(response.status_code, 201)
        
        # request a token
        response = self.client.post(
                token_url,
                data={
                    'username': user_info1['username'],
                    'password': user_info2['password'],
                    });
        self.assertEquals(response.status_code, 401)

    
