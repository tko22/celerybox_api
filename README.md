# Grocery-Api
RESTful api for grocery app using [Django Rest Framework](http://www.django-rest-framework.org/).<br>
Note: we will move this repository to a separate user when we figure out a name
## Setup
We will create a virtual environment to evade conflicting dependencies:
```bash
pip install virtualenvwrapper
```
Then, put the following lines in your bash startup file(.zshrc, .bashrc, .profile, etc):
```bash
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/directory-you-do-development-in
source /usr/local/bin/virtualenvwrapper.sh
```
Create the environment:
```bash
mkdir -p ~/groceryapp && cd ~/groceryapp
mkvirtualenv groceryenv
```
Your shell should now be prepended with a (groceryenv). (your environment can be any name, not just "groceryenv")<br>
To exit environment, type: <b>deactivate</b>. <br>
To startup environment, type: <b>workon groceryenv</b> <br>
Now we need to install django and the django rest framework:
```bash 
pip install django
pip install djangorestframework
pip install markdown
```
Now confirm whether you have installed django:
```bash
which django-admin.py
```
The last step is to clone this repository(I will need your .ssh public key first though)
```bash
git clone
```
