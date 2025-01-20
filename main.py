from concurrent.futures import ThreadPoolExecutor
from database.database import Session, get_cities_table, del_forecast, del_city_not_exists_table,Forecast,CityNotExists
from components.api_calling import get_whether_forecast

def add_all_cities(start, stop, city):
    session = Session()
    try:
        for i in range(start, stop):
            print(f"Processing city: {city[i].name}")
            data = get_whether_forecast(city[i].name)
            if data['success']:
                forecast = data["data"]["forecast"]["forecastday"]
                city_obj = session.merge(city[i])
                for day in forecast:
                    session.add(Forecast(city_id=city_obj.id, date=day["date"], weather=day['day']['condition']['text']))
            else:
                session.add(CityNotExists(name=city[i].name))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def main():
    cities = get_cities_table()
    city_len = len(cities)

    # Clear existing data
    del_forecast()
    del_city_not_exists_table()

    num_threads = 4
    chunk_size = city_len // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size
            stop = (i + 1) * chunk_size if i < num_threads - 1 else city_len
            futures.append(executor.submit(add_all_cities, start, stop, cities))
        
        # Wait for all threads to complete
        for future in futures:
            future.result()

    print("Task completed")

if __name__ == "__main__":
    main()