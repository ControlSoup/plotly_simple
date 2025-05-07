import os
import numpy as np
import pandas as pd

def remove_file(file_path: str):
    try:
        os.remove(file_path)
    except:
        pass


def datadict_to_csv(datadict: dict[str, np.array], file_path: str, compression: str = None):
    df = pd.DataFrame.from_dict(datadict)
    df.to_csv(file_path, index=False, compression = compression)


def csv_to_datadict(file_path: str, compression: str = None, subsample: int = 1) -> dict[str, np.array]:
    df = pd.read_csv(file_path, compression = compression)

    dict = {}
    for key in df:
        dict[key] = df[key].to_numpy()[::subsample]

    return dict


def to_file(string: str, file_path: str, prepend: str = None, append: str = None):
    with open(file_path, "w", encoding="utf-8") as f:

        if prepend is not None:
            f.write(prepend)

        f.write(string)

        if append is not None:
            f.write(append)


class ReportHTML():
    def __init__(self, title: str):
        self.text = ""
        self.__header(title)

    def __header(self, title):
        self.write('<head>')
        self.write('    <meta charset="UTF-8">')
        self.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        self.write(f'   <title>{title}</title>')
        self.write('    <style>')
        self.write('        body {')
        self.write('            font-family: Arial, sans-serif;')
        self.write('            margin: 20px;')
        self.write('        }')
        self.write('        details summary {')
        self.write('            cursor: pointer;')
        self.write('            font-weight: bold;')
        self.write('        }')
        self.write('        details[open] summary {')
        self.write('            color: blue;')
        self.write('        }')
        self.write('    </style>')
        self.write('</head>')

    def write(self, text: str):
        self.text += f"{text}\n"

    def write_collapsable(self, text: str, section_title: str):
        self.write('<body>')
        self.write(f'    <h1>{section_title}</h1>')
        self.write('    <details>')
        self.write(text)
        self.write('    </details>')
        self.write('</body>')

    def export(self, file_path: str):
        to_file(self.text, file_path)
