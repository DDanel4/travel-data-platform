SELECT
    DATE(date) AS date,
    ROUND(AVG(temperature)::numeric, 2) AS average_temperature,
    ROUND(MIN(temperature)::numeric, 2) AS min_temperature,
    ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
    ROUND(SUM(precipitation)::numeric, 2) AS total_precipitation,
    ROUND(AVG(humidity)::numeric, 2) AS average_humidity
FROM {{ ref('stg_weather') }}
GROUP BY DATE(date)
ORDER BY date