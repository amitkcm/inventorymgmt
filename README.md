# inventorymgmt
Install requirement.txt
You can create super user by going to inverntorymgmt folder & run the given command: python3 manage.py createsuperuser
To run server: python3 manage.py runserver
Now you can access the server at localhost:8000
For creating users, please login by admin by given link: localhost:8000/admin
for normal login you can go to link : localhost:8000/login

API
to get token login send postrequest with username and password at : localhost:8000/token/
now you will get token
pass that token in header and access api via postman or any other api request site at : localhost:8000/inv/
