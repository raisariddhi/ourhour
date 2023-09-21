#Based on the provided documentation and the code in ticket_views.py, here is the information for each endpoint:
#GET /tickets/int:ticket_id/
#Retrieves a ticket by ID.
#Request
#Method: GET
#Endpoint: /tickets/<int:ticket_id>/
#URL parameters:
#ticket_id (integer): the ID of the ticket to retrieve
#Headers:
#None
#Body:
#None
#Response
#Status code: 200 OK or 404 Not Found
#Body:
#If the ticket exists:
#{
#    "id": integer,
#    "title": string,
#    "description": string,
#    "created_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#    "updated_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#    "status": string,
#    "course_id": integer
#}
#If the ticket does not exist:
#{
#    "detail": "Not found."
#}

#POST /tickets/add/
#Creates a new ticket.
#Request
#Method: POST
#Endpoint: /tickets/add/
#URL parameters:
#None
#Headers:
#Content-Type: application/json
#Body:
#{
#    "title": string,
#    "description": string,
#    "status": string,
#   "course_id": integer
#}
#Response
#Status code: 201 Created or 400 Bad Request
#Body:
#If the request is valid:
#{
#   "id": integer,
#    "title": string,
#    "description": string,
#    "created_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#    "updated_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#    "status": string,
#   "course_id": integer
#}
#If the request is invalid:
#{
#    <field_name>: [
#        <error_message>,
#        ...
#    ],
#    ...
#}

#GET /tickets/course/<c_id>/<int:days>/
#Retrieves a list of tickets for a course within a time range
#0 days to get all tickets
#Request
#Method: GET
#ndpoint: /tickets/course/<c_id>/<int:days>/
#URL parameters:
#c_id (string): the ID of the course to retrieve tickets for
#days (int): The number of days in the past to get tickets until (1 for just today)
#Headers:
#None
#Body:
#None
#Response
#Status code: 200 OK
#Body:
#[
#    {
#        "id": integer,
#        "title": string,
#        "description": string,
#        "created_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#        "updated_at": string,  # format: "YYYY-MM-DDTHH:MM:SSZ"
#        "status": string,
#        "course_id": integer
#    },
#    ...
#]
#If there are no tickets for the course, the response will be an empty list [].
#Note: Only instructors of a course are permitted to get a list of all tickets for that course. If the user is not authenticated, the response will be a 401 Unauthorized status code.
from django.urls import path

from .ticket_views import *

urlpatterns = [
        path('tickets/<int:ticket_id>/', TicketView.as_view()),
        path('tickets/course/<c_id>/<int:days>/', CourseView.as_view()),
        path('tickets/', TicketCreateView.as_view()),
        path('tickets/wait/<int:ticket_id>/', TicketWaitView.as_view()),
        ]
