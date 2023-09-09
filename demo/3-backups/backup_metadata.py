import subprocess
import json
import platform

import os
import zipfile
from datetime import datetime


# ********** Note: **********
# The provided code is free to use for educational and non-commercial purposes.
# It is offered without any warranty, express or implied. The author and contributors
# of this code cannot be held liable for any damages or consequences resulting from the use of this code.
# Use at your own risk.

# ********** Use Case: **********
# This sample script demonstrates how to backup metadata from an org using the Salesforce CLI.


api_version = "57.0"
env_prod = "CGI-CLI-DEMO-PROD"
env_dev1 = "CGI-DEMO-DEV1"


def main():
    # generate a manifest by pulling all the metadata in source-tracking: scratch org, developer or developer-pro only
    metadata_retrieve_preview()

    # retrieve metadta from target-org
    metadata_retrieve_all()

    # backup metadta from target-org
    backup_metadata()


# generate a manifest by pulling all the metadata in source-tracking: scratch org, developer or developer-pro only
def metadata_retrieve_preview():

    # sf project retrieve start --target-org env_dev1 --api-version api_version --json
    command = ["sf", "project", "retrieve", "preview", "--target-org", env_dev1, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    print("***** result_status *****")
    print(sf_result_json)

    if result_status == 0:
        print("Success: retrieved metadta from target-org")

        output_file = "scripts/demo/3-backups/json-responses/sf_project_retrieve_preview.json"
        write_response_to_file(sf_result_json, output_file)


# generate a manifest by pulling all the metadata in source-tracking: scratch org, developer or developer-pro only
def metadata_retrieve_all():

    # sf project retrieve start --target-org env_prod --manifest manifest/asterisk-package.xml --output-dir md --api-version api_version --json
    command = ["sf", "project", "retrieve", "start", "--target-org", env_prod, "--manifest",
               "manifest/asterisk-package.xml", "--output-dir", "md/backup", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: retrieved metadta from target-org")

# zip the metadata files and save them in the backups folder
def backup_metadata():

    # Directory to be zipped
    source_directory = "md/backup"  # Update this with the correct path

    # Get current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Zip file name
    zip_filename = f"cgi_prod_backup_{timestamp}.zip"

    # Directory to save backups
    backup_directory = "backups"
    os.makedirs(backup_directory, exist_ok=True)

    # Path to save the zip file
    output_zip_path = os.path.join(backup_directory, zip_filename)

    # Create a ZipFile object
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source directory and add files to the zip
        for foldername, subfolders, filenames in os.walk(source_directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, source_directory)
                zipf.write(file_path, arcname)

    print(f"Zip file '{zip_filename}' created and saved in '{backup_directory}' folder.")



# ********** Support Methods **********


def get_command(list_of_arguments=[]):
    os_system = platform.system()
    # On Windows, we need to run the command in a shell
    return ['cmd', '/c'] + list_of_arguments if os_system == 'Windows' else list_of_arguments


def execute_step(command):
    sf_process_results = ''
    try:
        sf_process_results = subprocess.run(
            command, capture_output=True, text=True)
        sf_process_results = sf_process_results.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e}")

    return sf_process_results


def get_result_status(sf_result_json):
    return sf_result_json.get('status', {})


def write_response_to_file(sf_result_json, output_file):
    with open(output_file, "w") as file:
        json.dump(sf_result_json, file)


if __name__ == "__main__":
    main()
