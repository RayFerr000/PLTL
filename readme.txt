Read Me
=======

Install Virtual Environment
...........................
...........................

pip install virtualenv


Creating virtual environment and installing packages
....................................................
....................................................

Go to the project folder yourname-pltl

RUN
$ su
Enter the super user password..


Create, Activate and Install the packages
-----------------------------------------

Run the install.sh file
$ sh install.sh

Check the packages that are installed
-------------------------------------
$ pip freeze


Install NPM:
...........
...........

$ curl http://nodejs.org/dist/node-latest.tar.gz | tar xvz
$ cd node-v*
$ ./configure --prefix=$VIRTUAL_ENV
$ make install

It will take much time installing npm
