from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Ticket, Course, Instructor
import json

user_name = 'auth_tester'
pass_word = 'good_password_here'
user2 = "user2"
pass2 = "password_lol"


class TicketTest(TestCase):
    def setUp(self):
        """
        For every test:
            Create 2 users and assign one to a "scott" instructor
            Create an instructor called scott and associate it with a user
            Create two courses, CS506 and CS537
            Assign scott to CS537
        """
        test_user = User.objects.create(username=user_name)
        test_user.set_password(pass_word)
        test_user.save()
        test_user2= User.objects.create(username=user2)
        test_user2.set_password(pass2)
        test_user2.save()
        scott = Instructor(user=test_user)
        scott.save()
        cs506 = Course(course_id='CS506')
        cs506.save()
        cs506.instructors.add(scott)
        cs506.save()
        cs537 = Course(course_id='CS537')
        cs537.save()
    def tearDown(self):
        Ticket.objects.all().delete()

    def addTicket(self, desc, course_id):
        """
        Adds a valid ticket with dummy values except for those provided

        @param desc         The description of the ticket
        @param course_id    The course_id (string) of the course the ticket belongs to
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': desc,
                    'phone': '5555555555',
                    'status': 1,
                    'length': 1,
                    'course_id': course_id,
                    }),
                content_type='application/json',
                )
        return response

    def authenticate(self, u, p):
        """
        Acquire a JWT access token
        @param u    username
        @param p    password
        """
        response = self.client.post('/auth/jwt/create/',
                data=json.dumps({
                    'username': u,
                    'password': p,
                    }),
                content_type='application/json',
                )
        result = json.loads(response.content)
        self.assertTrue("access" in result)
        return result["access"]
    
    def testBadStatus(self):
        """
        If a post specifies a status it must be 1
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 0,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 2,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 3,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 4,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 1,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 201)

    def testBadLength(self):
        """
        If a post specifies a length it must be 1-3
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5555555555',
                    'status': 1,
                    'length': 0,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)    
 

    def testBadPhone(self):
        """
        Phone numbers should have the correct format
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '5d55555555',
                    'status': 1,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

    def testBadCourse(self):
        """
        CourseID must refer to an existing course
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'desc': 'desc',
                    'phone': '555555555',
                    'status': 1,
                    'length': 1,
                    'course_id': 'NONEXISTINGCOURSEID',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

    def testNoDesc(self):
        """
        Tickets must have a description
        """
        response = self.client.post('/api/tickets/',
                data=json.dumps({
                    'phone': '555555555',
                    'status': 1,
                    'length': 1,
                    'course_id': 'CS506',
                    }),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

    def testGet(self):
        """
        Anyone can view a ticket if they have its ticket id
        Authenticated instructors are allowed to view all the
        tickets for any course they belong to
        """
        response = self.addTicket("one", "CS506")
        self.assertEquals(response.status_code, 201)
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        # get the ticket that was just added
        response = self.client.get(f'/api/tickets/{ticket_id}/',
                content_type='application/json'
                )
        # Should be a success
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content)
        # Make sure the data is correct
        self.assertEquals(result["desc"], "one")
        self.assertEquals(result["course_id"], "CS506")


        response = self.addTicket("two", "CS506")
        self.assertEquals(response.status_code, 201)
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        # Get the ticket that was just added
        response = self.client.get(f'/api/tickets/{ticket_id}/',
                content_type='application/json'
                )
        # Should be a success
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content)
        # Make sure the data is correct
        self.assertEquals(result["desc"], "two")
        self.assertEquals(result["course_id"], "CS506")

        response = self.addTicket("three", "CS537")
        self.assertEquals(response.status_code, 201)
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        # Get the ticket that was just added
        response = self.client.get(f'/api/tickets/{ticket_id}/',
                content_type='application/json'
                )
        # Should be a success
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content)
        # Make sure the data is correct
        self.assertEquals(result["desc"], "three")
        self.assertEquals(result["course_id"], "CS537")


        # Get an access token for an instructar that isnt in CS506
        bad_token = self.authenticate(user2, pass2)
        
        # Try to get a list of all of the tickets for CS506 without authenticating

        response = self.client.get('/api/tickets/course/CS506/0/',
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 401)
        
        # Try to get a list of all of the tickets for CS506 with the wrong access token

        response = self.client.get('/api/tickets/course/CS506/0/',
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {bad_token}'
                )
        self.assertEquals(response.status_code, 403)
        # Get an access token for an instructor for CS506
        token_506 = self.authenticate(user_name, pass_word)
        # Try to get a list of all of the tickets for CS506 with the correct access token

        response = self.client.get('/api/tickets/course/CS506/0/',
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {token_506}'
                )
        self.assertEquals(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEquals(len(result), 2)
        for data in result:
            self.assertNotEqual("three", data['desc'])


    def testCancel(self):
        """
        Anyone can cancel a ticket if it is active or waiting
        Once a ticket is cancelled it is permanent, it cannot be
        changed again.
        """
        response = self.addTicket("test", "CS506")
        self.assertEquals(response.status_code, 201);
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        # The user cancelled their ticket, should be a success
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':4}),
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 200)

        # The next three puts should return 400, because ticket cancellations are permanent
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':2}),
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':1}),
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 400)

        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':3}),
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 400)
        # Make another test ticket
        response = self.addTicket("test", "CS506")
        self.assertEquals(response.status_code, 201);
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        
        # Set the new ticket to active
        # First get an auth token
        token = self.authenticate(user_name, pass_word)
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':2}),
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {token}'
                )
        self.assertEquals(response.status_code, 200)
        # Active tickets can be cancelled by Anyone

        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':4}),
                content_type='application/json'
                )
        self.assertEquals(response.status_code, 200)
        
        pass
    def testActivateComplete(self):
        """
        Only instructors who belong to a course can activate its tickets.
        Only instructors who belong to a course can mark its tickets as complete
        Marking a ticket as complete is permanent
        """
        # Make a test ticket
        response = self.addTicket("test", "CS506")
        self.assertEquals(response.status_code, 201);
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        

        # Try to change its status without authenticating
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':2}),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 401)       

        # Now try to activate it with the wrong instructor
        bad_token = self.authenticate(user2, pass2)
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':2}),
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {bad_token}'
                )
        self.assertEquals(response.status_code, 403)

        # Now try after authenticating with the correct instructor
        token = self.authenticate(user_name, pass_word)
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':2}),
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {token}'
                )
        self.assertEquals(response.status_code, 200)
        # Try to mark the ticket as complete without authenticating

        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':3}),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 401)

        # Try to complete the ticket as the wrong instructor
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':3}),
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {bad_token}'
                )
        self.assertEquals(response.status_code, 403)

        # Now try while authenticated with the correct instructor
       
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':3}),
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {token}'
                )
        self.assertEquals(response.status_code, 200)
    
        response = self.client.put(f'/api/tickets/{ticket_id}/',
                data=json.dumps({'status':1}),
                content_type='application/json',
                )
        self.assertEquals(response.status_code, 400)

    def testDelete(self):
        """
        Instructors who belong to a course can delete its tickets
        """
        # Make a test ticket
        response = self.addTicket("one", "CS506")
        self.assertEquals(response.status_code, 201);
        result = json.loads(response.content)
        ticket_id_1 = result["ticket_id"]
        # Make another ticket
        response = self.addTicket("two", "CS506")
        self.assertEquals(response.status_code, 201);
        result = json.loads(response.content)
        ticket_id = result["ticket_id"]
        # Leave it as waiting
        bad_token = self.authenticate(user2, pass2)
        # Try to delete without authenticating
        response = self.client.delete(f'/api/tickets/{ticket_id_1}/')
        self.assertEqual(response.status_code, 401)
        # Try to delete as the wrong Instructor
        response = self.client.delete(f'/api/tickets/{ticket_id_1}/',
                HTTP_AUTHORIZATION=f'Bearer {bad_token}')
        self.assertEqual(response.status_code, 403)
        # Try to delete as the correct instructor
        token = self.authenticate(user_name, pass_word)
        response = self.client.delete(f'/api/tickets/{ticket_id_1}/',
                HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        
        # Get a list of all of the tickets for CS506 with the correct access token

        response = self.client.get('/api/tickets/course/CS506/0/',
                content_type='application/json',
                HTTP_AUTHORIZATION=f'Bearer {token}'
                )
        self.assertEquals(response.status_code, 200)

        result = json.loads(response.content)
        self.assertEquals(len(result), 1)
        self.assertEqual("two", result[0]['desc'])

    def testListCourseOneDay(self):
        cs506 = Course.objects.get(pk="CS506")
        today = Ticket()
        today.desc = 'today'
        today.phone = '5555555555'
        today.course_id = cs506
        today.save()
        yesterday = Ticket()
        yesterday.desc = 'yesterday'
        yesterday.phone = '5555555555'
        yesterday.course_id = cs506
        yesterday.save()
        yesterday.creation_time = timezone.now() - timedelta(days=1)
        yesterday.save()
        token = self.authenticate(user_name, pass_word)
        url = '/api/tickets/course/CS506/1/'
        response = self.client.get(url,
                HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200)
        
        result = json.loads(response.content)
        self.assertEquals(len(result), 1)
        self.assertEquals("today", result[0]['desc'])

    def testEstimateWaitSuccess(self):
        """
        Generates old finished tickets and verifies that the correct time estimation is returned
        """
        cs506 = Course.objects.get(pk="CS506")
        short_count = 1
        short_total = 10
        med_count = 1
        med_total = 20 
        long_count = 1
        long_total = 30
        for i in range(30):
            old_ticket = Ticket()
            old_ticket.desc = 'old'
            old_ticket.phone = '5555555555'
            old_ticket.course_id = cs506
            old_ticket.status = 3
            old_ticket.length = 1
            old_ticket.creation_time = timezone.now() - timedelta(minutes=15)
            old_ticket.finish_time = timezone.now()
            old_ticket.save()
            short_count += 1
            short_total += 15

        for i in range(30):
            old_ticket = Ticket()
            old_ticket.desc = 'old'
            old_ticket.phone = '5555555555'
            old_ticket.course_id = cs506
            old_ticket.length = 2
            old_ticket.status = 3
            old_ticket.creation_time = timezone.now() - timedelta(minutes=25)
            old_ticket.finish_time = timezone.now()
            old_ticket.save()
            med_count += 1
            med_total += 25

        for i in range(30):
            old_ticket = Ticket()
            old_ticket.desc = 'old'
            old_ticket.phone = "5555555555"
            old_ticket.course_id = cs506
            old_ticket.length = 3
            old_ticket.status = 3
            old_ticket.creation_time = timezone.now() - timedelta(minutes=35)
            old_ticket.finish_time = timezone.now()
            old_ticket.save()
            long_count += 1
            long_total += 35
        short = short_total/short_count
        med = med_total/med_count
        long = long_total/long_count

        wait = 0
        for i in range(10):
            new = Ticket()
            new.desc = 'old'
            new.phone = "5555555555"
            new.course_id = cs506
            new.length = 1
            new.save()
            wait += short
        for i in range(10):
            new = Ticket()
            new.desc = 'old'
            new.phone = "5555555555"
            new.course_id = cs506
            new.length = 2
            new.save()
            wait += med
        for i in range(10):
            new = Ticket()
            new.desc = 'old'
            new.phone = "5555555555"
            new.course_id = cs506
            new.length = 3
            new.save()
            wait += long

        response = self.addTicket('test', 'CS506')
        self.assertEquals(response.status_code, 201)
        wait += short
        ticket_id = response.data['ticket_id']
        token = self.authenticate(user_name, pass_word)
        response = self.client.get(f'/api/tickets/wait/{ticket_id}/',
                        HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['line'], 30)
        self.assertAlmostEquals(response.data['minutes'], wait, places=4)
