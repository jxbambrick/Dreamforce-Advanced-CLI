import subprocess
import json
import platform

from scripts.sf_validate_package_xml import validate_package_xml
from scripts.sf_get_apex_test_classes import get_apex_test_classes_formatted


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
    # get_apex_test_classes()

    # validate_test_packages()

    # remove_nodes_from_metadata()
    pass


def get_apex_test_classes():

    apex_test_class_flags = get_apex_test_classes_formatted()
    print(f"Formatted Apex Flag: {apex_test_class_flags}")


def validate_test_packages():

    malformed_package_xml = 'demo/5-bonus/resources/bad_package_v1.xml'
    is_valid, message = validate_package_xml(malformed_package_xml)
    print(f"Is Valid: {is_valid} - Message: {message}")

    missing_required_xml = 'demo/5-bonus/resources/bad_package_v2.xml'
    is_valid, message = validate_package_xml(missing_required_xml)
    print(f"Is Valid: {is_valid} - Message: {message}")

    contains_extra_name_element_xml = 'demo/5-bonus/resources/bad_package_v3.xml'
    is_valid, message = validate_package_xml(contains_extra_name_element_xml)
    print(f"Is Valid: {is_valid} - Message: {message}")

    valid_package_xml = 'demo/5-bonus/resources/valid_package.xml'
    is_valid, message = validate_package_xml(valid_package_xml)
    print(f"Is Valid: {is_valid}  - Message: {message}")


def remove_nodes_from_metadata():
    
    # node scripts/support/sf_remove_nodes.js -f "**/*.profile-meta.xml" -p Profile.fieldPermissions.field -v "CustomWidget__c.Custom_Widget_Name__c"
    subprocess.run(["node", "scripts/custom/sf_remove_nodes.js", "-f", "**/*.profile-meta.xml",
                   "-p", "Profile.fieldPermissions.field", "-v", "CustomWidget__c.Custom_Widget_Description__c"])
    
    # <fieldPermissions>
    #     <editable>true</editable>
    #     <field>CustomWidget__c.Custom_Widget_Description__c</field>
    #     <readable>true</readable>
    # </fieldPermissions>

    print("***** remove_nodes_metadata *****")


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
