# Harry Potter Database Management System

A web-based database management system for Harry Potter characters, creatures, and spells. Built with Python Flask and MySQL.

## Features

- View and manage Harry Potter characters
- Browse magical creatures
- Explore spells and their effects
- Beautiful Harry Potter-themed UI
- Responsive design

## Prerequisites

- Python 3.7 or higher
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Make sure MySQL server is running and accessible with the following credentials:
- Username: root
- Password: 5264077v
- Host: localhost

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Database Structure

The application uses three main tables:

1. Characters
   - id (Primary Key)
   - name
   - blood_status (pure-blood, half-blood, muggle)
   - house (gryffindor, slytherin, ravenclaw, hufflepuff, not a hogwarts student)
   - marital_status (single, married)
   - also_known_as
   - book_appearances

2. Creatures
   - id (Primary Key)
   - name
   - type
   - description
   - danger_level
   - habitat
   - diet
   - size

3. Spells
   - id (Primary Key)
   - name
   - type
   - effect
   - incantation
   - difficulty
   - creator
   - first_appearance

## Contributing

Feel free to submit issues and enhancement requests! 