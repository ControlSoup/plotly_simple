import plotly_datadict.template_parsing as tp
import plotly_datadict.tar_database as tb
import os

FILE_PATH = os.path.dirname(__file__) 
config =  tp.parse_yaml('examples/example.yaml')

figs = tp.parse_template(config)

for fig in figs:
    fig.show()