import polars as pl
import plotly_datadict.template_parsing as tp
import plotly_datadict.tar_database as tb
import os

FILE_PATH = os.path.dirname(__file__) 
config =  tp.parse_yaml('examples/example.yaml')
file_path = lambda path: os.path.join(FILE_PATH, path)
tdb = file_path('example.tar.gz')

set4 = pl.DataFrame({'a [lbf]': [0.0, 100.0, 0.0], 'time [s]': [-10.0, 5.0, 10.0]})

# Create a db (I hate python try catches)
tb.create_tar_gzip(tdb)

try:
    tb.add_entries(tdb, file_path('set-2.csv'), file_path('set-3.csv'))

    # Create the figs
    figs = tp.parse_template(config)

    for fig in figs:
        fig.show()

except Exception as e:
    print(e)

os.remove(tdb)