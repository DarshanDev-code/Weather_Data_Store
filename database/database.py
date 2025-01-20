from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, scoped_session

# List of Cities
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
print(f"Total Cities: {len(cities)}")


# Base Declaration
Base = declarative_base()

# City Table
class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    weather_forecast = relationship('Forecast', back_populates='city')
    forecast_history = relationship('WeatherHistory', back_populates='city')

# Forecast Table
class Forecast(Base):
    __tablename__ = 'forecasts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)
    weather = Column(String, nullable=False)
    city = relationship('City', back_populates='weather_forecast')

# Weather History Table
class WeatherHistory(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)
    weather = Column(String, nullable=False)
    city = relationship('City', back_populates='forecast_history')

#Data NotExists Table
class CityNotExists(Base):
    __tablename__ = 'city_not_exists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

# Database Configuration
DATABASE_URL = "postgresql://postgres:darshan@localhost:5432/weather_data"
engine = create_engine(DATABASE_URL, echo=True)

# Create Tables
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print("Failed to create tables:", e)

# Create Session
Session = scoped_session(sessionmaker(bind=engine))

# Populate Cities if Table is Empty
def add_city():
    session = Session()
    if not session.query(City).all():
        city_objects = [City(name=city) for city in cities]
        session.add_all(city_objects)
        session.commit()
        print("Cities added successfully!")
    session.close()

# Utility Function
def get_cities_table():
    session = Session()
    try:
        return session.query(City).order_by(City.id).all()
    finally:
        session.close()

# def city_exists(city_name):
#     session = Session()
#     return session.query(City).filter_by(name=city_name).first() is not None

def add_forecast_data(id, forecasts):
    session = Session()
    for day in forecasts:
        session.add(Forecast( city_id=id , date=day["date"], weather=day['day']['condition']['text']))
        session.commit()
    session.close()

def del_forecast():
    try:
        session = Session()
        session.execute(text("TRUNCATE TABLE forecasts RESTART IDENTITY"))
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

def del_city_not_exists_table():
    try:
        session = Session()
        session.execute(text("TRUNCATE TABLE city_not_exists RESTART IDENTITY"))
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()

def add_city_not_found(city):
    session = Session()
    session.add(CityNotExists(name = city.name))
    session.commit()
    session.close()