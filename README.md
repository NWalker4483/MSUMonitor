# MSUMonitor

Automatically monitor and register for courses when availabilities arise
## Setup

To deploy locally create an ```auth.py``` in the root dir with the contents ...

``` python
# Provide your own Websis Login
username = "*********"
password = "*********"
```
* Run ```python3 -m pip install -r requirements.txt```
* Run the start.sh script or run ```python3 server.py```
* Go to [localhost:5000](http://localhost:5000) in your choice of browser.

A production deployment can also be accessed through [msu-register.glitch.me](https://msu-register.glitch.me)

For frontend use instructions please refer to the user manual in the [docs](docs/) folder
# Tasks
## General
* Implement Check ```WebsisSessionIsActive``` Function to check logins
* Implement course registration in ```register_for_course``` Function
* Implement more automated system and interface testing
* Check that all important operations/changes are logged (Use your personal descretion for what is important)
## Darius
* Set up somewhere for users to email the development team
## Nile
* Implement something to protect user data from program crashes
## Charnelle 
* Give users the option to remove/moniter a course subscription manually 
* 