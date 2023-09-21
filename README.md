# OurHour


## Team Members/Roles

| Pair One | Pair Two | Pair Three |
| -------- | -------- | ---------- |
| Eric     | Raisa    | Karim      |
| Austin   | Ritwick  | Khalid     |

Project Owner: Eric

Scrum Master: Ritwick

## Logistics
[Discord Link](https://discord.gg/vdwtMCV5Xx)

[Kanban Board Invite](https://www.notion.so/invite/4e18c27965dceb552e8530782599b42ed4e53348)

## Build Instructions
`rebuild-dev.sh` builds the project using bind mounts at `./backend` and `./frontend` to their respective
directories in the containers. This means that any changes made to the container while it is running
will be manifested in your local directories. It's strongly recommended that you use this to build
while testing so that any progress made while the container is running is persisted in your local directory


`rebuild-prod.sh` builds the project as if for deployment. It copies your local directories into the container volume but the files
will not persist.

NOTE: `rebuild-dev.sh` and `rebuild-prod.sh` allows any user to access the directory that it is run in. This is necessary due to
permission issues on the CSL machines. I could not find any other workaround.


## TODO
1. Contribute to Requirement/Specification Document (located at reqs_specs.md in this repo)
2. Join Notion
3. Fill out this readme if you think of anything else
    
    
