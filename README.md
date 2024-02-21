## Flask_Python_api 

**Project Name:** Flask_Python_api

**Description:**

This project is a Python API built with Flask that allows interaction between two user roles: Client User and Ops User.

**Functionalities:**

* **Ops User:**
    * Upload files to a designated folder ("uploadedfiles")

* **Client User:**
    * Download uploaded files
    * View their own profile information
    * View uploaded files

**Features:**

* Uses in-memory database (SQLAlchemy) for user management and file metadata
* Stores uploaded files directly in a designated folder

**Target Audience:**

This project is designed for developers interested in creating simple file upload and download functionalities within a web application.

**Installation:**

1. Clone this repository or download the zip file.
2. Create a virtual environment (`python3 -m venv venv`) and activate it (`source venv/bin/activate`).
3. Install required dependencies: `pip install -r requirements.txt`.
4. Also create a folder named as 'uploadedfiles' if not exit.
5. Configure the database connection parameters in `config.py`.
6. Run the application: `python app.py`.

**Routes:**

* **http://127.0.0.1:5000/ (GET):** Checks the health of the server (basic response).
* **http://127.0.0.1:5000/signup (POST):** Allows user signup with details (uname, email, password). Requires a valid email address.
* **http://127.0.0.1:5000/signup (GET):** (Not recommended for production) Retrieves a list of all registered client users.
* **http://localhost:5000/userlogin (POST):** Allows client user login with credentials (uid, password) If email is verified.
* **http://localhost:5000/verify/<token> (GET):** Verifies a user account using a token sent via email.
* **http://localhost:5000/userlogin/listall/<id> (GET):** Lists all files available for download for a specific client user (identified by ID).
* **http://localhost:5000/opsuser (GET):** Retrieves information about the current logged-in Ops User (if logged in).
* **http://localhost:5000/opsuser (POST):** Processes Ops User sign-up with relevant details.

**Dependencies:**

* Flask
* Flask-SQLAlchemy
  

* This is a basic example and may require further customization for production use.
* Consider implementing security measures for user authentication and authorization.
* Explore alternative storage solutions for uploaded files beyond a local folder.

This updated readme includes the requested route details. Remember that exposing a route to retrieve all user information is not recommended for production due to security concerns. Consider implementing appropriate access control mechanisms for such routes.
