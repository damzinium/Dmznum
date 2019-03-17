# Damzinium
Codebase for Damzinium, an online learning platform designed to help students learn smarter.
## Development
### Pre-requesites
1. Ensure the latest version of python is installed i.e (v 3.x.x)
2. Ensure the latest version of virtualenv is installed. You can install it with the following command:
```
$ pip install virtualenv
```
### Setup
1. Create a virtual environment in the project directory.
Note: `venv` is used as the directory for the virtual environment because it is ignored by git. So please stick to it.
```
$ virtualenv venv
```
2. Activate the virtual environment
- Windows
```
> venv/Scripts/activate
```
- Linux
```
$ venv/bin/activate
```
3. Install required packages
```
$ pip install -r requirements.txt
```
4. You can run the development server and have fun developing
```
python manage.py runserver
```

## Staging
### Pre-requisites
1. Ensure the latest version of heroku CLI is installed.
2. Ensure that you are in your working directory.
3. Make sure you have commited all changes you want to push for staging

### Process
1. Add the remote repository for staging
```
$ heroku git:remote -a staging-damzinium
```
2. Push your commits
```
$ git push heroku master
```
3. You can test your changes at [www.staging-damzinium.herokuapp.com](http://staging-damzinium.herokuapp.com).

## Production
### Pre-requisites
1. Ensure the latest version of heroku CLI is installed.
2. Ensure that you are in your working directory.
3. Make sure you have commited all changes you want to push for production

### Process
1. Add the remote repository for production
```
$ heroku git:remote -a damzinium
```
2. Push your commits
```
$ git push heroku master
```
3. You can view your changes at [www.damzinium.herokuapp.com](http://damzinium.herokuapp.com).

## Note
Please be reminded to update our standard Github remote repository with successful updates.

## Thanks
