from helpers.data import load_data

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


def test_skip_rows():
    test_df = pd.DataFrame({"id": ["1", "3"], "test4": ["test", "test"]})
    test_df.set_index("id", inplace=True)
    pd.testing.assert_frame_equal(
        load_data(filepath="tests/data/test-data.csv", skip_blank_rows=True),
        test_df,
    )
