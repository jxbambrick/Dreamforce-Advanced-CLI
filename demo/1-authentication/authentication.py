import subprocess
import json
import platform


# ********** Note: **********
# The provided code is free to use for educational and non-commercial purposes.
# It is offered without any warranty, express or implied. The author and contributors
# of this code cannot be held liable for any damages or consequences resulting from the use of this code.
# Use at your own risk.

# ********** Use Case: **********
# This sample script demonstrates an alternative method to quickly authenticate to a Salesforce org using
# the Salesforce CLI. If you are working on a proof-of-concept or demo, this method can be used to quickly
# test your code without having to create a connected app.

# Assumptions: You are previously authenticated to the Salesforce CLI

# ********** Warning: **********
# This method is not recommended for production use.


def main():

    org_alias = "CGI-CLI-DEMO-PROD"

    # run the command and get the result
    command = ["sf", "org", "display", "--verbose", "--json"]
    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        # save the json to a file
        output_file = "scripts/demo/1-authentication/sf_org_display.json"
        # write_response_to_file(sf_result_json, output_file)

        # get the command and log in to the org
        # sf org login sfdx-url --sfdx-url-file scripts/demo/1-authentication/sf_org_display.json --setdefaultusername --setalias CGI-CLI-DEMO-PROD --json
        command = ["sf", "org", "login", "sfdx-url", "--sfdx-url-file",
                   output_file, "--setdefaultusername", "--setalias", org_alias, "--json"]
        
        sf_process_results = execute_step(command)
        sf_result_json = json.loads(sf_process_results)
        result_status = get_result_status(sf_result_json)

        sf_result_json = json.loads(sf_process_results)
        result_status = get_result_status(sf_result_json)

        if result_status == 0:
            print(f"Success: authenticated to {org_alias}")
            
            # set the target org to the authenticated org
            command = ["sf", "config", "set", "target-org", org_alias, "--json"]
            sf_process_results = execute_step(command)
            sf_result_json = json.loads(sf_process_results)
            result_status = get_result_status(sf_result_json)

            if result_status == 0:
                print(f"Success: set target-org to {org_alias}")
            
        else:
            print(f"Error: failed to authenticate: {command}")

    else:
        print(f"Error: failed to run command: {command}")

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

def get_result_auth_url(sf_result_json):
    return sf_result_json.get('result', {}).get('sfdxAuthUrl', 'None')

def write_response_to_file(sf_result_json, output_file):
    with open(output_file, "w") as file:
        json.dump(sf_result_json, file)

if __name__ == "__main__":
    main()