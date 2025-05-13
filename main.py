from helpers.data import load_data, convert_df_to_json, confirmation
from helpers.caller import SpecifySession
import logging

from dotenv import load_dotenv
import os
import sys
from datetime import datetime


logger = logging.getLogger(__name__)


def main(
    instance_url: str,
    method: str,
    table: str,
    collectionid: int,
    subtables=[],
    skip_blank_rows=False,
    input_data_filepath="data/data.csv",
):
    logging.basicConfig(
        filename=f"logging/{datetime.today().strftime('%Y-%m-%d')}.log",
        level=logging.INFO,
    )
    logger.info(f"\nStarted logging {datetime.now()}")

    if method not in ["edit", "delete"]:
        raise ValueError("Method argument must be edit or delete")

    # Load the environment variables from the .env file
    load_dotenv()

    # Load the data from a flat file and convert to a json format that can be
    # ingested by the API
    json_data = convert_df_to_json(
        load_data(
            filepath=input_data_filepath,
            skip_blank_rows=skip_blank_rows,
            subtables=subtables,
        )
    )

    # Create a session to make requests to
    session = SpecifySession(
        username=os.getenv("SP7_USERNAME"),
        password=os.getenv("SP7_PASSWORD"),
        collectionid=collectionid,
        instance_url=instance_url,
    )

    # Log in
    session.login()

    ack = confirmation(method=method, json_object=json_data, table=table)
    if not ack:
        sys.exit(
            "Configuration not accepted. Program will exit without making changes"
        )

    if method == "edit" and ack:
        session.put_data(data_to_add=json_data, table=table)
    if method == "delete" and ack:
        session.delete_data(data_to_delete=json_data, table=table)

    logger.info(f"Logging finished at {datetime.now()}")


if __name__ == "__main__":
    main()
