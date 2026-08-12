SELECT
    DATE(date) AS date,
    date::TIME AS time, 
    latitude,
    longitude,
    temperature,
    precipitation,
    humidity
FROM {{ ref('stg_weather') }}