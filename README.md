# rest-repo
Flask REST Service performing CRUD for a client


SQLAlchemy has been used as ORM.
Three tables Items,Stores and Users
All crud operations are done by SQLAlchemy

Flask-JWT-Extended used to manage tokens for logging in/out.

Deployed in http://139.59.33.251 digitalOcean Ubuntu server where Nginx is the reverse proxy.
uWSGI serves the application to Nginx through an internal socket.
