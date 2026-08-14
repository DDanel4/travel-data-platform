SELECT
    DATE_TRUNC('month', date)::date AS month,
    latitude,
    longitude,
    ROUND(AVG(temperature)::numeric, 2) AS average_temperature,
    ROUND(
            AVG(
                CASE 
                    WHEN date::TIME BETWEEN '06:00:00' AND '18:00:00' THEN temperature 
                END
            )::numeric, 2
        ) AS average_day_temperature,    
    ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
    ROUND(MIN(temperature)::numeric, 2) AS min_temperature,
    ROUND(SUM(precipitation)::numeric, 2) AS total_precipitation,
    ROUND(AVG(humidity)::numeric, 2) AS average_humidity
FROM {{ ref('stg_weather') }}
GROUP BY DATE_TRUNC('month', date)::date, latitude, longitude
ORDER BY month