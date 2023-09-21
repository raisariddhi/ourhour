# OurHour
OurHour is a simple, lightweight, and intuitive web-application to be used by students and TAs during office hours at universities. 

It's simplistic design aims to create an intuitive user-flow to increase usability and decrease the learning curve. Combined with a stong backend it creates a speedy and bug-less software to use on-the-go.

This project was developed over the course of a semester by the following people:
Raisa, Eric, Austin, Ritwick, Karim, Khalid


## Logistics
We used Discord and Notion to conduct this project. 
Raisa: UI/UX Developer and Product Manager
Ritwick: Front-end development
Karim & Khalid: Network management (Docker and APIs)
Austin & Eric: Backend developnent (Data structures and databases)


## Build Instructions
`rebuild-dev.sh` builds the project using bind mounts at `./backend` and `./frontend` to their respective
directories in the containers. This means that any changes made to the container while it is running
will be manifested in your local directories. It's strongly recommended that you use this to build
while testing so that any progress made while the container is running is persisted in your local directory


`rebuild-prod.sh` builds the project as if for deployment. It copies your local directories into the container volume but the files
will not persist.

NOTE: `rebuild-dev.sh` and `rebuild-prod.sh` allows any user to access the directory that it is run in. This is necessary due to
permission issues on the CSL machines. I could not find any other workaround.


## License
MIT