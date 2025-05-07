from plotly_datadict import tar_database

tarpath = "examples/example.tar.gz"
try:
    tar_database.create_tar_gzip(tarpath)
except:
    pass

tar_database.add_entries(tarpath, "examples/set-1.csv", "examples/set-2.csv")
print(tar_database.list_entries(tarpath))
tar_database.delete_entry(tarpath, "examples/set-1.csv")
print(tar_database.list_entries(tarpath))
tar_database.add_entries(tarpath, "examples/set-1.csv", "examples/set-2.csv")

df = tar_database.get_entry(tarpath, 'set-2')