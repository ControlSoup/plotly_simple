import os
import polars as pl
import yaml
import plotly.graph_objects as go
from logging import warning
from . import tar_database
from . import plot_wrappers as pwrap

def parse_yaml(file_path) -> dict:
        with open(file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")


def parse_path(path: str) -> pl.DataFrame:

    if 'tar.gz' in path:
        source, entry = path.split(":")
        return tar_database.get_entry(source, entry)
    elif '.csv' in path:
        return pl.read_csv(path)
    else:
        warning(f"Unable to parse path type {path}")

        
def parse_template(template: dict) -> list[go.Figure]:

    for key in ["data", "plots"]:
        if key not in template:
            raise ValueError(f"Template must contain the key [{key}]")

    if 'plots' not in template:
        raise ValueError("Template must contain the key [data]")

    # Compile data
    df_list = []
    for source, info in template['data'].items():

        if "type" not in info:
            warning(f"Data source [{source}] does not contain type information skipping")
            continue
        
        if info["type"] == 'path':
            df = parse_path(source)
        
        df_list.append(dict(
            df = df,
            source = source,
            alt_color = info.get('alt_color')
        ))

    # Get the plot configs going
    fig_list = [] 
    plot: dict
    for plot_name, plot in template['plots'].items():

        fig = go.Figure()

        for key in ["type", "x"]:
            if key not in plot:
                raise ValueError(f"Plot [{plot_name}] must contain key [{key}]")

        type = plot["type"]
        x = plot['x']

        _color_list = [
            '#2ca02c',  # cooked asparagus green
            '#1f77b4',  # muted blue
            '#d62728',  # brick red
            '#ff7f0e',  # safety orange
            '#9467bd',  # muted purple
            '#bcbd22',  # curry yellow-green
            '#8c564b',  # chestnut brown
            '#e377c2',  # raspberry yogurt pink
            '#7f7f7f',  # middle gray
            '#17becf'   # blue-teal
        ]
        color_list = lambda idx: _color_list[idx % len(_color_list)]
        curr_color = 0

        for i, axis in enumerate([_str for _str in plot if _str == ('y1' or 'y2' or 'y3' or 'y4')]):
            for y_ch in plot[axis]:
                
                # This makes me not like myself right here, disgusting... 
                # #who puts a typ eclause with locally scoped var
                if isinstance(y_ch, dict):
                    y_ch_content = y_ch[next(iter(y_ch))]
                    y_ch = next(iter(y_ch))

                for info in df_list:

                    df = info['df']
                    source = info['source'] 

                    if info['alt_color'] is not None:
                        color = y_ch_content.get(f'alt_color_{info["alt_color"]}', color_list(curr_color))
                    else:
                        color = plot.get('color', color_list(curr_color))

                    if y_ch not in df:
                        warning(f'Unable to find [{y_ch}] in [{source}], skipping in the plot')
                        continue

                    if type.lower() == 'lines' or 'markers':
                        pwrap.graph_scatter_by_key(
                            df = df,
                            x = x,
                            y = y_ch,
                            x_title = plot.get('x_title'),
                            y_title = plot.get('y_title'),
                            title = plot_name,
                            color = color,
                            group_name = y_ch,
                            fig = fig,
                            mode = type,
                            alt_y_name = f'{source}:{y_ch}',
                            options = plot.get('options', {}),
                            axis = i + 1,
                        )
                curr_color += 1
        fig_list.append(fig)

    return fig_list

        





