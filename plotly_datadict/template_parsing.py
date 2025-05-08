import os
import polars as pl
import yaml
import plotly.graph_objects as go
from logging import warning
from . import tar_database


def parse_path(path: str) -> pl.DataFrame:

    if 'tar.gz' in path:
        source, entry = path.split(":")
        return tar_database.get_entry(source, entry)
    elif '.csv' in path:
        return pl.read_csv(path)
    else:
        warning(f"Unable to parse path type {path}")


        
def parse_template(template: dict):

    for key in ["data", "plots"]:
        if key not in template:
            raise ValueError(f"Template must contain the key [{key}]")

    if 'plots' not in template:
        raise ValueError("Template must contain the key [data]")

    # Compile data
    df_list = []
    for source, info in template['data']:

        if "type" not in info:
            warning(f"Data source [{source}] does not contain type information skipping")
            continue
        
        if info["type"] == 'path':
            df_list.append((source, parse_path(source)))

    
    # Get the plot configs going
    for plot in template['plots']:

        for key in ["type", "x1", "y1"]:
            if key not in plot:
                raise ValueError(f"Plot [{plot}] must contain key {key}")

        plot_name = plot
        type = plot["type"]
        y1 = plot["y1"]
        x1 = plot["x1"]






