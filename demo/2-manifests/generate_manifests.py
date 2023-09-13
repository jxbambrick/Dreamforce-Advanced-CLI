import subprocess
import json
import platform


# ********** Note: **********
# The provided code is free to use for educational and non-commercial purposes.
# It is offered without any warranty, express or implied. The author and contributors
# of this code cannot be held liable for any damages or consequences resulting from the use of this code.
# Use at your own risk.

# ********** Use Case: **********
# This sample script demonstrates how to generate a manifest using the Salesforce CLI. 


api_version = "57.0"
env_prod = "CGI-CLI-DEMO-PROD"
env_dev1 = "CGI-DEMO-DEV1"


def main():
    # generate a manifest by pulling all the metadata in source-tracking: scratch org, developer or developer-pro only
    genreate_manifest_retrieve_start()

    # generate a manifest by pulling all the metadata using * wildcard
    generate_manifest_wildcard_package()

    # generate a manifest using the source-dir option
    generat_manifest_source_dir()

    # generate a manifest by pulling all the metadata from an org
    genreate_manifest_from_org()

    # generate a manifest by pulling all the metadata from a change set
    generate_manifest_from_change_sets()


# generate a manifest by pulling all the metadata in source-tracking: scratch org, developer or developer-pro only
def genreate_manifest_retrieve_start():

    # sf project retrieve start --target-org env_dev1 --api-version api_version --json
    command = ["sf", "project", "retrieve", "start", "--target-org",
               env_dev1, "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    print("***** result_status *****")
    print(sf_result_json)

    if result_status == 0:
        print("Success: retrieved metadta from target-org")

        # sf project generate manifest --source-dir force-app --name source-dir-package --output-dir manifest --api-version api_version --json
        command = ["sf", "project", "generate", "manifest", "--source-dir", "force-app", "--name", "sf-project-generate-package",
                   "--output-dir", "scripts/demo/2-manifests/resources", "--api-version", api_version, "--json"]

        sf_process_results = execute_step(command)
        sf_result_json = json.loads(sf_process_results)
        result_status = get_result_status(sf_result_json)

        if result_status == 0:
            print("Success: retrieved metadta from target-org")


def generate_manifest_wildcard_package():

    # sf project retrieve start --target-org env_prod --manifest manifest/asterisk-package.xml --output-dir md --api-version api_version --json
    command = ["sf", "project", "retrieve", "start", "--target-org", env_prod, "--manifest",
               "manifest/asterisk-package.xml", "--output-dir", "md", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: retrieve metadta from target-org")

        # sf project generate manifest --source-dir md --name asterisk-dir-package --output-dir manifest --api-version api_version --json
        command = ["sf", "project", "generate", "manifest", "--source-dir", "md", "--name", "sf-project-generate-asterisk-package",
                   "--output-dir", "scripts/demo/2-manifests/resources", "--api-version", api_version, "--json"]

        sf_process_results = execute_step(command)
        sf_result_json = json.loads(sf_process_results)
        result_status = get_result_status(sf_result_json)

        if result_status == 0:
            print("Success: generated asterisk-dir-package")


def generat_manifest_source_dir():

    # sf project generate manifest --source-dir force-app --api-version api_version --json
    command = ["sf", "project", "generate", "manifest", "--source-dir", "force-app", "--name", "sf-project-generate-source-dir-package",
               "--output-dir", "scripts/demo/2-manifests/resources", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: generated source-dir-package")


def genreate_manifest_from_org():

    command = ["sf", "project", "generate", "manifest", "--from-org", env_prod, "--name",
               "from-org-package", "--output-dir", "scripts/demo/2-manifests", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: generated manifest using from-org")


def generate_manifest_from_change_sets():

    # sf project retrieve start --target-org env_prod --package-name WidgetUpdatesv1 
    # --target-metadata-dir md/WidgetUpdatesv1 --unzip --api-version api_version --json
    change_set_name = "WidgetUpdatesv1"

    # *special behavior when using --unzip
    # special behavior when using --api-version
    command = ["sf", "project", "retrieve", "start", "--target-org", env_prod, "--package-name", change_set_name,
               "--target-metadata-dir", f"md/{change_set_name}", "--unzip", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: retrieve change set from target-org")


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
