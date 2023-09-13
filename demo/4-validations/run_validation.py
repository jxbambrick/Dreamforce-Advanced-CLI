import subprocess
import json
import platform

import os
import glob


# ********** Note: **********
# The provided code is free to use for educational and non-commercial purposes.
# It is offered without any warranty, express or implied. The author and contributors
# of this code cannot be held liable for any damages or consequences resulting from the use of this code.
# Use at your own risk.

# ********** Use Case: **********
# This sample script demonstrates how to validate metadata using the Salesforce CLI. 


api_version = "57.0"
env_prod = "CGI-CLI-DEMO-PROD"
env_dev1 = "CGI-DEMO-DEV1"


def main():
    
    # preview the deployment
    project_deploy_preview()

    # validate the deployment #1
    project_deploy_start_validation()

    # validate the deployment
    project_deploy_validate()

    # TODO: need to complete testing method
    # validate just apex 
    apex_run_tests()


# preview the deployment
def project_deploy_preview():

    # sf project retrieve start --target-org env_dev1 --api-version api_version --json
    command = ["sf", "project", "deploy", "preview", "--target-org", env_dev1, "--manifest", "scripts/demo/4-validations/preview-package.xml", "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: project preview")


# 
def project_deploy_start_validation():

    # sf project deploy start --target-org env_dev1 --test-level NoTestRun --api-version api_version --json
    command = ["sf", "project", "deploy", "start", "--target-org", env_dev1, "--manifest", "scripts/demo/4-validations/resources/preview-package.xml", "--test-level", "NoTestRun", "--api-version", api_version, "--dry-run", "--json"]
    # NoTestRun is an ooption only on the project deploy start

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    if result_status == 0:
        print("Success: project deploy start --dry-run")



def project_deploy_validate():
    
    # preferred method to validate
    # tests need to be individual
    # sf project deploy validate --target-org env_dev1 --manifest scripts/demo/4-validations/resources/preview-package.xml --api-version api_version --json
    command = ["sf", "project", "deploy", "validate", "--target-org", env_dev1, "--manifest", "scripts/demo/4-validations/resources/preview-package.xml", "--api-version", api_version, "--json"]

    apex_test_flags = get_apex_test_flags()
    command.extend(apex_test_flags)

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    print("***** result_status *****")
    print(sf_result_json)

    if result_status == 0:
        print("Success: project deploy validate")

        output_file = "scripts/demo/4-validations/json-responses/project_deploy_validate.json"
        write_response_to_file(sf_result_json, output_file)



def apex_run_tests():

    # sf project retrieve start --target-org env_dev1 --api-version api_version --json
    command = ["sf", "apex", "tests", "run", "--target-org", env_dev1, "--test-level", "RunSpecifiedTests", "--tests", "sample-test-1", "--detailed-coverage", "--api-version", api_version, "--json"]

    sf_process_results = execute_step(command)
    sf_result_json = json.loads(sf_process_results)
    result_status = get_result_status(sf_result_json)

    print("***** result_status *****")
    print(sf_result_json)

    if result_status == 0:
        print("Success: apex tests run")

        output_file = "scripts/demo/4-validations/json-responses/apex_tests_run.json"
        write_response_to_file(sf_result_json, output_file)


def get_apex_test_flags():
    # this is the default in case there are no Apex test classes in your local project
    apex_test_flags = ["--test-level", "RunSpecifiedTests"]
    apex_test_classes = get_apex_test_classes()

    if apex_test_classes:
        for test_class in apex_test_classes.split(","): 
            apex_test_flags.extend(["--tests", test_class])
    else:
        apex_test_flags.extend(["--tests", ""])

    return apex_test_flags


def get_apex_test_classes():
    path = os.path.join("force-app", "main", "default", "classes")
    return ",".join([os.path.basename(x).replace(".cls", "") for x in glob.glob(path + "/*Test.cls")])


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