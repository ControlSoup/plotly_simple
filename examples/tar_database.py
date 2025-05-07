import polars as pl
import os
import io
import tarfile 

def create_tar(tarpath: str) -> None:
    with tarfile.open(tarpath, mode = 'x:gz'):
        return


def list_entries(tarpath: str) -> list[str]:
    with tarfile.open(tarpath, mode = 'r:gz') as tar:
        return [tar.name for tar in tar.getmembers()]


def add_entries(tarpath:str, *files) -> None:
    with tarfile.open(tarpath, mode = 'w:gz') as tar:
        for file in files:
            if ".csv" in file:
                encoded = pl.read_csv(file).write_csv().encode('utf8')
                tar_info = tarfile.TarInfo(name = os.path.basename(file).replace(".csv", ""))
                tar_info.size = len(encoded)
                tar.addfile(tar_info, io.BytesIO(encoded))
            else:
                raise ValueError(f"File must be a csv, tryig to upload {file}")

def get_entry(tarpath: str, entry: str) -> pl.DataFrame:
    with tarfile.open(tarpath, mode = 'r:gz') as tar:
        file = tar.extractfile(f'{entry}.csv')
        return pl.read_csv(file)

tarpath = "examples/example.tar.gz"

# create_tar(tarpath)
add_entries(tarpath, "examples/set-1.csv", "examples/set-2.csv")
print(list_entries(tarpath))