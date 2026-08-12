SELECT 
        id,
        date,
        latitude,
        longitude,
        temperature,
        precipitation,
        humidity
FROM {{ source('raw', 'weather') }}
