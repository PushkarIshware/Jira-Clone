# Jira App

## Installation
1. Clone the repository:
    > git clone https://github.com/aub-recruitment/Pushkar-Ishware.git

    > cd Pushkar-Ishware

2. Build Project using Docker:
    > docker-compose build

    > docker-compose up
  
3.  Check server is running or not using URL:
    > http://127.0.0.1:8000/


## Create Super user for Django Application (Optional):
1. Open new terminal window and enter command:
    > docker ps

2. Copy NAME/ CONTAINER ID

3. Next enter command:
    > docker exec -it <NAME/CONTAINER ID> python manage.py createsuperuser

4. Enter Username, Email, Password and Password Again.

5. Finally hit y/Y.

6. Now you can access Django admin portal URL:
    > http://127.0.0.1:8000/admin

7. Enter Username and Password.

## How to Access API endpoints.

I have attached postman collection link below. It has section wised APIs.

Sequence of APIs are as follows:

    1. Account APIs
    2. Project APIs
    3. Task APIs
    4. Comment APIs

### Note 1: 
#### To get the JWT access token. Please access: 
  
  1. Account/signup API
  2. Account/signin API - (Here you will get a JWT Access Token)

### Note 2: 
  #### After getting JWT Access Token. Please store that Token in Authorization Header. (DO NOT ADD ANY Bearer/Token Prefix before the Token)

  > Example:

  > Authorization: randomelytypedwordsjusttolooklikeajwttoken 

### Finally
#### You can access all subsequent APIs.

##### How to import above collection in Postman: 
1. Copy above URL.

2. Open Postman Application.

3. Click on Import.

4. Paste the copied URL.



## Objective

Using the DRF (Django Rest Framework), create scalable and reliable backend REST APIs for a Jira-inspired project management platform.

## Tasks to Achieve

### Task-1: Authentication

- A user profile should have basic information, i.e., `Name`, `Bio`, `Picture`, and `Phone number`.
- Create necessary APIs for the following use cases.
  - A user should be able to register & login using Email & Password.
    - You can use Django’s built-in system or JWT to implement this.
    - No 3rd party ( Google, Github, … ) auth integration is required.
  - A user should be able to update profile information.

### Task-2: Projects

- A project should have basic information, i.e., `Title`, `Description`, `Owner`, `Members`, and `Tasks`.
- Create necessary APIs for the following use cases.
  - A user should be able to create a new project.
    - By default, a user creating a project should be that project's owner.
  - A user should be able to update and delete the self-owned projects.
    - The owner of a project cannot be updated once a project is created.
  - A user should be able to get the list of self-owned projects.
    - Add support of filters by a textual search parameter. The search should be applied to all the attributes of the blog.
    - Add support for pagination.
  - A user should be able to get the details of self-owned projects.

### Task-3: Tasks

- A task should have basic information, i.e., `Title`, `Description`, `Story Points`, `Assignee`, `Labels (multiple)`, and `Comments (multiple)`.
- Create necessary APIs for the following use cases.
  - A user should be able to create a task in a project if one is an owner or member of the project.
    - By default, a user creating a task should be that task’s assignee.
  - A user should be able to update a task in a project if one is an owner or member of the project.
  - A user should be able to delete a task in a project if one is an owner of the project.
  - A user should be able to get the list of tasks.
    - Add support of filters by `Projects (multiple)` and `Labels (multiple)`.
    - Add support of filters by a textual search parameter. The search should be applied to all the attributes of the blog.
    - Add support of pagination.
  - A user should be able to get the details of a task of self-owned projects.

### Task-4: **Task Comments**

- Create necessary APIs for the following use cases.
  - Add support for adding comments on a task.
    - A user should be able to add a comment on a task.
    - A user should be able to edit and delete self-created comments.
    - Add support of getting the list of comments for a particular task.
      - Add support of pagination.

## Submission

- Push your code to a this repository only and do not create your own repository.
- Update the `README.md` file with instructions on how to run your application.
