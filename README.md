﻿# Newspaper Agency

## Test user:
**Username:**
admin
**Password**
223344Aa


## Project Description

This is a Django web application for a newspaper agency. It allows for the management of newspapers, topics, and redactors. The application provides features such as creating, updating, and deleting newspapers, topics, and redactors.

## Installation

Follow these steps to install and run the project:

1. **Clone the repository**
    ```
    https://github.com/kstorozhenko/newspaper-agency.git
    ```
2. **Navigate to the project directory**
    ```
    cd newspaper_agency
    ```
3. **Create a virtual environment**
    ```
    python3 -m venv env
    ```
4. **Activate the virtual environment**
    - On Windows:
        ```
        .\env\Scripts\activate
        ```
    - On Unix or MacOS:
        ```
        source env/bin/activate
        ```
5. **Install the requirements**
    ```
    pip install -r requirements.txt
    ```
6. **Apply migrations**
    ```
    python manage.py migrate
    ```
7. **Run the server**
    ```
    python manage.py runserver
    ```

Now, you can access the application at `http://127.0.0.1:8000/`.

## Usage

The application provides the following endpoints:

- `/`: The home page which displays some statistics about the newspapers, redactors, and topics.
- `/topics/`: A list of all topics.
- `/topics/create/`: A form to create a new topic.
- `/topics/<int:pk>/`: The detail view of a topic.
- `/topics/<int:pk>/update/`: A form to update a topic.
- `/topics/<int:pk>/delete/`: A form to delete a topic.
- `/newspapers/`: A list of all newspapers.
- `/newspapers/<int:pk>/`: The detail view of a newspaper.
- `/newspapers/create/`: A form to create a new newspaper.
- `/newspapers/<int:pk>/update/`: A form to update a newspaper.
- `/newspapers/<int:pk>/delete/`: A form to delete a newspaper.
- `/redactors/`: A list of all redactors.
- `/redactors/<int:pk>/`: The detail view of a redactor.
- `/redactors/create/`: A form to create a new redactor.

Please note that only staff users can create, update, and delete topics, newspapers, and redactors.
