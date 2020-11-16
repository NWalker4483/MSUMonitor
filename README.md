# AutoRegistration
Automatically monitor and register for courses when availabilities arise

# Tasks 
## General 
* Implement Check ```WebsisSessionIsActive``` Function to check logins
* Implement course registration in ```register_for_course``` Function
* Implement automated system and interface testing
* As it currently works sending notification emails blocks the program. In the future this should be done in a seperate thread.
* Check that all important operations/changes are logged (Use your personal descretion for what is important)
* Set up somewhere for users to email the development team
## Darius 
* Create Email Templates Files for various notifications 
* * Added_to_waitlist_with_registration.txt
* * Added_to_waitlist_without_registration.txt
* * Course_availability_found.txt # A spot was found but the user did not opt into automatic registration
* * Course_registration_successful.txt # A spot was available and taken
* * Course_registration_unsuccessful.txt # A spot is available and couldn't be taken i.e Prerequsite/ Major of study restrictions
* * Any other cases you can think of
## Nile 
* Write a script to keep the glitch project active or find another hosting service
* https://support.glitch.com/t/how-to-make-a-glitch-project-to-run-constantly/2439
## Charnelle 
* Give users the option to remove/moniter a course subscription manually 