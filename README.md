# Using Vagrant and Ansible to provision a two-tier Flask API

## Tech Stack
Ubuntu | Vagrant | Ansible | Python | PostgreSQL | ngrok
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![](images/ubuntu.png)  |  ![](images/vagrant.png)  | ![](images/ansible.png) | ![](images/python.png) | ![](images/postgres.png) | ![](images/ngrok.png)

## Motivation
Inspiration behind this project was fueled by mainly two areas; first is the desire to provide a simple workflow which allows developers, business analysts & testers to run their API calls against the same pre-alpha/alpha flask API server and be aligned with their UAT (User Acceptance Testing). The other area that motivated this project was the aspiration to increase familiarity with provisioning software(Vagrant/Oracle VM Box) and configuration management tools (Ansible).



## Proposed Architecture
![](images/flaskAPI-vagrant-ansible.png)

## Python Flask API (Port:5000)

In summary, these are the methods available on the Flask API
![](images/flaskAPI-methods.png)

The API was written initally with the default routing ```@app.get('/')``` convention. After finding out it doesn't fulfill RESTful best practices, the ```Flask RESTful``` python library was used and the codebase was refactored to include GET/POST methods within functions instead of routing. 

You may find more details from my [RESTful Flask API] github repository.

## PostgreSQL Database (Port: 5432)
There will be one users table in our PostgreSQL database storing details and account balance for our loyal user base. The fields available in our schema is shown below:
![](images/postgres-upay-table.png)

You may find more details from my [RESTful Flask API] github repository.


[RESTful Flask API]: https://github.com/hideyukikanazawa/restful-flask-api