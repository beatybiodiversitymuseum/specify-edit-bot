# Specify Edit Bot

This tool allows for bulk editing of a given table in Specify 7 via id numbers.

## Setup

Before using the script, a dedicated specify user should be created in the instance and given a descriptive name that identifies it as a bot (such as `bulk_edit_bot`). It should be given the *lowest permissions* required to perform its task. Usually this is `update` or `delete` permissions in the target table, and `read` access to any tables which are required for that table to load.

### Dependencies

All required dependencies are listed in `requirements.txt`. They can be installed via `pip install -r requirements.txt`. A virtual environment is recommended.

### Secrets

The bot requires login credentials, however, these should be kept safe and not committed to git. They are thus defined in an `.env` in the root of the repository. The `.env` file should look like this, in which `{bot_username}` and `{bot_password}` are replaced with the values of the bot account

```toml
SP7_USERNAME = {bot_username}
SP7_PASSWORD = {bot_password}
```

### Input data

Input data should be defined as a csv file. The left-most column should contain id numbers, and be called `id`. The other columns should represent the fields you wish to edit, and be named to match the database schema. For example, editing some records in `collectionobject` may look like this

| id | remarks | text1 | cataloger |
| --- | ------ | ----- | -------- |
| 4523 | Edits made by a bot | test 1 2 | /api/specify/agent/3

Note that relationships to other tables just need to be defined by their appropriate API route. Edits to fields within the same table just need to adhere to business rule and type requirements for that field.

Depending on if your data file is csv or tab delimited, you may need to change the `sep=` argument within `pd.read_csv` in `helpers/data.py`. Tab delimited files should use `sep='\t'` while csv delimited files should not need the `sep=` argument at all.

## Usage

All non-secret variables that need to be adjusted to define the task are in `main()`. They are outlined here:

- `instance_url`: The base url for your instance. For example, `https://sp7demofish.specifycloud.org`. It should not have a trailing slash.
- `method`: Either `edit` or `delete`. If the method is `edit`, then the program will edit existing values based on what is defined in the input table. If the method is `delete`, then a list of ids is all that is required (if data is present it will be ignored), and the program will attempt to delete records with that id from the specified table. Note that Specify has delete blockers which may prevent a record from being deleted if it has dependents. The program will stop with an error if an API call results in a non-successful status code.
- `table`: The table to perform the edits on. Must match the table name as defined in the API documentation. For example, `collectionobject`
- `collectionid`: The collection id that defines the collection to edit. Required for logging in.
- `input_data_filepath`: The filepath which the program should look to for the input data. Default is `data/data.csv`. If you do not use this path, you should add the path to `.gitignore` if it is within the repository.

Once the variables above have been defined, you may run `main.py`. A progress bar will display in the terminal to show the estimated time to complete the edits. To avoid excess strain on the specify instance, the program is set to wait 4.5 seconds between api calls.