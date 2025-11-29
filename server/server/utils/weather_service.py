import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Weather service using OpenWeatherMap API
    """
    BASE_URL = "http://api.openweathermap.org/data/2.5"
    
    @classmethod
    def get_weather_forecast(cls, latitude, longitude, date):
        """
        Get weather forecast for specific coordinates and date
        Only works for dates within 5 days from now
        """
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key:
            logger.warning("OpenWeather API key not configured")
            return None
            
        # Check if date is within 5 days
        target_date = datetime.strptime(date, '%Y-%m-%d').date() if isinstance(date, str) else date
        today = datetime.now().date()
        days_diff = (target_date - today).days
        
        if days_diff < 0 or days_diff > 5:
            return None
            
        # Check cache first
        cache_key = f"weather_{latitude}_{longitude}_{target_date}"
        cached_weather = cache.get(cache_key)
        if cached_weather:
            return cached_weather
            
        try:
            # Use 5-day forecast API
            url = f"{cls.BASE_URL}/forecast"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Find forecast for target date
            for forecast in data.get('list', []):
                forecast_date = datetime.fromtimestamp(forecast['dt']).date()
                if forecast_date == target_date:
                    weather_data = {
                        'temperature': round(forecast['main']['temp']),
                        'description': forecast['weather'][0]['description'].title(),
                        'icon': forecast['weather'][0]['icon'],
                        'humidity': forecast['main']['humidity'],
                        'wind_speed': forecast.get('wind', {}).get('speed', 0)
                    }
                    
                    # Cache for 1 hour
                    cache.set(cache_key, weather_data, 3600)
                    return weather_data
                    
            return None
            
        except requests.RequestException as e:
            logger.error(f"Weather API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Weather service error: {e}")
            return None
    
    @classmethod
    def get_weather_icon_url(cls, icon_code):
        """
        Get full URL for weather icon
        """
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
