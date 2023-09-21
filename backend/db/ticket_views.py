from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta, date
from .models import Ticket, Course, Instructor
from .serializers import *

import json

class TicketView(APIView):
    def get(self, request, ticket_id):
        """
        Defines API for get request of a ticket
        @param request      The incoming request
        @param ticket_id    The ticket_id that was requested
        @return HTTP Response with status 200 for success and 404 if the ticket doesn't exist
        """
        # Make sure the ticket_id exists
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            # If it doesn't return 404 not found
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Initialize a serializer to format the ticket as json
        serializer = TicketSerializer(ticket)
        # return HTTP response 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, ticket_id):
        """
        Defines API for put request of a ticket
        @param request      The incoming request
        @param ticket_id    The ticket_id to be modified
        @return HTTP response with the appropriate status code.
        """
        # Make sure the ticket exists
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            # Return 404 if not
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Get the course object that the ticket belongs to
        course = ticket.course_id
        
        result = request.data
        # If the request is trying to modify the status of the ticket
        if 'status' in result:
            if ticket.status == 4 or ticket.status == 3:
                # Completed and cancelled tickets cannot be modified.
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if result['status'] == 2 or result['status'] == 3:
                # Only instructors can activate tickets and complete them
                
                if request.user.is_anonymous:
                    # The instructor has not logged in, unauthorized.
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                # Make sure the user is an instructor
                try:
                    instructor = request.user.instructor
                except ObjectDoesNotExist:
                    # Return forbidden if the user isn't an instructor
                    return Response(status=status.HTTP_403_FORBIDDEN)
                # Make sure the instructor belongs to the same course as the ticket does
                if not instructor.course_set.filter(course_id=course.course_id).exists():
                    return Response(status=status.HTTP_403_FORBIDDEN)
            ticket.status = result['status']
            if result['status'] == 3 or result['status'] == 4:
                ticket.finish_time = timezone.now()
        # Anyone can modify descriptions
        if 'desc' in result:
            ticket.desc = result['desc']
        if 'length' in result:
            ticket.length = result['length']

        ticket.save()    
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, ticket_id):
        """
        Defines API for delete request of a ticket
        @param request      The incoming request
        @param ticket_id    The ticket to be deleted
        @return             The appropriate HTTP status code
        """
        ticket = None
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            course = ticket.course_id
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instructor = request.user.instructor
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # Add comment clarifying next line
        c_id = course.course_id
        if not instructor.course_set.filter(course_id=c_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        ticket.delete()
        return Response(status=status.HTTP_200_OK)

    pass
            

        


class TicketCreateView(APIView):
    def post(self, request):
        """
        Defines post request API for ticket creation
        @param request  The incoming request
        @return HTTP Request with appropriate status code
        """
        # Construct a serializer based on the incoming request data
        serializer = TicketSerializer(data=request.data)
        # Validate the incoming data with the serializer
        if serializer.is_valid():
            if not request.data['status'] == 1:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    pass

class CourseView(APIView):
    
    def get(self, request, c_id, days):
        """
        Defines the API for the get request of a course.
        Returns tickets belonging to a course within a certain time range
        @param request      The incoming request
        @param c_id         The course whose tickets are to be retrieved
        @param days         How many days in the past to get tickets for
        @return             A list of tickets belonging to the course_id specified
        

        """
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            course = Course.objects.get(pk=c_id)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instructor = request.user.instructor
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # Add comment clarifying next line
        if not instructor.course_set.filter(course_id=c_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        if days == 0:
            tickets = Ticket.objects.filter(course_id=c_id)
        else:
            end_date = timezone.now()
            start_date = (end_date - timedelta(days=days-1)).date()
            tickets = Ticket.objects.filter(course_id=c_id).filter(creation_time__range=[start_date, end_date])
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    pass



class TicketWaitView(APIView):

    def get(self, request, ticket_id):
        """
        Defines API to estimate the wait time of a ticket
        Returns the ticket's place in line and estimated wait time
        @param request      The incoming request
        @param ticket_id    The ticket whose waiting time is to be estimated
        @return             The ticket's place in line and estimated wait time
        """
        # The user must be authenticated
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Try to get the ticket object for the ticket_id
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course = ticket.course_id
        c_id = course.course_id
        try:
            instructor = request.user.instructor
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if not instructor.course_set.filter(course_id=c_id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        # Get all of the tickets in the last week that are cancelled or complete
        end_date = timezone.now()
        start_date = (end_date - timedelta(days=7)).date()
        tickets = Ticket.objects.filter(course_id=c_id).filter(creation_time__range=[start_date, end_date])

        tickets = tickets.filter(status=4) | tickets.filter(status=3)
        serializer = TicketSerializer(tickets, many=True)
        long_total = 30;
        long_cnt = 1;
        med_total = 20;
        med_cnt = 1;
        short_total = 10;
        short_cnt = 1;
        wait = 0;
        
        for tick in serializer.data:
            if tick['length'] == 2:
                med_cnt += 1
                med_total += (parse_datetime(tick['finish_time'])
                        - parse_datetime(tick['creation_time'])).total_seconds() / 60
            elif tick['length'] == 1:
                short_cnt += 1
                short_total += (parse_datetime(tick['finish_time'])
                        - parse_datetime(tick['creation_time'])).total_seconds() / 60
            elif tick['length'] == 3:
                long_cnt += 1
                long_total += (parse_datetime(tick['finish_time'])
                        - parse_datetime(tick['creation_time'])).total_seconds() / 60
        tickets = Ticket.objects.filter(course_id=course).filter(status=1)
        serializer = TicketSerializer(tickets, many=True)
        for tick in serializer.data:
            if tick['length'] == 2:
                wait += med_total/med_cnt
            elif tick['length'] == 1:
                wait += short_total/short_cnt
            elif tick['length'] == 3:
                wait += long_total/long_cnt

        return Response({
            'minutes': wait,
            'line': len(serializer.data) - 1,
            }, status=status.HTTP_200_OK)


