from helpers.data import load_data, convert_df_to_json

import pandas as pd
import numpy as np


def test_load_data():
    test_df = pd.DataFrame(
        {"id": ["1", "2", "3"], "test4": ["test", "N/A", "test"]}
    )
    test_df = test_df.replace("N/A", np.nan)
    test_df.set_index("id", inplace=True)
    pd.testing.assert_frame_equal(
        load_data(filepath="tests/data/test-data.csv", skip_blank_rows=False),
        test_df,
    )


def test_subtables():
    test_df = pd.DataFrame(
        {
            "id": ["1", "2"],
            "collectionobjectattribute": [
                {"text1": "test", "text2": "test"},
                {"text1": "test", "text2": "test"},
            ],
        }
    )
    test_df.set_index("id", inplace=True)
    pd.testing.assert_frame_equal(
        load_data(
            filepath="tests/data/test-data-subtable.csv",
            skip_blank_rows=False,
            subtables=["collectionobjectattribute"],
        ),
        test_df,
    )


def test_skip_rows():
    test_df = pd.DataFrame({"id": ["1", "3"], "test4": ["test", "test"]})
    test_df.set_index("id", inplace=True)
    pd.testing.assert_frame_equal(
        load_data(filepath="tests/data/test-data.csv", skip_blank_rows=True),
        test_df,
    )


def test_df_to_json():
    test_json = {
        "1": {"test4": "test"},
        "2": {"test4": None},
        "3": {"test4": "test"},
    }
    assert (
        convert_df_to_json(
            load_data(
                filepath="tests/data/test-data.csv", skip_blank_rows=False
            )
        )
        == test_json
    )
