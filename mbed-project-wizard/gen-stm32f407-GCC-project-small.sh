#!/bin/bash

set -e
### Variables:
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPTNAME="$(basename $0)"
BASEDIR=$SCRIPTDIR/..
MBED=$BASEDIR/mbed/libraries/mbed
FREERTOS=$BASEDIR/freertos/FreeRTOS
LINKER_SCRIPT=STM32F407.ld

##
# Check if project directory is emtpy
STATUS=$(ls)
if [[ "$STATUS" ]]; then
	echo "Project directory is not empty!"
	exit 1
fi

##
# Create directory structure
do_create_dir() {
mkdir -p $(pwd)/bin
touch $(pwd)/bin/.gitkeep # A dummy file to keep directory structure in place
mkdir -p $(pwd)/inc
echo 'Your application header files (*.h).' > $(pwd)/inc/README
mkdir -p $(pwd)/lib
echo 'Place third-party source code or libraries here.' > $(pwd)/lib/README
mkdir -p $(pwd)/src
echo 'Your application source files (*.c, *.cpp, *.s).' > $(pwd)/src/README
}

##
# Deploy mbed SDK and tailor to fit STM32F4XX and GCC
do_deploy_mbed() {
cp -LR $MBED $(pwd)/lib/mbed
cp `find . | grep "$LINKER_SCRIPT"` $LINKER_SCRIPT

}

##
# Deploy FreeRTOS and tailor to fit STM32F4XX and GCC
do_deploy_freertos() {
cp -LR $FREERTOS $(pwd)/lib/FreeRTOS
# Copy FreeRTOSConfig.h
mkdir $(pwd)/lib/FreeRTOS/config/
cp $SCRIPTDIR/freertos/FreeRTOSConfig.h $(pwd)/lib/FreeRTOS/config/FreeRTOSConfig.h
if [[ "$1" == "link" ]]; then
	# Abs to Rel Symlinks
	symlinks -rc $(pwd) 1>/dev/null
fi
}

case "$1" in
  mbed-none)
	echo "Project template created by ${0##*/} $1" > $(pwd)/README
	echo "   mbed-none ... creates a bare-metal project with mbed SDK" >> $(pwd)/README
	echo "" >> $(pwd)/README
	echo "Usage: make && sudo make deploy" >> $(pwd)/README
	echo "" >> $(pwd)/README
	echo "Git info:" >> $(pwd)/README
	echo "   stm32:    "$(cd $BASEDIR && git rev-parse --short=10 HEAD)" ("$(cd $BASEDIR && git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2>/dev/null)")" >> $(pwd)/README
	echo "   mbed:     "$(cd $BASEDIR/mbed && git rev-parse --short=10 HEAD)" ("$(cd $BASEDIR/mbed && git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2>/dev/null)")" >> $(pwd)/README
	do_create_dir $2
	do_deploy_mbed $2
	cp $SCRIPTDIR/mbed-none/main.cpp $(pwd)/src/main.cpp
	cp $SCRIPTDIR/mbed-none/Makefile $(pwd)/Makefile
	# Print usage instructions
	cat README
	;;
  mbed-freertos)
	echo "Project template created by ${0##*/} $1" > $(pwd)/README
	echo "   mbed-freertos ... creates a FreeRTOS project with mbed SDK (/w libraries)" >> $(pwd)/README
	echo "" >> $(pwd)/README
	echo "Usage: make && sudo make deploy" >> $(pwd)/README
	echo "" >> $(pwd)/README
	echo "Git info:" >> $(pwd)/README
	echo "   stm32:    "$(cd $BASEDIR && git rev-parse --short=10 HEAD)" ("$(cd $BASEDIR && git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2>/dev/null)")" >> $(pwd)/README
	echo "   mbed:     "$(cd $BASEDIR/mbed && git rev-parse --short=10 HEAD)" ("$(cd $BASEDIR/mbed && git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2>/dev/null)")" >> $(pwd)/README
	#echo "   freertos: "$(cd $BASEDIR/freertos && git rev-parse --short=10 HEAD)" ("$(cd $BASEDIR/cpputest && git symbolic-ref -q --short HEAD || git describe --tags --exact-match 2>/dev/null)")" >> $(pwd)/README
	do_create_dir $2
	do_deploy_mbed $2
	do_deploy_freertos
	cp $SCRIPTDIR/mbed-freertos/main.cpp $(pwd)/src/main.cpp
	cp $SCRIPTDIR/mbed-freertos/Makefile $(pwd)/Makefile
	# Print usage instructions
	cat README
	;;
  *)
	exit 3
	;;
esac
