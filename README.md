

# **Binge-Flix**


This is my 3rd Milestone Project for the Code Institute. It is a fully responsive site.

Binge-Flix is an App to allow its user's to keep rate and review TV Series from all streaming platforms.
Each user will have their own profile created upon registering. A user can edite or delete their own personal ratings or reviews.

The live version can be found [here.](http://binge-flix-project.herokuapp.com)


## **UX**


A responsive App. Allowing the user to review and rate TV series across all platforms. The 
user will also have their own profile, and record of reviews and ratings.

### **Target Users**  

* Users who like watching TV series
* Users who like to review TV seires
* Users who like to rate TV series
* Users who like to recomend what to watch
* Users Looking for new Series to watch and are looking for a recomendation 

### **User Stories**

* As a User I want a clean and clear Website
* As a User I want to be able to navigate around the site with ease
* As a User I want to be able to use the website with ease with clear messages
* As a User I want to be able to create an account
* As a user I want to find my account history
* As a User I want to edit my reviews
* As a User I want to delete my reviews
* As a User I want to be able to update my profile
* As a User I want to like or dislike reviewed shows
* As a User I want to be able to search shows by keywords
* As a User I want to able to use the site on different platforms

  

The Wireframes can be found [here](https://www.figma.com/file/5F65S2c3ZgqiyoLLFoxLgj/Binge-Flix?node-id=0%3A1).


## **Features**


### **Exsisting Features**

1. **landing Page** 
    * Title
    * About
    * Log In Button
    * Link to register if no account held
2. **Log In Page**
    * Form
    * Submit Button 
3. **Register Page**
    * Form for full details for profile
    * Submit Button
4. **My Profile** 
    * Shows what reviews the user has made
    * Edit Button on each show card
    * Delete Button on each show card
5. **Shows Trending Page**
    * Where the User can See all shows 
    * Users can see who posted each review
    * The user can search for reviews by show name
    * The user can like a review
    * the user can dislike a review 
7. **Add a Show Page**
    * Form for adding a show
    * Several Dropdown menus to choose platforms, genres and seasons
    * Submit Button
8. **Edit a Show Page**
    * Form for editing a show
    * Several Dropdown menus to choose platforms, genres and seasons
    * All Previous information is shown in the form that user previously entered
    * Submit Button
8. **Nav Bar**
    * So User can easily navigate the site
9. **Footer**
    * links to Social Media
    * Copyright
10. **Safety Modal**
    * Appears when the user is about to make changes, makes sure user is happy to proceed
11. **Search Bar**
    * User can search for shows by name

### **Future Features**
To be added in the future:

* Users to be able to comment on other users comments
* Users to like or dilike tose comments
* Users can click on the show to watch it.(Providing user has the appropriate apps)
* Users can link to sites like IMBD or wikipedia


## **Technologies**


### **Languages**
* HTML
* CSS
* JavaScript
* Python

### **Libraries & Frameworks**
* Flask
* jQuery
* PyMongo
* Jinja
* Materialize
* Werkzeug

### **Wireframes**
* Figma

### **Tools**
* [MongoDB](https://www.mongodb.com/) The Database
* [Heroku](https://heroku.com) Host for deployed site
* [GitHub](https://github.com) Repository
* [Gitpod](https://gitpod.io) Development
* [Freepik](https://www.freepik.com) Homepage Image
* [coolor.co](https://coolors.co) Color Palattes

## **Testing**

## **Deployment**

## **Issues**

* A problem when registering or logging in, there seemed to be connection problems with the database. I realised I used incorrect code for the submit button.
* Building the like button. I was incorrectly using the $inc operator, I had forgotten the qoutation marks.
* On Mobile the trending page did not look good with all the information. I decided to create a new page with for show details. The trending page will just have the title, Image and posted information


## **Credits**

### **Code**
* Code Institute Backend Developement Task Manager Project by Tim Nelson: I followed along to put in the basics and modified to suit my site.
### **Media**
* AWS: For the stock pictures used by users
### **Other**
### **Acknowledgements**
* My Mentor Precious
* Fatima, Sean, Michael, John & Jo From the Code Institute.
* 
