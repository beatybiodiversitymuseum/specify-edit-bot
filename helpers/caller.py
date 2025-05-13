"""
This module handles requests made to the instance, including logging in and
modifying data.
"""

import json
import requests

from requests.adapters import HTTPAdapter, Retry

import time
from tqdm import tqdm
import warnings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SpecifySession:
    """
    Initiates a requests session with a specify instance using the username and
    password supplied. To obtain the collectionid, run a query for collection
    name and collection id from within the Specify GUI.
    """

    S = requests.Session()

    def __init__(self, username, password, instance_url, collectionid):
        self.username = username
        self.password = password
        self.instance_url = instance_url
        self.collectionid = collectionid

    def login(self):
        """
        Log into the collection using the credentials supplied. This method must
         be run before any other requests can be made.
        """
        available_collections = self.S.get(
            self.instance_url + "/context/login/"
        )
        token = available_collections.cookies["csrftoken"]
        data = {
            "username": self.username,
            "password": self.password,
            "collection": self.collectionid,
        }
        headers = {"X-CSRFToken": token, "Referer": self.instance_url}
        log_in = self.S.put(
            url=(self.instance_url + "/context/login/"),
            data=json.dumps(data),
            headers=headers,
        )
        if log_in.status_code != 204:
            raise RuntimeError("Login failed.")
        self.collection = log_in.cookies["collection"]
        self.sessionid = log_in.cookies["sessionid"]
        self.token = log_in.cookies["csrftoken"]
        self.headers = {
            "X-CSRFToken": self.token,
            "collection": self.collection,
            "sessionid": self.sessionid,
            "Referer": self.instance_url,
        }
        self.base_url = self.instance_url + "/api/specify/"

        return None

    def put_data(
        self, data_to_add: dict, table: str, sleep_in_seconds=4.5
    ) -> None:
        """
        Takes json data with a series of id objects with corresponding
        dictionaries of data to be added to the system, and adds all data
        through put requests. The table argument must be spelled exactly as it
        is required in the request url.
        """
        # Redundancy in case the network cuts out,
        # retries after 0s, 2s, 4s, 8s, 16s
        retries = Retry(
            total=5, backoff_factor=1, status_forcelist=[502, 503, 504]
        )
        self.S.mount(self.instance_url, HTTPAdapter(max_retries=retries))
        for id, values in tqdm(data_to_add.items(), desc="Uploading records"):
            time.sleep(sleep_in_seconds)
            # Sanity check
            if not id.isnumeric():
                raise RuntimeError(
                    "The ids in the data are not properly formatted"
                )
            if not isinstance(values, dict):
                raise RuntimeError(
                    "The values in the data are not properly formatted"
                )

            # Get the version of the table via a generic get request to the
            # table
            try:
                get_table = self.S.get(
                    self.instance_url
                    + "/api/specify/"
                    + table
                    + "/"
                    + str(id)
                    + "/",
                    headers=self.headers,
                )
                get_table.raise_for_status()
                version = get_table.json()["version"]
                data = values
                params = {"version": version}
                put_request = self.S.put(
                    url=(self.base_url + table + "/" + str(id) + "/"),
                    params=params,
                    data=json.dumps(data),
                    headers=self.headers,
                )
                if put_request.status_code != 200:
                    warnings.warn(
                        f"An error occurred while editing id:{id} \
                        {put_request.text}"
                    )
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)

            logger.info(
                f"{table} with id {id} successfully edited at {datetime.now()}."
            )

        return None

    def delete_data(
        self, data_to_delete: dict, table: str, sleep_in_seconds=4.5
    ) -> None:
        """
        Takes json data with a series of id objects with corresponding
        dictionaries of data to be added to the system, and removes the records
        corresponding with those ids. The table argument must be spelled exactly
         as it is required in the request url.

        Note, the dictionary structure is still kept, which allows for both a
        similar setup to the put requests, but also allows for data to be kept
        alongside the ids for convenience, it is just not touched by the script.
        """
        retries = Retry(
            total=5, backoff_factor=1, status_forcelist=[502, 503, 504]
        )
        self.S.mount(self.instance_url, HTTPAdapter(max_retries=retries))
        for id, values in tqdm(data_to_delete.items(), desc="Deleting records"):
            time.sleep(sleep_in_seconds)
            # Sanity check
            if not id.isnumeric():
                raise RuntimeError(
                    "The ids in the data are not properly formatted"
                )

            # Get the version of the table via a generic get request to the table
            get_table = self.S.get(
                self.instance_url
                + "/api/specify/"
                + table
                + "/"
                + str(id)
                + "/",
                headers=self.headers,
            )
            version = get_table.json()["version"]
            params = {"version": version}
            delete_request = self.S.delete(
                url=(self.base_url + table + "/" + str(id) + "/"),
                params=params,
                headers=self.headers,
            )
            if delete_request.status_code != 204:
                warnings.warn(
                    "An error occurred while deleting record with id:" + id
                )
        return None
