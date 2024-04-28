# BookStoreAPI

A BookStoreAPI is an application programming interface (API) that facilitates communication between a client application and a bookstore's backend system. It serves as a bridge that allows software applications to interact with the bookstore's database, retrieve information, and perform various operations related to books and their management.
The BookStoreAPI typically follows the principles of Representational State Transfer (REST) architecture, meaning it uses standard HTTP methods like GET, POST, PUT, and DELETE to handle different types of requests and manipulate resources.

## Here are some key features and functionalities that a BookStoreAPI might offer:
-  Book Retrieval:
   The API allows clients to retrieve information about books, such as title, author, ISBN, genre, publication date, and synopsis.
-  Search and Filtering:
   Clients can perform searches based on specific criteria, like book title, author, genre, or keyword, to find relevant books.
-  Book Details:
   Clients can access detailed information about a particular book, including its availability, price, ratings, and reviews.
-  User Management:
   The bookstore has user accounts, the API might provide endpoints for user registration, login, and authentication.
-  Shopping Cart and Checkout:
   For online bookstores, the API could support adding books to a shopping cart and processing the checkout process.
-  Order History:
   The API give the permission to clients to retrieve information about past orders and transactions.
-  Reviews and Ratings:
   Clients might be able to submit reviews and ratings for books, as well as retrieve average ratings and reviews for each book.
-  Book Inventory Management:
   The API will include functionality to manage the bookstore's book inventory, such as adding new books, updating existing information, and 
   marking books as out of stock.
-  Security and Authorization:
   To protect sensitive data and ensure proper access control, the API will implement security measures like API keys or json web token for authentication.
-  Error Handling:
   The API will have proper error handling mechanisms to provide informative and consistent error responses to clients.


Getting Started
---------------

To run the API locally, follow these steps:

1.  Clone the repository: `git clone https://github.com/yourusername/BookStoreAPI_v1.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Go to .settings.DATABASES section, deactivate #PRODUCTION mode and activate #Development mode, add PostgreSQL configuration to connect to your database to be the default database.
6.  Change `.env.templates` to .env and setup you environment variables. 
7.  Set up the database: `python manage.py migrate`
8.  Create a superuser account: `python manage.py createsuperuser`
9.  Start the development server: `python manage.py runserver`


BookStoreAPI Organization
--------------------------
It's worth noting that Django's modularity allows us to create multiple applications to organize our code efficiently and keep related functionalities together. Breaking down this project into smaller, focused applications can make the codebase more maintainable, scalable, and easier to work with in the long run.

In a Django project for the BookStoreAPI, we typically need at least three main applications to organize the code and manage different functionalities in a modular way. Here's a breakdown of these three essential applications:

Core Application - the main project (or Main Application):
This application serves as the backbone of your project and contains settings, common functionalities, and global configurations. It may include features such as URL routing, project-wide settings, middleware, and base templates. The Core Application doesn't directly handle the specific functionality of the BookStoreAPI but provides the necessary infrastructure to support other applications.

User Application:
BookStoreAPI requires user management functionality, so we create a separate User Application. This application would handle user authentication, registration, login, and other user-related features. It may also include features like user profiles, password reset, and user-specific settings.

Book Application:
The Book Application handles all the functionalities related to books in the BookStoreAPI. This includes defining the models for books, creating views to handle book retrieval and manipulation, implementing forms for book-related data input, and managing book-related templates. The Book Application might also include features like book search, filtering, and sorting.

Of course, this is just a basic setup, and depending on the complexity of this BookStoreAPI project and the specific features we want to implement, we might need additional applications to handle different aspects. For example, we could have a separate application for handling shopping cart and checkout functionality when our API includes e-commerce features.

NOTE: you need this command to run celery in another terminal 
celery -A project worker --pool=solo  -l INFO