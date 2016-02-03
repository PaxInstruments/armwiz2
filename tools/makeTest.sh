#!/bin/sh

## Do this for each project {
mkdir test
cd test
git init
mkdir libraries
mkdir .git/modules
# }

# If including CMSIS {
# TODO check to see if the library is already pulled from github. Maybe just do a 'git submodule <module> --init' right away
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

# Download STM32SubeF1 from http://www.st.com/web/en/catalog/tools/PF260820#
# TODO Add these to a github repo
# TODO Add the github repos to armwiz
wget -c http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef1.zip
wget -c http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef2.zip
wget -c http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef3.zip
wget -c http://www.st.com/st-web-ui/static/active/en/st_prod_software_internet/resource/technical/software/firmware/stm32cubef4.zip
unzip stm32cubef1.zip 

## Project Types
- cmsis - Based only on CMSIS. Do not use any GPIO or any perpherials. Just use a loop
  to iterate over a variable. Maybe use printf if possible. This project can only rely
  on CMSIS libraries; no vendor specific code.
- sm32 - Uses ST perpherial libraries and CMSIS.
- mbed - Based on mbed, which includes CMSIS. This will only work on boards supported
  by the mbed platform




