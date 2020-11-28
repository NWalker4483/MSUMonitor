# MSU Monitor User Manual 
## Preface 
The purpose of this document is to guide users through the frontend of the MSU monitor system for a more technical description please refer to the requirements document appropriate for your version.
<img src="images/UI.png">

Our system borrows its frontend appearance from the [MSU Bursars Office Site](http://bursar.morgan.edu) for a more seamless integration into the MSU ecosystem.
<img src="images/uname.png">
This section is rather self-explanatory enter a valid MSU username and after validating it we'll send you an email with your subscription status
<img src="images/register.png">
```
For any version prior to 2.0 disregard this section as it is entirely disabled and ignored by the backend.
```
When attempting to enable automatic registration we require that the user enters a password and their alternate pin needed to access the registration page. When the "Attempt to register" button isnt select input in the password and altpin field is ignored and the inputs are disabled.

<img src="images/select.png">
Checking if a course exist on websis is a time intensive task in order to lighten the load here we provide a list of three Jquery+Json driven dropdowns which allow you to select any subject, course, and associated course number that is available in the semester.


```Note: Some of the wording and appearances in the images above may be inconsistent with the final version submitted. Though the order and function of the inputs will not.```