# Django Bucket List Repository

Welcome to the **Django Bucket List** repository! This project is a web application built with Django that allows users to create and manage their bucket list items. A bucket list is a collection of goals, dreams, and experiences that a person aspires to accomplish in their lifetime. With this application, users can add, edit, and track their bucket list items, making it easier to stay focused on their life's objectives.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

The Django Bucket List project is designed to help users organize and prioritize their bucket list items effectively. Users can create an account, log in, and start adding their desired goals. Each item in the bucket list can have a title, description, target date, and status (e.g., in progress, completed). The application aims to provide a user-friendly interface and a seamless experience in managing one's bucket list.

## Features

- User authentication: Users can create accounts and log in securely.
- Create and manage bucket list items: Users can add new items to their bucket list, edit existing ones, mark them as completed, or remove them if they change their mind.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

<pre>
git clone https://github.com/giovanibs/django_bucket_list.git
</pre>

2. Change into the project directory:

<pre>
cd django_bucket_list
</pre>

3. It is recommended to set up a virtual environment before installing the project dependencies. You can use `venv` or `virtualenv`:

<pre>
# Using venv (Python 3)
python3 -m venv venv
source venv/bin/activate
</pre>

4. Install the required dependencies:

<pre>
pip install -r requirements.txt
</pre>

5. Apply the database migrations:

<pre>
python manage.py migrate
</pre>

6. Create a superuser account (an admin account) to manage the application:

<pre>
python manage.py createsuperuser
</pre>

7. Finally, run the development server:

<pre>
python manage.py runserver
</pre>

...or using gunicorn:

<pre>
gunicorn django_bucket_list.wsgi:application
</pre>

The application will be accessible at `http://localhost:8000/` in your web browser.

## Usage

- Access the application by navigating to `http://localhost:8000/` in your web browser.
- To start managing your bucket list, create a new account or log in if you already have one.
- Once logged in, you will be able to view your existing bucket list items or create new ones.
- Click on the add button to add a new goal to your bucket list.
- Edit or delete existing items by clicking on the respective options for each item.
- Mark items as completed when you achieve them.

## Contributing

Contributions to this project are welcome and encouraged! If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b my-feature`
3. Make changes and commit them: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin my-feature`
5. Submit a pull request explaining your changes.

Please ensure your code follows the project's coding conventions and includes relevant tests.

---

I hope you enjoy using the **Django Bucket List** application! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request. Happy bucket listing! 🚀
