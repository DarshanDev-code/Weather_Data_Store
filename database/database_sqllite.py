import sqlite3

cities = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", 
    "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", 
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", 
    "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", 
    "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", 
    "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", 
    "Vasai-Virar", "Varanasi", "Srinagar", "Aurangabad", 
    "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", 
    "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", 
    "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", 
    "Guwahati", "Chandigarh", "Solapur", "Hubli–Dharwad", 
    "Bareilly", "Mysore", "Tiruchirappalli", "Tiruppur", 
    "Moradabad", "Salem", "Aligarh", "Thiruvananthapuram", 
    "Bhiwandi", "Saharanpur", "Gorakhpur", "Guntur", 
    "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", 
    "Warangal", "Cuttack", "Firozabad", "Kochi", "Bhavnagar"
]

conn = sqlite3.connect(database="C:/Users/DARSHAN/Desktop/Python/Whether_data_store/weather_data.db")
cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS cities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE)
    '''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS forecasts(
        forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities(id))
    '''
)
cur.execute(
    '''CREATE TABLE IF NOT EXISTS forecast_history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities(id))
    '''
)

def add_cities():
    cur.execute('''SELECT name FROM cities''')
    if not cur.fetchall():
        for city in cities:
            cur.execute('''INSERT INTO cities (name) VALUES(?)''',(city,))
    conn.commit()

def add_city(city):
    try:
        cur.execute('''INSERT INTO cities (name) VALUES(?)''',(city,))
    except:
        print('City already exists')

def show_cities_table():
    cur.execute('SELECT * FROM cities')
    rows = cur.fetchall()
    for row in rows:
        print(row)

def city_exists(city):
    query = "SELECT name FROM cities WHERE name = ?;"
    try:
        cur.execute(query, (city,))
        res = cur.fetchone()
        return res[0]
    except:
        return False