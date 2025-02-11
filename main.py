from helpers.data import load_data, convert_df_to_json
from helpers.caller import SpecifySession

from dotenv import load_dotenv
import os


def main(
    instance_url: str,
    method: str,
    table: str,
    collectionid: int,
    input_data_filepath="data/data.csv",
):
    if method not in ["edit", "delete"]:
        raise ValueError("Method argument must be edit or delete")

    # Load the environment variables from the .env file
    load_dotenv()

    # Load the data from a flat file and convert to a json format that can be ingested by the API
    json_data = convert_df_to_json(load_data(input_data_filepath))

    # Create a session to make requests to
    session = SpecifySession(
        username=os.getenv("SP7_USERNAME"),
        password=os.getenv("SP7_PASSWORD"),
        collectionid=collectionid,
        instance_url=instance_url,
    )

    # Log in
    session.login()

    if method == "edit":
        session.put_data(json_data, table=table)
    if method == "delete":
        session.delete_data(json_data, table=table)


if __name__ == "__main__":
    main()
