import os
import polars as pl
import yaml
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

    # Compile data
    df_list = []
    for source, info in template['data']:

        if "type" not in info:
            warning(f"Data source [{source}] does not contain type information skipping")
            continue
        
        if info["type"] == 'path':
            df_list.append((source, parse_path(source)))

    
