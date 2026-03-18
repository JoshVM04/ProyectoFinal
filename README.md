# Nómada - Costa Rica Travel Platform 🇨🇷

Nómada is a web platform that recommends tourist destinations in Costa Rica. Users can explore places by category (Beaches, Parks, Adventure, Hot Springs), read and post experiences, and get personalized recommendations from an AI assistant.

________________________________

##  Features

### For Visitors
- Browse destinations by category
- View detailed information about each destination
- Read comments and ratings from other travelers
- Use the AI chat assistant for recommendations
- Register a new account

### For Registered Users
- Log in to access profile
- Post comments about destinations
- Rate destinations (1-5 stars)

### For System Owner
- Add new destinations
- Edit destination information
________________________________

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend programming language |
| Flask | Web framework |
| MySQL | Database |
| SQLAlchemy | ORM (Object-Relational Mapping) |
| HTML/CSS/JavaScript | Frontend |
| Tailwind CSS | Styling |
| DeepSeek API | AI chat assistant |
| GitHub | Version control |

________________________________

## 📁 Project Structure
ProyectoFinal/
├── app/
│ ├── init.py
│ ├── models/
│ │ ├── usuario.py
│ │ ├── destino.py
│ │ └── comentario.py
│ ├── routes/
│ │ ├── main.py
│ │ ├── auth.py
│ │ ├── destinos.py
│ │ ├── experiencias.py
│ │ └── ia_chat.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── auth/
│ │ ├── destinos/
│ │ └── ia_chat.html
│ ├── static/
│ │ ├── css/
│ │ ├── js/
│ │ └── images/
│ └── utils/
├── config.py
├── run.py
├── requirements.txt
└── README.md

________________________________

##  Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git

### Step 1: Clone the repository
```bash
git clone https://github.com/JoshVM04/ProyectoFinal.git
cd ProyectoFinal

________________________________

Step 2: Create and activate virtual environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

________________________________

Step 3: Install dependencies

pip install -r requirements.txt

________________________________

Step 4: Configure MySQL
Create a database named nomada_db:

mysql -u root -p
CREATE DATABASE nomada_db;
EXIT;

________________________________

Step 5: Create config.py
python
import os

class Config:
    SECRET_KEY = 'nomada-secret-key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:TU_CONTRASEÑA@localhost/nomada_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

________________________________

Step 6: Run the application


python run.py
Open your browser and go to: http://127.0.0.1:5000

________________________________

## Database Schema

Users Table
id (INT, PRIMARY KEY, AUTO_INCREMENT)
name (VARCHAR) - User's full name
email (VARCHAR, UNIQUE) - User's email address
password (VARCHAR, hashed) - User's password (bcrypt hash)
role (VARCHAR: 'visitor', 'registered') - User role (default: 'registered')
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Registration date

Categories Table
id (INT, PRIMARY KEY, AUTO_INCREMENT)
name (VARCHAR) - Category name (Playas, Parques, Aventura, Termales)

Destinations Table
id (INT, PRIMARY KEY, AUTO_INCREMENT)
name (VARCHAR) - Destination title/name
description (TEXT) - Full description of the destination
location (VARCHAR) - Province where located
category_id (INT, FOREIGN KEY REFERENCES categories(id)) - Category ID
daily_cost (DECIMAL) - Cost per person per day
main_photo (VARCHAR) - Main image path
photo2 (VARCHAR) - Second image path
photo3 (VARCHAR) - Third image path
restaurantes_links (TEXT) - Comma-separated links to restaurants
actividades_links (TEXT) - Comma-separated links to activities
hospedajes_links (TEXT) - Comma-separated links to accommodations
rentacar_links (TEXT) - Comma-separated links to car rentals
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Creation date

### Comments Table
id (INT, PRIMARY KEY, AUTO_INCREMENT)
user_id (INT, FOREIGN KEY REFERENCES users(id)) - User who commented
destination_id (INT, FOREIGN KEY REFERENCES destinations(id)) - Destination being commented
text (TEXT) - Comment content
rating (INT, CHECK 1-5) - Rating from 1 to 5 stars
created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP) - Comment date
________________________________

AI Integration (DeepSeek)
The AI assistant uses DeepSeek API. To enable it:

Get an API key from DeepSeek Platform

Install the DeepSeek package:

pip install deepseek
Add your API key to the configuration

________________________________

Documentation
(Project Overview.pdf)

 Contributors
Joshua Membreño

Valeria Mejias

Julian Murillo

Contact
For questions or suggestions: josejulianmurillomondragon.17@gmail.com

Project Link: https://github.com/JoshVM04/ProyectoFinal
