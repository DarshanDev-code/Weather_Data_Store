from components.api_calling import get_whether_forecast
from threading import Thread
from database.database import Session,del_forecast,Forecast,CityNotExists, get_cities_table, del_city_not_exists_table

def add_all_cities(start, stop, city):
    session = Session()  # Create a session for this thread
    try:
        for i in range(start, stop):
            print(f"Processing city: {city[i].name}")
            data = get_whether_forecast(city[i].name)
            if data['success']:
                forecast = data["data"]["forecast"]["forecastday"]
                city_obj = session.merge(city[i])  # Reattach city object to session
                for day in forecast:
                    session.add(Forecast(city_id=city_obj.id, date=day["date"], weather=day['day']['condition']['text']))
                session.commit()  # Commit after processing all forecasts for a city
            else:
                session.add(CityNotExists(name=city[i].name))
                session.commit()
                print(f"{city[i].name} not found. Reason: {data['msg']}")
    except Exception as e:
        session.rollback()  # Rollback the transaction in case of error
        print(f"Error processing city {city[i].name}: {e}")
    finally:
        session.close()  # Always close the session

def main():
    cities = get_cities_table()
    city_len = len(cities)
    del_forecast()
    del_city_not_exists_table()
    t1 = Thread(target=add_all_cities, args=(0,city_len//4,cities))
    t2 = Thread(target=add_all_cities, args=(city_len//4,city_len//2,cities))
    t3 = Thread(target=add_all_cities, args=(city_len//2,(city_len//2+city_len//4),cities))
    t4 = Thread(target=add_all_cities, args=((city_len//2+city_len//4),city_len,cities))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print('Task completed')

if __name__ == "__main__":
    main()