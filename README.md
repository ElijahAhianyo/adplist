# adplist

ADPList Take home assignment

This project implements the core backend logic of ADPList as a take home assignment.

## How it works.
The application contains two types of users:
- Mentor
- Member

### Mentor
A mentor can:
- register(after which they are rendered unapproved and need a superuser to approve them via `PATCH /mentors/{id}/approve`)
- sign in (Authentication uses JWT)
- create schedule. when a mentor creates a schedule, the available time is split into 30 minutes slots(created asynchronously).
- create appointment. An appointment can be scheduled between an approved mentor and a member.

### Member
A member can:
- register
- sign in
- read available slots for mentor
- book an appointment with a mentor.


# How to run

This project runs on docker. Run the following command:
`docker-compose -f local.yml --build up`. If everything goes on well(hopefully it does :) ), your application 
hould be accessible on port `8000`.

Go to `127.0.0.1:8000/api/docs/` to access the docs.

## What I would have done differently/better
Given the time constraints, I would revamp the schedules model to a more sophisticated one;
mentors can create different schedules for different days as well an option to recur a schedule. For eg. A schedule should 
be created for a period of time say 6 weeks. Also, I would add  Non-available days to schedule. This could have possible 
days such as holidays and vacation where mentor isnt available(this should also reflect in the slots).

I would also duplicate endpoints for members to create appointments, read mentor(Currently they exist only for the mentor)

I would also fix the broken test case in creating schedules. Currently, slots are created asynchronously (using celery) using a 
signal on the schedule. When a schedule is created, slots are created using Pandas rather than django. This choice was made because
Pandas is a lot faster and optimized than django in creating bulk records. However, for some strange reason, django seem to flush the data
in the test database which results in an integrity error since the schedule pk cant be found by sqlalchemy. To fix this, I would 
create a seed for testing rather than manually creating objects in the test setup.

I would also deploy the application to AWS, but I have exhausted my trial periods and Heroku doesnt look feasible to run for free after they updated their 
terms and conditions.



created by Elijah Ahianyo
