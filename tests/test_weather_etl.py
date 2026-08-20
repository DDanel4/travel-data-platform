import pandas as pd
import scripts.etl.weather_etl as weather_etl



class fake_variable:
    def __init__(self, values):
        self.values = values

    def ValuesAsNumpy(self):
        return self.values
    
class fake_hourly:
    def __init__(self):
        self.variables = [
            [24.64],
            [0.1],
            [96.75],
        ]
        
    def Time(self):
        return 0

    def TimeEnd(self):
        return 3600

    def Interval(self):
        return 3600

    def Variables(self, index):
        return fake_variable(self.variables[index])

class fake_response:
    def Latitude(self):
        return 3.58

    def Longitude(self):
        return 98.67

    def Timezone(self):
        return b"UTC"

    def Hourly(self):
        return fake_hourly()

def test_transform_weather_data() -> None:
    ##response = ...

    response = fake_response()
    result = weather_etl.transform_weather_data(response)
    assert isinstance(result, pd.DataFrame)
    assert "temperature" in result.columns
    assert "precipitation" in result.columns
    assert result["humidity"].iloc[0] == 96.75
    assert result["latitude"].iloc[0] == 3.58
    assert len(result) == 1
