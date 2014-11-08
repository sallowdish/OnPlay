# CMPT470 Web-based Information System
## Group 3 Cryptonite 
## Final Project: ![logo](logo.png)Game Hosting System

# ![logo](logo.png)Game Hosting System  
<b>Game Hosting System</b> is a cloud-enabled, online-storage, Django powered Web-based Infomation System. Developers and game players are empowered with following features:
     - Online game hosting
     - Global leading board
     - Game-side chatroom
     - etc. 

# Version
    Current 1.0.0
    
# Demo
- A quick demonstration PDF can be found [here.](https://csil-git1.cs.surrey.sfu.ca/group3-cryptonite/final_project/raw/master/QuickDemo.pdf)

#About us
*    We a group of student from Simon Fraser University and dedicate ourselves to make people's life different with the technology and knowledge we have.
*    We are working as a team of 5 which called *Cryptonite"

# How to Start
  - Reposity: https://csil-git1.cs.surrey.sfu.ca/groups/group3-cryptonite
  - Local File Location: mx3:/home/share/final_project
  - Using ```$ git clone```to make a copy from repo to your own PC and modify the <code>settings.py</code> and <code>wsgi.py</code> to meet your local developing environment.
  - Run <code>$.manage.py runserver</code> to start the project locally
 
# Tips
  - Start a new branch before making any changes. 
    - [Create a new branch with git and manage branches.](https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches) You may will find this article is helpful.
  - You dont have to restart local server everytime you make some changes. Many changes will be reload automatically.
  - ```$ git merge ``` will make branch-based working very handly. But <b>DO NOT</b> ```PUSH/MERGE``` to master branch until you are sure your version really works.
  - If you add any static file like ```.js .css .jpg``` and etc. , you have to run ```$ ./manage.py collectstatic``` in order to make them ready in deployment evironment.


# Tech

<b>Game Hosting System</b> uses a number of open source projects to work properly:

* [Django](https://www.djangoproject.com/) - full stack Python-based framework for web apps!
* [Django REST Framework](http://www.django-rest-framework.org/) - awesome RESTful API framework
* [Jquery](http://jquery.com/) - a super convinient JavaScript library for runtime DOM selection
* [Bootstrap](http://getbootstrap.com/) - great UI boilerplate for modern web apps

# Todo's

 - Write Tests
 - Rethink Github Save
 - Add Code Comments
 - Add Night Mode

# Database Diagram
![DB Diagram](https://csil-git1.cs.surrey.sfu.ca/group3-cryptonite/final_project/raw/master/notfirstapp/DB/1.5/DB_1.5.png)


License
----
MIT
