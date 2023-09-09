import xml.etree.ElementTree as ET

def validate_package_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check the root element
        namespace = '{http://soap.sforce.com/2006/04/metadata}'
        if root.tag != namespace + 'Package':
            return False, "Root element must be <Package> with correct namespace."

        # Check for required child elements
        required_elements = {namespace + 'types', namespace + 'version'}
        found_elements = {child.tag for child in root}
        if not required_elements.issubset(found_elements):
            return False, "Missing or incorrect child elements."

        # Check <types> elements
        for types_elem in root.findall(namespace + 'types'):
            name_elems = types_elem.findall(namespace + 'name')
            members_elems = types_elem.findall(namespace + 'members')
            
            if len(name_elems) != 1:
                return False, "Must have a single <name> element for each types entry."
            
            if len(members_elems) == 0:
                return False, "Each <types> element must have a single <name> element and one or more <members> elements."

        return True, "Valid package.xml"

    except ET.ParseError:
        return False, "Invalid XML format."

# Example usage (if needed to be run as a standalone script)
if __name__ == "__main__":
    package_xml_file = 'manifest/package.xml'
    is_valid, message = validate_package_xml(package_xml_file)
    print(message)
