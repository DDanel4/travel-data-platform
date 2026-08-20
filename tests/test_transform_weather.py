"""
import pandas as pd
from unittest.mock import MagicMock
from scripts.etl.weather_etl import transform_weather_data



def test_transform_weather_data_returns_correct_dataframe() -> None:    
    mock_response = MagicMock()
    mock_response.Latitude.return_value = 3.5833
    mock_response.Longitude.return_value = 98.6667
    mock_response.Timezone.return_value = b"Asia/Jakarta"
    
    mock_hourly = MagicMock()
    mock_hourly.Time.return_value = 1700000000     # Start Unix timestamp
    mock_hourly.TimeEnd.return_value = 1700007200  # Eind Unix timestamp (2 uur later)
    mock_hourly.Interval.return_value = 3600       # Interval van 1 uur (3600 seconden)
    
    mock_var_temperature = MagicMock()
    mock_var_temperature.ValuesAsNumpy.return_value = [25.5, 26.0]
    
    mock_var_precipitation = MagicMock()
    mock_var_precipitation.ValuesAsNumpy.return_value = [0.0, 0.1]
    
    mock_var_humidity = MagicMock()
    mock_var_humidity.ValuesAsNumpy.return_value = [80.0, 82.0]
    
    mock_hourly.Variables.side_effect = [
        mock_var_temperature,
        mock_var_precipitation,
        mock_var_humidity
    ]
    
    mock_response.Hourly.return_value = mock_hourly

    result_df = transform_weather_data(mock_response)

    assert result_df is not None
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 2
    assert "latitude" in result_df.columns
    assert "temperature" in result_df.columns
    assert result_df["latitude"].iloc[0] == 3.5833
    assert result_df["temperature"].iloc[0] == 25.5
"""