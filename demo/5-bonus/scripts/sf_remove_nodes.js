// Author: Greg Lovelidge
// Email: greglovelidge@gmail.com
// Website: protopixel.dev/Protopixel.dev
// LinkedIn: linkedin.com/in/gregory-lovelidge-13b20731

// Description: This script removes nodes from an XML file based on a path and a value.

// Dependencies: Run the following command to installed required dependencies:
// - npm install glob xmldom yargs

// ***** Example for metadata format *****

// node scripts/node/remove-nodes.js -f "**/*.profile" -p Profile.  -v 
// <layoutAssignments>
//     <layout>Account_Geolocation__c-Account Geolocation Layout</layout>
// </layoutAssignments>

// Use "" if there is a space in the value
// node scripts/node/remove-nodes.js -f "" -p Profle.layoutAssignments.layout -v "Account_Geolocation__c-Account Geolocation Layout" 

// node scripts/node/remove-nodes.js -f "**/*.object" -p CustomObject.fields.valueSet.valueSetDefinition.value.isActive -v false
// node scripts/node/remove-nodes.js -f "**/*.profile" -p Profile.userPermissions.name -v CIIS_SupplyChainInfoChangeNotofication

// ***** Example for Source Format *****

// <PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
//    <fieldPermissions>
//        <editable>false</editable>
//        <field>Account.BIDW_Org_Rep_MailingPostalCode__c</field>
//        <readable>true</readable>
//    </fieldPermissions> */

// node scripts/support/sf_remove_nodes.js -f "**/*.profile-meta.xml" -p Profile.fieldPermissions.field -v "CustomWidget__c.Custom_Widget_Name__c"
// node scripts/support/sf_remove_nodes.js -f "**/*.profile-meta.xml" -p Profile.layoutAssignments.layout -v "Account-Account Layout"


const fs = require("fs/promises");
const { glob } = require("glob");
const xmldom = require("xmldom").DOMParser;
const serializer = new (require("xmldom").XMLSerializer)();
const argv = require("yargs/yargs")(process.argv.slice(2))
  .option("f", {
    alias: "filepath",
    describe: "Filepath blob pattern",
    type: "string",
    demandOption: true,
  })
  .option("p", {
    alias: "path",
    describe: "Path to the nodes in the XML that should be removed",
    type: "string",
    demandOption: true,
  })
  .option("v", {
    alias: "value",
    describe:
      "Value of the targeted nodes that tells the script if it should be removed",
    type: "string",
    demandOption: true,
  }).argv;

const filepathPattern = argv.f;
const targetPath = argv.p.split(".");
const targetValue = argv.v;

/** * Recursively removes the parent node of a node if it matches the provided path and value. 
 * * @param {Node} node The node to check. 
 * * @param {string[]} path The path to the node. 
 * * @param {string} value The value of the node. 
 * * @param {number} index The path index that should be checked. */ 
function removeParentOfNode(
  node,
  path,
  value,
  index = 0
) {
  const childNodes = node.childNodes;
  if (!childNodes) return;
  for (let i = childNodes.length - 1; i >= 0; i--) {
    if (index < path.length - 1 && childNodes[i].nodeName === path[index]) {
      removeParentOfNode(childNodes[i], path, value, index + 1);
    } else if (
      index === path.length - 1 &&
      childNodes[i].nodeName === path[index] &&
      childNodes[i].textContent === value
    ) {
      const parent = childNodes[i].parentNode;
      const grandparent = parent.parentNode;
      grandparent.removeChild(parent);
    }
    removeParentOfNode(childNodes[i], path, value, index);
  }
}
(async () => {
  try {
    const files = await glob(filepathPattern);
    if (files.length === 0) {
      console.log("No files found for the provided pattern:", filepathPattern);
      return;
    }
    console.log("Files found:", files);
    for (const file of files) {
      const data = await fs.readFile(file, "utf8");
      const doc = new xmldom().parseFromString(data, "application/xml");
      removeParentOfNode(doc, targetPath, targetValue);
      const updatedXML = serializer.serializeToString(doc);
      await fs.writeFile(file, updatedXML, "utf8");
    }
  } catch (err) {
    console.error("Error:", err);
  }
})();

