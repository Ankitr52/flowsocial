from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize Database (Add your event and user initialization logic here)
def init_db(db_path):
    if not os.path.exists('database'):
        os.makedirs('database')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop the tables if they exist
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS events')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            city TEXT,
            interest TEXT,
            events_registered TEXT
        )
    ''')

    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            event_date TEXT
        )
    ''')

    conn.commit()

    # Insert sample users
    sample_users = [
        ('Rahul', 'rahul@example.com', 'password123', 'Noida, Uttar Pradesh', 'gaming, reading', ''),
        ('Ankit', 'ankit@example.com', 'password123', 'Delhi, Delhi', 'coding, gaming', ''),
        ('Priya', 'priya@example.com', 'password123', 'Mumbai, Maharashtra', 'reading, photography', ''),
        ('Karan', 'karan@example.com', 'password123', 'Bangalore, Karnataka', 'sports, cooking', ''),
        ('Amit', 'amit@example.com', 'password123', 'Chennai, Tamil Nadu', 'music, traveling', ''),
        ('Sia', 'sia@example.com', 'password123', 'Hyderabad, Telangana', 'coding, traveling', ''),
        ('Ravi', 'ravi@example.com', 'password123', 'Pune, Maharashtra', 'gaming, coding', ''),
        ('Neha', 'neha@example.com', 'password123', 'Lucknow, Uttar Pradesh', 'cooking, gardening', ''),
        ('Rishabh', 'rishabh@example.com', 'password123', 'Jaipur, Rajasthan', 'sports, photography', ''),
        ('Sakshi', 'sakshi@example.com', 'password123', 'Kolkata, West Bengal', 'music, painting', ''),
        ('Vishal', 'vishal@example.com', 'password123', 'Ahmedabad, Gujarat', 'gaming, reading', ''),
        ('Madhuri', 'madhuri@example.com', 'password123', 'Chandigarh, Punjab', 'traveling, photography', ''),
        ('Manish', 'manish@example.com', 'password123', 'Surat, Gujarat', 'cooking, sports', ''),
        ('Deepika', 'deepika@example.com', 'password123', 'Indore, Madhya Pradesh', 'music, dancing', ''),
        ('Yash', 'yash@example.com', 'password123', 'Bhopal, Madhya Pradesh', 'photography, traveling', ''),
        ('Simran', 'simran@example.com', 'password123', 'Patna, Bihar', 'reading, traveling', ''),
        ('Nikhil', 'nikhil@example.com', 'password123', 'Nagpur, Maharashtra', 'gaming, coding', ''),
        ('Tanu', 'tanu@example.com', 'password123', 'Varanasi, Uttar Pradesh', 'painting, gardening', ''),
        ('Shubham', 'shubham@example.com', 'passwor123', 'Dehradun, Uttarakhand', 'sports, music', ''),
        ('Kriti', 'kriti@example.com', 'password123', 'Ranchi, Jharkhand', 'reading, traveling', '')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO users (name, email, password, city, interest, events_registered)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_users)

    # Insert sample events
    sample_events = [
        ('Tech Conference 2024', '2024-10-15'),
        ('Sports Meet 2024', '2024-11-01'),
        ('Art Exhibition', '2024-12-10'),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO events (event_name, event_date)
        VALUES (?, ?)
    ''', sample_events)

    conn.commit()
    conn.close()

# Define routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission and registration
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('database/flow_social.db')
        cursor = conn.cursor()
        
        # Add new user to the database
        cursor.execute('''
            INSERT INTO users (name, email, password, events_registered)
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, ''))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    return render_template('register.html')  # Template file for registration

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        # Handle event creation
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        
        conn = sqlite3.connect('database/flow_social.db')
        cursor = conn.cursor()
        
        # Add new event to the database
        cursor.execute('''
            INSERT INTO events (event_name, event_date)
            VALUES (?, ?)
        ''', (event_name, event_date))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    return render_template('add_event.html')  # Template file for adding events

@app.route('/')
def home():
    conn = sqlite3.connect('database/flow_social.db')
    cursor = conn.cursor()
    
    # Fetch events from the database
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()

    conn.close()
    
    return render_template('home.html', events=events)  # Template file for home page

if __name__ == '__main__':
    # Initialize database and start the server
    db_path = 'database/flow_social.db'
    init_db(db_path)
    app.run(debug=True)
