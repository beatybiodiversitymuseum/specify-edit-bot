"""
This module converts the data contained in a flat file (csv) to a json
representation of the same data, so that it may be ingested by the Specify API
"""

import pandas as pd
from json import loads, dumps
import json


def load_data(
    filepath: str, skip_blank_rows=True, subtables=[]
) -> pd.DataFrame:
    """Convert data (csv) from a filepath and output a dataframe"""
    df = pd.read_csv(filepath, header=0, dtype="str")
    df.set_index("id", inplace=True)
    if skip_blank_rows:
        df = df.dropna(how="all")
    for subtable in subtables:
        df[subtable] = df[~df[subtable].isna()][subtable].apply(
            lambda st_dict: json.loads(st_dict.replace("'", '"'))
        )
    return df


def convert_df_to_json(df: pd.DataFrame) -> dict:
    """
    Converts a pandas dataframe with a catalog number to a dictionary that
    contains the catalog number as the key and a json representation of the data
     contained within all other columns.
    """
    result = df.to_json(orient="index")
    parsed = loads(result)
    json_object = json.loads(dumps(parsed, indent=4))
    return json_object


def confirmation(json_object: dict, method: str, table: str) -> bool:
    """
    Formats information about the data and its destination and presents to
    the user for confirmation
    """
    print(
        f"You are about to {method} {len(json_object)} records in the {table} table."
    )
    confirm = input("Do you wish to proceed? (y/n)")
    if confirm == "y":
        return True
    return False
