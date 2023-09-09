import os
import glob


# return 
def get_apex_test_classes_formatted():
    
    apex_classes = get_apex_test_classes()
    formatted_apex_classes = " ".join([f"--tests {apex_class}" for apex_class in apex_classes.split(",")])
    
    return formatted_apex_classes


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


def main():
    print_test_classes_as_list = True

    if print_test_classes_as_list:
        print(get_apex_test_classes_formatted)
    else:
        print(get_apex_test_classes())
