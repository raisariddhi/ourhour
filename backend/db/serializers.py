from rest_framework import serializers

from .models import *

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # Include all fields in the serializer
        fields = ('ticket_id', 'desc',
                'phone', 'creation_time', 'finish_time',
                'status', 'length', 'course_id')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        # Include all fields in the serializer
        fields = ('course_id', 'start_time', 'end_time', 'instructors')
