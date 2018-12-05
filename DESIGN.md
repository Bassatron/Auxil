# Accessibility
Some features are out website are accessible only after making a account, but other features are accessible without registering or
logging in. In application.py, we made the distinction between these two type.The main features that are accessible without logging
in in application.py are the index page which is the defaul page "/" in application.py, the signup and the login features.

# Application.py
In application.py, we connect the html pages of our website with the SQL side. In our case, SQL is used to store the account data,
organization data, comment data, and application data.In application.py, the account data is connected to signup(), login() and change(),
where SQL stores the user data: id, first name, last name, email, and a hash of the user's password.The method in application.py called
signup creates a new user by adding entirely new information to the user data table in SQL. The Login method in application.py checks
to see if the inputted username and password exist already in the user table in SQL. Finally, the change method changes the password
stored with a specific username in the user table. The organization data table in SQL stores information on each volunteering opportunity.
The website has a capability of recieving data via POST in the html called add and the method in application.py called add() adds this
data to the organization table in SQL and then renders a list of all organizations by calling the method organizations() in application.py.
The comment data and applications data table work very similarly to this--where all the information inputed from users through the comment
or application webpage is stored in relevant data tables in SQL.

# Search function
The search function, accessible on the main page of the website even without logging in, has a feature where you can type in any
location or 5 digit zipcode and any volunteering opportunitities that are near you will appear on the list below. In our application.py,
the zipcode is cut down into just three digits and we search through the data table of organizations in SQL to see if there are any
zipcodes that also begin with those same three letters. If there are, then we display those results. By typing in an exact location,
we check to see if any organizations have that exact city listed.

# Map
The map funcionality is implemented through the google maps developers API. The map is implemented through primarily javascript in the
map.js static file. The primary function of map.js is the initMap function that is being called to render the map in "/explore.html".
This function is doing a few things. By default, it will render a google map center at Denver (Jacqueline & Justin's hometown), but
it use geolocation from googles developers documentation to find the user's current location and recenter the map around that area.
We then used a mashup of code from around the internet to create our plot markers function. The function plots markers at their given
lat, lng, and changes the pin color based on the type of opportunity.The last part of the map is the legend that we hard coded in, but
I think could have been more efficiently done.

# Helpers.py
The helpers.py file includes one main method used throughout the website called apology(). Apology is a method used when checking for
errors in python. When checking that an email has been entered when logging in, for instance, the application.py method called login() would first
check to see, using POST and request.form.get whether an email had been entered. If it had not been entered, application.py would
then call the apology method inside of helpers.py and send it a unique message specifically addressing what the problem is like
"must enter a username". This technique helps make our code more effcient because instead of writing new code to display an
apology text every time it is necessary in application.py,we simply do it once in helpers.py and pass in a unique text.

# Error Checking
We check for errors in our program two ways. First, in the html pages when users have the opportunity to entered in a piece of data,
we use the "required" tag. This will flash an error if the user attempts to move on without filling in that piece of the data. The more
widespread way that we check for errors is in application.py. Here, after using email = request.form.get("email") to retrieve a piece
of information, we check if not email to see if the email input actually has a piece of information attached to it or if the user did not enter anything.