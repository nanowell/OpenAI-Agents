import { useState, useEffect } from 'react';
import axios, { AxiosError } from 'axios';

interface WeatherData {
  // Add the interface for the weather data here
}

const WeatherApp = () => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [city, setCity] = useState('New York City');
  const [error, setError] = useState<AxiosError | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const response = await axios.get(
          `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=YOUR_API_KEY`
        );
        setWeatherData(response.data);
      } catch (err) {
        setError(err);
      }
    };

    fetchWeatherData();
  }, [city]);

  return (
    <div className="bg-gray-200 min-h-screen flex justify-center items-center">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-4">Weather App</h1>

        <div className="mb-4">
          <input
            type="text"
            className="border rounded-lg w-full py-2 px-3"
            placeholder="Enter a city"
            value={city}
            onChange={e => setCity(e.target.value)}
          />
        </div>

        {error ? (
          <p className="text-red-500">{error.message}</p>
        ) : weatherData ? (
          <div>
            <h2 className="text-xl font-bold mb-2">
              {weatherData.name}, {weatherData.sys.country}
            </h2>
            <p className="mb-4">
              {weatherData.weather[0].main} -{' '}
              {weatherData.weather[0].description}
            </p>
            <p className="mb-4">
              <strong>Temperature:</strong> {weatherData.main.temp} °F
            </p>
            <p className="mb-4">
              <strong>Humidity:</strong> {weatherData.main.humidity}%
            </p>
          </div>
        ) : (
          <p>Loading weather data...</p>
        )}
      </div>
    </div>
  );
};
