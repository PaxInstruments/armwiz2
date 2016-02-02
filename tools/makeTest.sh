#!/bin/sh

## Do this for each project {
mkdir test
cd test
git init
mkdir libraries
mkdir .git/modules
# }

# If including CMSIS {
rsync -ac --exclude=".DS_Store" ~/Desktop/arm-dev/armwiz/.git/modules/CMSIS .git/modules
rsync -ac --exclude=".DS_Store" ~/Desktop/arm-dev/armwiz/libraries/CMSIS/ libraries/CMSIS
echo "gitdir: ../../.git/modules/CMSIS" > libraries/CMSIS/.git
echo "\
[submodule "CMSIS"]
	path = libraries/CMSIS
	url = https://github.com/ARM-software/CMSIS
" >> .gitmodules
# TODO check out the most recent version
# TODO echo version to README file
# TODO echo relevant instrucitons to README file
# }

