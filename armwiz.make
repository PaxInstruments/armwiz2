#!/bin/sh

# TODO
# - Add linker script based on armwiz.conf
# - Add TOOLCHAIN_PATH as a variable. Add in front of toolchain commands

# Path to toolchain directory. Requires a "/" on the end.
# TODO Make a command flag to define the toolchain location


function echoMakefile () {
	# Header information
	echo "###"
	echo "# This Makefile is generated by $ARMWIZ_COMMAND $ARMWIZ_VERSION"
 	echo ""
	echo "# TODO Make variable for toolchain location. Prepend to the toolchain list below"
	echo ""
	echo "###########################"
	echo "## User Definable Items ###"
	echo "###########################"
	echo ""
	echo "OPENOCD_BOARD_CONFIG_FILE=board/stm32f4discovery.cfg"
	echo ""
	echo "# Define output files ELF & IHEX"
	echo "BINELF=${projectname}.elf"
	echo "BINHEX=${projectname}.hex"
	echo ""
	echo "#################"
	echo "### Toolchain ###"
	echo "#################"
	echo ""
	echo "# GNU ARM Embedded Toolchain"
	echo "TOOLCHAIN_PATH=  # Requires a '/' on the end."
	echo "CC=\${TOOLCHAIN_PATH}arm-none-eabi-gcc"
	echo "CXX=\${TOOLCHAIN_PATH}arm-none-eabi-g++"
	echo "LD=\${TOOLCHAIN_PATH}arm-none-eabi-ld"
	echo "AR=\${TOOLCHAIN_PATH}arm-none-eabi-ar"
	echo "AS=\${TOOLCHAIN_PATH}arm-none-eabi-as"
	echo "CP=\${TOOLCHAIN_PATH}arm-none-eabi-objcopy"
	echo "OD=\${TOOLCHAIN_PATH}arm-none-eabi-objdump"
	echo "NM=\${TOOLCHAIN_PATH}arm-none-eabi-nm"
	echo "SIZE=\${TOOLCHAIN_PATH}arm-none-eabi-size"
	echo "A2L=\${TOOLCHAIN_PATH}arm-none-eabi-addr2line"
	echo ""
	echo "# OpenOCD"
	echo "OPENOCD_PATH=   # Requires a '/' on the end."
	echo "OPENOCD=openocd"
	echo ""
	echo "# Directory Structure"
	echo "BINDIR=bin"
	echo "INCDIR=inc"
	echo "SRCDIR=src"
	echo "LIBDIR=lib"
	echo ""
	echo "####################"
	echo "### Find Sources ###"
	echo "####################"
	echo "# Find source files"
	echo "ASOURCES=\$(shell find -L \$(SRCDIR) -iname '*.s')"
	echo "ASOURCES+=\$(shell find -L \$(LIBDIR) -iname '*.s')"
	echo "CSOURCES=\$(shell find -L \$(SRCDIR) -iname '*.c')"
	echo "CSOURCES+=\$(shell find -L \$(LIBDIR) -iname '*.c')"
	echo "CXXSOURCES=\$(shell find -L \$(SRCDIR) -iname '*.cpp')"
	echo "CXXSOURCES+=\$(shell find -L \$(LIBDIR) -iname '*.cpp')"
	echo ""
	echo "# Find header directories"
	echo "INC=\$(shell find -L \$(INCDIR) -iname '*.h' -exec dirname {} \; | uniq)"
	echo "INC+=\$(shell find -L \$(LIBDIR) -iname '*.h' -exec dirname {} \; | uniq)"
	echo "INCLUDES=\$(INC:%=-I%)"
	echo ""
	echo "# Find libraries"
	echo "INCLUDES_LIBS="
	echo "LINK_LIBS="
	echo ""
	echo "# Create object list"
	echo "OBJECTS=\$(ASOURCES:%.s=%.o)"
	echo "OBJECTS+=\$(CSOURCES:%.c=%.o)"
	echo "OBJECTS+=\$(CXXSOURCES:%.cpp=%.o)"
	echo ""
	echo "################"
	echo "### Compiler ###"
	echo "################"
	echo "# MCU Flags"
	echo "MCFLAGS=$GCC_MCFLAGS"
	echo ""
	echo "# Compile Flags"
	echo "DEFS=$GCC_COMPILE_FLAGS_DEFS"
	echo "CFLAGS=$GCC_COMPILE_FLAGS_CFLAGS"
	echo "CXXFLAGS=$GCC_COMPILE_FLAGS_CXXFLAGS"
	echo ""
	echo "# Linker Flags"
	echo "LDSCRIPT=$MBED_TARGET_LINKER_SCRIPT"
	echo "LDFLAGS =$GCC_LINKER_FLAGS"
	echo ""
	echo "###################"
	echo "### Build Rules ###"
	echo "###################"
	echo "# Build Rules"
	echo ".PHONY: all release release-memopt debug clean"
	echo ""
	echo "all: release-memopt"
	echo ""
	echo "release-memopt-blame: CFLAGS+=-g"
	echo "release-memopt-blame: CXXFLAGS+=-g"
	echo "release-memopt-blame: LDFLAGS+=-g -Wl,-Map=\$(BINDIR)/output.map"
	echo "release-memopt-blame: release-memopt"
	echo "release-memopt-blame:"
	echo "	@echo \"Top 10 space consuming symbols from the object code ...\\\n\""
	echo "	\$(NM) -A -l -C -td --reverse-sort --size-sort \$(BINDIR)/\$(BINELF) | head -n10 | cat -n # Output legend: man nm"
	echo "	@echo \"\\\n... and corresponging source files to blame.\\\n\""
	echo "	\$(NM) --reverse-sort --size-sort -S -tx \$(BINDIR)/\$(BINELF) | head -10 | cut -d':' -f2 | cut -d' ' -f1 | \$(A2L) -e \$(BINDIR)/\$(BINELF) | cat -n # Output legend: man addr2line"
	echo ""
	echo "release-memopt: DEFS+=-DCUSTOM_NEW -DNO_EXCEPTIONS"
	echo "release-memopt: CFLAGS+=-Os -ffunction-sections -fdata-sections -fno-builtin # -flto"
	echo "release-memopt: CXXFLAGS+=-Os -fno-exceptions -ffunction-sections -fdata-sections -fno-builtin -fno-rtti # -flto"
	echo "release-memopt: LDFLAGS+=-Os -Wl,-gc-sections --specs=nano.specs # -flto"
	echo "release-memopt: release"
	echo ""
	echo "debug: CFLAGS+=-g"
	echo "debug: CXXFLAGS+=-g"
	echo "debug: LDFLAGS+=-g"
	echo "debug: release"
	echo ""
	echo "release: \$(BINDIR)/\$(BINHEX)"
	echo ""
	echo "\$(BINDIR)/\$(BINHEX): \$(BINDIR)/\$(BINELF)"
	echo "	\$(CP) -O ihex \$< \$@"
	echo "	@echo \"Objcopy from ELF to IHEX complete!\\\n\""
	echo ""
	echo "\$(BINDIR)/\$(BINELF): \$(OBJECTS)"
	echo "	\$(CXX) \$(OBJECTS) \$(LDFLAGS) -o \$@"
	echo "	@echo \"Linking complete!\\\n\""
	echo "	\$(SIZE) \$(BINDIR)/\$(BINELF)"
	echo ""
	echo "%.o: %.cpp"
	echo "	\$(CXX) \$(CXXFLAGS) \$< -o \$@"
	echo "	@echo \"Compiled \"\$<\"!\\\n\""
	echo ""
	echo "%.o: %.c"
	echo "	\$(CC) \$(CFLAGS) \$< -o \$@"
	echo "	@echo \"Compiled \"\$<\"!\\\n\""
	echo ""
	echo "%.o: %.s"
	echo "	\$(CC) \$(CFLAGS) \$< -o \$@"
	echo "	@echo \"Assambled \"\$<\"!\\\n\""
	echo ""
	echo "clean:"
	echo "	rm -f \$(OBJECTS) \$(BINDIR)/\$(BINELF) \$(BINDIR)/\$(BINHEX) \$(BINDIR)/output.map"
	echo ""
	echo "#################################"
	echo "### Programming and debugging ###"
	echo "#################################"
	echo "deploy:"
	echo "	\${OPENOCD_PATH}\${OPENOCD} -f \${OPENOCD_BOARD_CONFIG_FILE} -c \"program \${BINDIR}/\"\${BINELF}\" verify reset\""
	echo ""
}
