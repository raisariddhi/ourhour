# OurHour
OurHour is a simple, lightweight, and intuitive web-application to be used by students and TAs during office hours at universities. 

It's simplistic design aims to create an intuitive user-flow to increase usability and decrease the learning curve. Combined with a stong backend it creates a speedy and bug-less software to use on-the-go.

This project was developed over the course of a semester by the following people:
Raisa, Eric, Austin, Ritwick, Karim, Khalid

### Login Page
![image](https://github.com/raisariddhi/ourhour/assets/117309407/54a90043-60c7-4b97-a2b5-073fc71fed06)

### Office Ticket Submission
![image](https://github.com/raisariddhi/ourhour/assets/117309407/5bb7f891-b753-4228-9b2a-7b1814647e54)

### User Workflows
![image](https://github.com/raisariddhi/ourhour/assets/117309407/7a7cf0fd-794f-4d10-ba5d-bc31f0aee915)
![image](https://github.com/raisariddhi/ourhour/assets/117309407/c6c44497-f92a-44e4-b8a6-175f1e406e4e)
![image](https://github.com/raisariddhi/ourhour/assets/117309407/fe3b2a89-6a74-41ab-9971-2c58ca890720)
![image](https://github.com/raisariddhi/ourhour/assets/117309407/b01f7293-485a-4b4c-a3df-142b6273d7fa)

### Mappings & Mockups
![image](https://github.com/raisariddhi/ourhour/assets/117309407/83410341-2dc4-4bec-b20b-3e4cdf7b1abf)
![image](https://github.com/raisariddhi/ourhour/assets/117309407/000d5693-fdc1-475c-948a-fed67c266e83)
![image](https://github.com/raisariddhi/ourhour/assets/117309407/a0140aaa-f7a8-4039-8afb-4f0ab8423f31)

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
