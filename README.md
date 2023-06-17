# Bitband Blog API

## Overview
This is a RESTful API for managing blog posts with a rich athentication and authorization architecture. It provides endpoints to create, read, update, and delete blog posts and users. The API is built using Django Rest Framework (DRF) and follows REST principles. the code level explanation is provided in [this youtube video](https://wait)


## Features
- Create a new article if you are an author or article manager
- Retrieve a list of the articles you wrote if you are an author
- Retrieve a list of the articles in your category if you are an article manager
- Retrieve a list of gold, bronze, silver or normal articles based on the level you purchase
- Retrieve a specific blog post if you are authorized
- Update an existing blog post if you are an author or article manager
- If you are an author you can only create article in you categories and edit your own articles, If you are an article manager beside creating article in your category, you can also verify, reject and edit them befor publish, this rule applies on edit too
- user managers can edit, block and grant permission to users
- root user has no limitation in the system, any api is available for him although I dont mention this in all apis

## Installation
Follow these steps to set up and run the API locally:

1. Clone the repository:
  ```
  git clone  https://github.com/MohammadJavadRamezanpour/bitband_blog_api.git src
  ```
2. Create and activate a virtual environment
	- On macOS and Linux:
  ```
  python3 -m venv env
  source env/bin/activate
  ```
	- On Windows:
  ```
  python -m venv env
  env\Scripts\activate
  ```
3. change directory to src folder
```
cd src
```
3. Install libraries
```
pip install -r requirements.txt
```
5. migrate
```
 python manage.py migrate
 ```
6. load initial data  in your db [Optional]
```
python manage.py loaddata initital_fixture.json
```
7. run server
```
python manage.py runserver
```
8. login to admin at /admin [Optional]
```
user: root
pass: 123
this password is for all users
```
## APIs
I will provide you with curl commands which you can run in your terminal.
##### make sure to set the proper parameters

#### Register
user will be registered using a phone number and after that he needs to verify his account usig the otp which will be sent (printed on the terminal) to his phone number
```
curl -i -X POST  -H "Content-Type:application/json"  -d  '{ "phone": "989226598743" }'  'http://127.0.0.1:8000/users/register/'
```
#### Verify the User
this happens after registeration
```
curl -i -X PATCH -H "Content-Type:application/json" -d '{"otp": "1234"}' 'http://127.0.0.1:8000/users/verify/?phone=989226598743'
```
#### Get OTP to Login
this will print the otp, or send the otp to the users phone number if you modify the __sms_otp method
```
curl -i -X PATCH \
   -H "Content-Type:application/json" \
   -d \
'' \
 'http://127.0.0.1:8000/users/get_otp/?phone=989226598743'
```
#### Send OTP to Login
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "phone": "989226598743",
  "otp": "1234"
}' \
 'http://127.0.0.1:8000/users/send_otp/'
 ```
 this will give you two json web tokens, one for access the other one is for refresh
 
 #### Login With Username and Password
 ```
 curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "username": "user_manager",
  "password": "123"
}' \
 'http://127.0.0.1:8000/auth/jwt/create/'
 ```
 again this gives you the json web tokens that you can use in the apis that need authorization
 #### Refresh the Json Web Token
 ```
 curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NzAyODc3NSwiaWF0IjoxNjg2OTQyMzc1LCJqdGkiOiI4Njk1NTUxZWI2ZTY0ZGFlOGJmMjYwZWVlNzViZWY4NiIsInVzZXJfaWQiOjE3fQ.WRriYKBPtzVk6C2t3DOdaLbQhep8Bb9vzFIPteb8ykU"
}' \
 'http://127.0.0.1:8000/auth/jwt/refresh/'
 ```
 of course you should replace  your own refresh token here
 #### Verify the Token
 ```
 curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDI4Nzc1LCJpYXQiOjE2ODY5NDIzNzUsImp0aSI6IjNjZWVlMTMwNmJiMDRlOGJiMjBhYzFlZjcyMTNmNDc1IiwidXNlcl9pZCI6MTd9.ygh_B1E-FCxadpklhIrdExmWm7Cw0WbImdKKCMtCCL8"
}' \
 'http://127.0.0.1:8000/auth/jwt/verify/'
 ```
 this will response 200 if the token is valid, otherwise 401
 #### List Users
 ```
 curl -i -X GET \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDI4Nzc1LCJpYXQiOjE2ODY5NDIzNzUsImp0aSI6IjNjZWVlMTMwNmJiMDRlOGJiMjBhYzFlZjcyMTNmNDc1IiwidXNlcl9pZCI6MTd9.ygh_B1E-FCxadpklhIrdExmWm7Cw0WbImdKKCMtCCL8" \
 'http://127.0.0.1:8000/users/'
 ```
 the list you get here depends on your access level, if the jwt you provide is for root user, you can get all users, if it's for user managers they can get all users, except those who are staff(those who access the admin panel and is_staff attribute is true for them), article managers can only get the authors in their category, other users can just list themselves.
 #### Modify Myself
 any user can edit these fields: phone, email, username, first_name, last_name.
 ```
 curl -i -X PATCH \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDMwNzA3LCJpYXQiOjE2ODY5NDQzMDcsImp0aSI6Ijg4MDg4ZmYwZTM5ZTQ2OTc5OWEzZDZhNDhhYzlkNmQ4IiwidXNlcl9pZCI6MTB9.aadsW6LUUpPM-Q0LAVlCN3pXcIgNfkJdjoEDYV9qfNI" \
   -H "Content-Type:application/json" \
   -d \
'{
  "phone": "789654123",
  "email": "something@otherthing.com",
  "username": "golden_user_new_username",
  "first_name": "Mohammad Javad",
  "last_name": "Ramezanpour"
}' \
 'http://127.0.0.1:8000/users/modify_me/'
 ```
 #### Modify Users
 this is only avaliable for user managers and root users.
 ```
