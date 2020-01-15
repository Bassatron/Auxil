# AUXIL

Auxil is a web application that connects people with volunteering opportunities.

## How To Use Web Application Demo
In order to view and use the Auxil web application, follow the steps below.
1. Clone the github repository to your local device
2. Install the required libraries and dependencies at the top of the app.py file
3. Navigate to where you cloned the repository
4. From the command line, type: `flask run`
5. Open web browser and navigate to "https://localhost:5000"


## Usage
Once you arrive at the Auxil homepage, you will have limited access to the web app's features. From the homepage you will be able to
search our database for opportunities near you. This will redirect you to a html table displaying general information about volunteering
opportunities in your city, or near your zipcode.

In order to access Auxil's full features, you must register for an account if you do not already have one. Your registration should
be confirmed by an email to your inputted address. (Note: No action is required from the email).

Once you are registered and logged into Auxil's webpage, you will be redirected to the homepage, and notice that you now have access to
several new features in the top left corner of the navbar. You now have full access to Auxil!
These features include:
    Explore: View a map centered at your location with markers showing what opportunities exist around you. You currently cannot click
             on the markers to view that markers information in an infoWindow, but we are working on implementing that feature.
             (NOTE: Geolocation functionality only works on secure connections via HTTS://...)
    Community: See what other members in Auxil's community have been up to! Here you can see comments that members have left about their
               experiences with Auxil, volunteering, and other topics, as well as the date of their posting.
    Register Org: Charities, Non-profits, and other organizations that provide volunteering opportunities can register their organization with
                  the Auxil database, so our members can start volunteering with them. Organizations just need to provide some basic information
                  about their work to register. We plan to continue iterating on this page to further validate organization's claims,
                  and have direct addition to the map feature.
    Apply to Vol: Users can select organizations they want to volunteer with, and their preferences. We are working to make Auxil
                  handle sending their information to the organizations, but due to limitations and the scope of this project we were
                  unable to currently partner with organizations to make this happen directly.
    Feedback: Users can leave feedback, stories and reviews of the organizations they have volunteered with the rest of the Auxil community.

That's the current state of our website!

## Support
If you run into any issues or are in need of further assistance please reach out to either justin_bassey@college.harvard.edu or
jacquelinepatel@college.harvard.edu

## Contribution
For those who want to make changes to the Auxil project, all of our code is completely open source, and free to use. Because Auxil
utilizes the google maps developers API, iterations on Auxil will require that hosts maintain a google developers API key. Furthermore,
Auxil is implemented to send emails to new users who sign up. This feature requires that you change the enviroment variable password
and add a new gmail address.

## Status
Dec-05-2018: Moved project to Github.

We hope to continue iterating and adding more functionality to our web application as we have time.

Optimally, our next step would be to change what happens with the applitions data. Right now, when a user submits an application to
an organization, it is simply put into a data table called applications. However, our next step would be creating a way for organizations
to access all of the applications which are relevant to their organization specifically. We would also like to implement slightly different
interfaces for organizations that use the website to post about themselves and find volunteers than volunteers looking for opportunities.
