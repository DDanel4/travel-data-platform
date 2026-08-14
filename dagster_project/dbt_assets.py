from pathlib import Path
from dagster_dbt import dbt_assets, DbtCliResource
from dagster import AssetExecutionContext
from dagster_dbt import DagsterDbtTranslator
from dagster_project.assets import load_weather



class CustomDbtTranslator(DagsterDbtTranslator):

    def get_asset_spec(self, manifest, unique_id, project):
        spec = super().get_asset_spec(
            manifest,
            unique_id,
            project,
        )

        node = manifest.get("nodes", {}).get(unique_id)

        if (
            node is not None
            and node["resource_type"] == "model"
            and node["name"] == "stg_weather"
        ):
            return spec.replace_attributes(
                deps=[load_weather]
            )

        return spec

dbt_path = Path("C:/Users/danel/travel-data-platform/dbt")

@dbt_assets(manifest=dbt_path.joinpath("target", "manifest.json"),
            dagster_dbt_translator=CustomDbtTranslator(),
            )

def dbt_models(context : AssetExecutionContext,
                         dbt : DbtCliResource,
                         ):
    yield from dbt.cli(["build"], context=context).stream()