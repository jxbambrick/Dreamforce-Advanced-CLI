# Demo notes

## Authenticate

- Easiest way is to log into an env and then use VS Code (cmd + shift + p) to auth an org
- What happens when you auth an org, where is that stored, why is this important
- Dont get caugh up on SF Login/Logout, these are for SF functions

sf org login access-token 
- requires a connectd app, digital signature

sf org login device
- createa a connect app, no  digital signature

sf org login jwt (json web token)
- requires a connected app, digital signature, recommended method*
- automated env where you can't interactively log in with a browser (CI/CD)
- create a digital signature (digital cert) using OpenSSL, store private key on your computer (set the --jwt-key-file flag to this file), create a custom connected app in your org. 

sf org login sfdx-url* 
- create a login file
- make sure to open up this file and show what it looks like
- can be used for proof-of-concept ideas, quick/insecure CI/CD pipeline


## Manifest
sf project generate 
--json
--api-version
--metadata: can pass in either the type:name or type
--source-dir: path to the local source files
--name
--type:inconsistency in the documentation, doesn't list the default value: package
--include-packages
--from-org: pass in an org and get all the metadata in existence, really powerfull
--output-dir


- this is a command that I use regullarly and is the bulk of my experience
new update can generate different kinds of manifests: package, pre, post, destroy

there is another way to get *limited all the metadata in your org
sf project retrieve start
- requires source tracking enabled, defualt on scratch orgs
- this gets all the components that are tracked by source tracking
- only works for scratch orgs, dev, and dev pro sandboes

there is a 3rd option:
- use the * command for all available types.
- get file from other laptop

there is a 4th option: 
- use the cli to download all of your change sets, merge into one manifest and then download

sf project retrieve can pull down one or more change sets
- using a cusotm program those change sets can be merged into a single change set and/or reviewed 

* merge existing manifest files into one
* sf-git-delta to generate a manifest based on two different commits


## Backup Metadata
sf project retrieve preview
- will list all the components that will be retrieved and deleted as well as conflicts and files not retrievede form force ignore
--json
--ignore-conflicts
--target-org

sf project retrieve preview --target-org sampleOrg --json

sf project retrieve start
- default value is to retrieve in source format but can retrieve in metadata format using flag
--json
--api-version
--ignore-conflicts
--manifest
--metadata
--package-name
--output-dir
--single-package
--source-dir
--target-metadata-dir: returns files in metadata format
--target-org
--wait
--unzip
--zip-file-name

using the sf project generate manifest --from-org command will generate a massive manifest file that can then be used to download the entire orgs metadata and used as a backup. Pair this with git and salesforce-git-delta and the command will create another manifest with just the updated components

* problem with downloadning using multiple --package-name
* problem with overloadingn a command that supports multiple entries --tests test1 test2 test3
* problem when downloading object instead of just custom fields, make sure to add them if and only if you really want everything
* reasons to download using metadata format - more control of multiple packages
* why its important to use teh --api-version, the system will choose the most appropraite sometimes its v45, v57, or v58 which causes issues with preview vs non-preview boxes or some metadata isn't yet upgraded/supported like flows

sf project retrieve start --target-org dev1 --target-metadata-dir md --api-version 57.0 --json
sf project retrieve start --target-org dev1 --manifest insert/local/manifest --api-version --json

*usually have to convert metadata format to source format or will need to specify deploy using metadata format

##  Validate Metadata/ Apex

sf project deploy preview
--json
--ignore-conflicts
--manifest
--metadata
--source-dir
--target-org

* run from within project
* ists what will be deployed and deleted, as well as conflicts between local and org, and any files in the .forceignore file

sf project deploy validate 
--json
--api-version
--async
--concise
--manifest
--source-dir
--metadata-dir
--single-package
--target-org
--tests: multiple format
--test-level: RunSpecifiedTests,RunLocalTests,RunAllTestsInOrg
--verbose
--wait
--coverage-formatters: this is new and I've not used them yet
--junit
--results-dir: if using junit 
--purge-on-delete: destructive manifest file are immediately eligible for deletion, no recycle bin
--pre-destructive-changes
--post-destructive-changes

* this command requires apex tests and it returns a job id rather than execting, useful for quick deploy
* either specify either souree-dir or metadata or manifest file
* used to auto enable flows

sf project deploy start --dry-run --test-level NoTest is an option but I don't recommend, too close to accidently deploy when you don't mean to

sf project deploy validate --target-org test1  --manifest insert/local/manifest test-level RunSpecifiedTests --tests ""  --api-version 57.0 --json
* was previously able to run without specifiying tests

sf project deploy validate --target-org test1  --source-dir force-app test-level RunSpecifiedTests --tests test1 test2 test3  --api-version 57.0 --json

sf project deploy validate --target-org test1  --source-dir force-app test-level RunSpecifiedTests --tests test1 --tests test2  --api-version 57.0 --json

* in a CLI you can write a script to scan for and include the Apex Tests
* talk about the new pre/post/purge on delete options and the scenarious when to use them

## Deploy Metadata

sf project deploy start
- default is source format, can push metadata format but needs another command
--json
--api-version
--async
--concise
--dry-run: Validate deploy and run Apex tests but don’t save to the org
--ignore-conflicts: can be useful for occasional conflicts, most often not needed
--ignore-errors: not recommended
--ignore-warnings: enable warnings to fail a deployment
--manifest
--metadata
--single-package
--source-dir
--target-org
--tests
--test-level:NoTestRun*,RunSpecifiedTests,RunLocalTests,RunAllTestsInOrg
--verbose
--wait
--purge-on-delete: destructive manifest file are immediately eligible for deletion, no recycle bin
--pre-destructive-changes
--post-destructive-changes
--coverage-formatters
--junit
--resutls-dir

* used to auto enable flows
* issue when using --tests test1 test2 test3, preference with --tests test1 --tests test2
* when you can use the NoTestRun flag

sf project deploy start --target-org test --manifest path/to/local --test-level RunSpecifiedTests --tests test1 --tests test2 --api-version 57.0 --json

sf project deploy start --target-org test --source-dir force-app --test-level RunSpecifiedTests --tests test1 --tests test2 --api-version 57.0 --json


# ***** Notes *****
jq is really powerful tool for working with cli, use the --json flag when possible