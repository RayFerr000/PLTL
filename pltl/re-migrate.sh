rm -r User/migrations
rm -r Assignment/migrations
rm -r Course/migrations
rm -r Homework/migrations
rm -r Class/migrations
rm -r Enrolled_Class/migrations
rm db.sqlite3
python manage.py makemigrations User
python manage.py makemigrations Assignment
python manage.py makemigrations Course
python manage.py makemigrations Homework
python manage.py makemigrations Class
python manage.py makemigrations Enrolled_Class
python manage.py migrate User
python manage.py migrate Assignment
python manage.py migrate Course
python manage.py migrate Homework
python manage.py migrate Class
python manage.py migrate Enrolled_Class
python manage.py migrate
