[README.md](https://github.com/user-attachments/files/25462053/README.md)
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
- Delete inappropriate comments
- View all registered users

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

Database Schema
Users Table
id (INT, PRIMARY KEY)

name (VARCHAR)

email (VARCHAR, UNIQUE)

password (VARCHAR, hashed)

role (VARCHAR: 'visitor', 'registered')

created_at (TIMESTAMP)

Destinations Table
id (INT, PRIMARY KEY)

name (VARCHAR)

description (TEXT)

location (VARCHAR)

category (ENUM: 'beaches', 'parks', 'adventure', 'hot_springs')

daily_cost (DECIMAL)

main_photo (VARCHAR)

photo2 (VARCHAR)

photo3 (VARCHAR)

created_at (TIMESTAMP)

Comments Table
id (INT, PRIMARY KEY)

user_id (INT, FOREIGN KEY)

destination_id (INT, FOREIGN KEY)

text (TEXT)

rating (INT, 1-5)

created_at (TIMESTAMP)

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