curl -i -X PATCH \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDMxOTQ3LCJpYXQiOjE2ODY5NDU1NDcsImp0aSI6IjkzODdmNTMwYjJhYjRkNzE4NmUxZDkyZDkzM2ZiNjQ1IiwidXNlcl9pZCI6MTd9.ZW5NH3D4GV1XWNoUnNAMaC84EF_JkQzJD2fy8dk3X88" \
   -H "Content-Type:application/json" \
   -d \
'{
  "groups":[1, 2],
  "categories":[2, 3],
  "is_author": true
}' \
 'http://127.0.0.1:8000/users/30/'
 ```
 please note that any other field is possible to be edited here. but we made this user an author and granted the groups user_manager, article_manager and categories of workout and music to him.
 #### List Articles
 ```
 curl -i -X GET \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDMyNTM4LCJpYXQiOjE2ODY5NDYxMzgsImp0aSI6ImE4MTY2YmRhZTNhZTQ0YWNiYTY5YjI3OWRjNDM5MjJmIiwidXNlcl9pZCI6MTB9.NQItgTUEOEN49F2zyImGbHAHIkuC6E_9Q0rTo-rtdr0" \
 'http://127.0.0.1:8000/'
 ```
 article managers see all articles in their categories
 authors see their own articles
 golden users see all verified categories
 silver users see all verified normal, bronze and silver articles
 and so on for bronze and normal users
 anonymouse users see like normal users
 anybody see his own articles
  #### Create Articles
 ```
curl -i -X POST \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDMzNjk4LCJpYXQiOjE2ODY5NDcyOTgsImp0aSI6ImQzYTZjZjE5ZTE0YjQ3OTliNjAzM2NlZTE0MDBlOTI3IiwidXNlcl9pZCI6MTF9.FOA2FTO4azvmG0M2ZDuv3unGa1sHNgSbft2sgEuPmA0" \
   -H "Content-Type:application/json" \
   -d \
'{
  "title": "new article",
  "body": "this is the body",
  "scope": "bronze",
  "category": 1
}' \
 'http://127.0.0.1:8000/'
 ```
here a tech author is creating an article in technology category
#### Edit Articles
```
curl -i -X PATCH \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDMzNjk4LCJpYXQiOjE2ODY5NDcyOTgsImp0aSI6ImQzYTZjZjE5ZTE0YjQ3OTliNjAzM2NlZTE0MDBlOTI3IiwidXNlcl9pZCI6MTF9.FOA2FTO4azvmG0M2ZDuv3unGa1sHNgSbft2sgEuPmA0" \
   -H "Content-Type:application/json" \
   -d \
'{
  "title": "title changed",
  "scope": "golden"
}' \
 'http://127.0.0.1:8000/19/'
```
this is only available for authors and article managers, authors can edit their own articles and they are limited to title, body, scope and category fields, but article managers can edit any field of any article in their own category .
#### Verify or Reject Articles
```
curl -i -X PATCH \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDM0ODk0LCJpYXQiOjE2ODY5NDg0OTQsImp0aSI6ImRjMjEzY2NmYmQ5MjQ3MDViNWU3NmVlYjk5ZDdkNjQ1IiwidXNlcl9pZCI6MTR9.DvAxLUJCHM6CCLj5ikP2I2JjS0o0MRatlxC9V3lahU0" \
   -H "Content-Type:application/json" \
   -d \
'{
  "status": "verified"
}' \
 'http://127.0.0.1:8000/19/'
```
only article managers can do this in their own category, options are "verified", "rejected" and "pending"
#### Delete Articles
```
curl -i -X DELETE \
   -H "Authorization:Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3MDM0ODk0LCJpYXQiOjE2ODY5NDg0OTQsImp0aSI6ImRjMjEzY2NmYmQ5MjQ3MDViNWU3NmVlYjk5ZDdkNjQ1IiwidXNlcl9pZCI6MTR9.DvAxLUJCHM6CCLj5ikP2I2JjS0o0MRatlxC9V3lahU0" \
 'http://127.0.0.1:8000/19/'
```
this is going to delete article with id 19, and the user is an article manager, this is only available for article managers and authors
