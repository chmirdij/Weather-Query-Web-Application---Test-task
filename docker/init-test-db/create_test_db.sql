SELECT 'CREATE DATABASE test_weather_app_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_weather_app_db')\gexec