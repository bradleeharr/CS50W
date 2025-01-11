# CS50W Project 2 - commerce

1. Make a virtual environment
    * `python -m venv .venv`
2. Activate the virutal environment
    * `.venv/Scripts/Activate` (Windows),    
    * or `source .venv/bin/activate` (Linux)

3. Make mirgations for the app
    * `python manage.py makemigrations auctions`

4. Apply migrations to database
    * `python manage.py migrate`


5. Run the server
    * `python manage.py runserver`