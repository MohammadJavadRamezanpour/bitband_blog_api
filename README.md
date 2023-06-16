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
- root user has no limitation in the system

## Installation
Follow these steps to set up and run the API locally:

1. Clone the repository:
  ```
  git clone  https://github.com/MohammadJavadRamezanpour/bitband_blog_api.git src
   ```
2. Create and activate a virtual enviroment
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
3. Install libraries
```
pip install -r requirements.txt
```
4. migrate
```
 python manage.py migrate
 ```
5. load initial data  in your db
```
python manage.py loaddata initital_fixture.json
```
## APIs
#### Register