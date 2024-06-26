# Vinea inventory-management
This is an inventory management system built upon a case study involving Vinea Wine Company. The project was carried out during an industrial engineering undergraduate project.

# How to Setup
1. Clone Project
```
git clone https://github.com/jacintho777/projet_pacte_4AGIL.git
```

2. Go To Project Directory
```
cd projet_pacte_4AGIL
```
3. Create Virtual Environment
```
python3 -m venv venv
```
4. Active Virtual Environment
   
Linux 
```
source venv/bin/activate
```
Windows 
```
venv\Scripts\activate
```
5. Install Requirements from txt file
```
pip install -r requirements.txt
```
6. Migrate Database
```
python manage.py migrate
```
7. Create Super User
```
python manage.py createsuperuser
```
8. Run Project
```
python manage.py runserver
```
