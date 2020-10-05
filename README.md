# AutoRegistration
Automatically monitor and register for courses when availabilities arise

```pip install -r requirements.txt```

```python server.py```

# Tasks 
* Create Gmail account for software
* Implement Email sending capability
* Create Email Templates Files for various notifications 
* * Added_to_waitlist_with_registration.txt
* * Added_to_waitlist_without_registration.txt
* * Course_availability_found.txt # A spot was found but the user did not opt into automatic registration
* * Course_registration_successful.txt # A spot was available and taken
* * Course_registration_unsuccessful.txt # A spot is available and couldn't be taken i.e Prerequsite/ Major of study restrictions
* * Any other cases you can think of
  
* Implement Check ```WebsisSessionIsActive``` Function to check logins
* Implement Scraping of Available Courses in ```get_available_courses``` Function  
* Implement Scraping of term id
* Implement course registration in ```register_for_course``` Function
* Make automatic registration optional
* * In its current state auto registration requires that the user enter password to moniter a course, This password is not actually required for monitoring and only for registration by making the registration feature optional we make our software more accessible to users uncomfortable giving us their passwords.