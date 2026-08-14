import os
import dagster as dg
from dagster_project.assets import weather_data, load_weather
from dagster_project.dbt_assets import dbt_models, dbt_path
from dagster_dbt import DbtCliResource, dbt_assets



dbt_resource = DbtCliResource(
    project_dir=os.fspath(dbt_path),
    profiles_dir=os.fspath("C:/Users/danel/.dbt"),
)

defs = dg.Definitions(  
                        assets = [weather_data, 
                                load_weather,
                                dbt_models],
                        resources={"dbt" : dbt_resource,
                                   },    
                    )