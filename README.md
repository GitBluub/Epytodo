# Epytodo
To-Do list REST API with Flask

# How to setup?
Install the virtualenv using the script setup_virtualenv.sh at the root.

Setup the database using your mysql user as 
```
cat epytodo.sql | mysql -u "USER" -p
```
then entering your password.

Modify config.py in order to enter the mysql database as your own user.

# Run the app :

To enter virtualenv
```
source bin/activate
```

Inside the virtualenv
```
python run.py
```

Site is available at localhost port 5000
