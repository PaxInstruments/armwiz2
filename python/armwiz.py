#!/usr/bin/env python3

# Project TODO List
# TODO Add a function to pull in the desired submodules.
# TODO Check if required submodule is present.
# TODO Generate Makefile from template
# TODO Generate examples. Modify based on configuration for appropriate LEDs etc.
# TODO Use rsync for copying FreeRTOS
# TODO Generate FreeRTOSConfig.h
# TODO Made an example file specfically for each board and configuration. The
#      examples must be tailored rather than generated. Generating them on the
#      fly would be unweildy.
# TODO Make FreeRTOS checkout th emost recent version from the tags
# TODO Make FreeRTOS and ChibiOS mutually exclusive
# TODO Initialize a new project as a git repository. Maybe have a command flag for this.


# TODO: Add information here.
"""
Armwiz docstring.
"""
#                         ____
#                       .'* *.'
#                    __/_*_*(_
#                   / _______ \
#                  _\_)/___\(_/_
#                 / _((\- -/))_ \
#                 \ \())(-)(()/ /
#                  ' \(((()))/ '
#                 / ' \)).))/ ' \
#                / _ \ - | - /_  \
#               (   ( .;''';. .'  )
#               _\"__ /    )\ __"/_
#                 \/  \   ' /  \/
#                  .'  '...' ' )
#                   / /  |  \ \
#                  / .   .   . \
#                 /   .     .   \
#                /   /   |   \   \
#              .'   /    b    '.  '.
#          _.-'    /     Bb     '-. '-._
#      _.-'       |      BBb       '-.  '-.
#     (__________/\____.dBBBb.________)____)
#  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
# ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
# ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝ 
# ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝  
# ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝

import subprocess
from subprocess import call
import os
import sys
import errno
import argparse

__author__ = "Charles Edward Pax"
__copyright__ = "Copyright 2016, Pax Instruments LLC"
__date__ = "2016"
__credits__ = ["Charles Pax"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Charles Pax"
__email__ = "charles.pax@gmail.com"
__status__ = "Development"

#######################
## Class definitions ##
#######################
class core(object):
	"""The MCU core designed by ARM."""
	def __init__(self,name,architecture):
		self.name=name
		self.architecture=architecture

class manufacturer(object):
	"""The manufacturer of an object"""
	def __init__(self,name,website):
		self.name=name
		self.website=website

class mcu(object):
	"""Microcontroller IC."""
	def __init__(self,name,manufacturer,core):
		self.name=name
		self.manufacturer=manufacturer
		self.architecture=core

class board(object):
	"""Development board or product"""
	def __init__(self,name,manufacturer,mcu,website):
		self.name=name
		self.manufacturer=manufacturer
		self.mcu=mcu
		self.website=website

class target(object):
	"""The target for which armwiz will generate a project. This could be
	a development board or just an MCU."""
	def __init__(self,name,manufacturer):
		self.name=name
		self.manufacturer=manufacturer
		self.mcu=mcu

##########################
## Function definitions ##
##########################
def printWizard():
	print("                             ____                   ")
	print("                          .'* *.'                   ")
	print("                       __/_*_*(_                    ")
	print("                      / _______ \                   ")
	print("                     _\_)/___\(_/_                  ")
	print("                    / _((\- -/))_ \                 ")
	print("                    \ \())(-)(()/ /                 ")
	print("                     ' \(((()))/ '                  ")
	print("                    / ' \)).))/ ' \                 ")
	print("                   / _ \ - | - /_  \                ")
	print("                  (   ( .;''';. .'  )               ")
	print("                  _\\\"__ /    )\ __\"/_            ")
	print("                    \/  \   ' /  \/                 ")
	print("                     .'  '...' ' )                  ")
	print("                      / /  |  \ \                   ")
	print("                     / .   .   . \                  ")
	print("                    /   .     .   \                 ")
	print("                   /   /   |   \   \                ")
	print("                 .'   /    b    '.  '.              ")
	print("             _.-'    /     Bb     '-. '-._          ")
	print("         _.-'       |      BBb       '-.  '-.       ")
	print("        (__________/\____.dBBBb.________)____)      ")

def printHeader():
	print("     █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗")
	print("    ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝")
	print("    ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝ ")
	print("    ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝  ")
	print("    ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗")
	print("    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝")
	print("                                      version",__version__ )

def parseArguments():
	"""Parses command line arguments. Returns array."""
	parser = argparse.ArgumentParser(
		description='Generate a template embedded ARM project.',
		epilog="armwiz 2016")
	parser.add_argument('-p','--projectname',
		help='Specify project name via -p <projectname>',
		metavar="<projectname>",
		required=True)
	parser.add_argument('-t','--target',
		help='Specify target microcontroller via -t <targetname>',
		metavar="<targetname>",
		required=True)
	parser.add_argument('--chibios',
		help='Include ChibiOS libraries',
		action="store_true",
		required=False)
	parser.add_argument('--freertos',
		help='Include FreeRTOS libraries',
		action="store_true",
		required=False)
	parser.add_argument('--mbed',
		help='Include mbed libraries',
		action="store_true",
		required=False)
	parser.add_argument('--targetlist',
		help='Print a list of available targets',
		action="store_true",
		required=False)
	parser.add_argument('-w','--wizard',
		help='Print the wizard',
		action="store_true",
		required=False)
	parser.add_argument('-v','--version',
		version='%(prog)s {version}'.format(version=__version__),
		action='version')
	return parser.parse_args()

def targetDetailPrint(targetBoard):
	"""Print detail of the target board"""
	# TODO Make object methods for these actions. For example:
	#      'myBoard.print(name)' #prints the board name
	print('Target:', targetBoard.name)
	print('    Board manufacturer:',targetBoard.manufacturer.name)
	print('    Board MCU:',targetBoard.mcu.name)
	print('    MCU manufacturer:',targetBoard.mcu.manufacturer.name)
	print('    Board website:',targetBoard.website)

def makePath(path):
	"""Make a directory path."""
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno == errno.EEXIST:
			print('ERROR',path,'already exists.')
		else:
			print('ERROR: UNKNOWN')
			raise
		exit()

def makeProjectDirectoryTree(arguments):
	"""
	Make project directory tree
	Takes <projectname> as argument
	"""
	makePath(arguments.projectname)
	makePath('%s/binary' % arguments.projectname)
	makePath('%s/include' % arguments.projectname)
	makePath('%s/libraries' % arguments.projectname)
	makePath('%s/source' % arguments.projectname)
	makePath('%s/tools' % arguments.projectname)
	call(['git','init',arguments.projectname])
	makePath('%s/.git/modules' % arguments.projectname)
	makePath('%s/.git/modules/libraries' % arguments.projectname)

def deployMakefile(arguments):
	"""
	# Generate the Makefile
	# Takes <projectname> as argument
	"""
	# echoMakefile > $(pwd)/$1/Makefile

def deployExample(arguments):
	"""
	Generate the Makefile
	Takes <projectname> as argument
	"""
	# echoExample > $(pwd)/$1/src/${projectname}.cpp

def deployChibiOS (arguments):
	"""
	deployChibiOS
	"""
	if arguments.chibios:
		print('Copying ChibiOS libraries... ',end="")
		sys.stdout.flush()
		try:
			makePath('%s/libraries/ChibiOS' % arguments.projectname)
			call(['rsync','-ac',"--exclude='.DS_Store'",'../libraries/ChibiOS/','%s/libraries/ChibiOS' % arguments.projectname])
			call(['rsync','-ac',"--exclude='.DS_Store'",'../.git/modules/libraries/ChibiOS','%s/.git/modules/libraries/ChibiOS' % arguments.projectname])
			moduleFile = open('%s/.gitmodules' % arguments.projectname, 'a')
			moduleFile.write("\n[submodule \"libraries/ChibiOS\"]\n\tpath = libraries/ChibiOS\n\turl = https://github.com/ChibiOS/ChibiOS.git\n")
			moduleFile.close()
			print('Okay')
		except:
			print('ERROR copying')
			exit()

		
def deployFreeRTOS (arguments):
	"""
	deployFreeRTOS
	"""
	if arguments.freertos:
		print('Copying FreeRTOS libraries... ',end="")
		sys.stdout.flush()
		try:
			makePath('%s/libraries/freertos' % arguments.projectname)
			call(['rsync','-ac',"--exclude='.DS_Store'",'../libraries/freertos/','%s/libraries/freertos' % arguments.projectname])
			call(['rsync','-ac',"--exclude='.DS_Store'",'../.git/modules/libraries/freertos','%s/.git/modules/libraries/freertos' % arguments.projectname])
			moduleFile = open('%s/.gitmodules' % arguments.projectname, 'a')
			moduleFile.write("\n[submodule \"libraries/freertos\"]\n\tpath = libraries/freertos\n\turl = https://github.com/PaxInstruments/freertos.git\n")
			moduleFile.close()
			print('Okay')
		except:
			print('ERROR copying')
			exit()


def deployMbed (arguments):
	"""
	deployMbed
	"""
	if arguments.mbed:
		print('Copying mbed libraries... ',end="")
		sys.stdout.flush()
		try:
			makePath('%s/libraries/mbed' % arguments.projectname)
			call(['rsync','-ac',"--exclude='.DS_Store'",'../libraries/mbed/','%s/libraries/mbed' % arguments.projectname])
			call(['rsync','-ac',"--exclude='.DS_Store'",'../.git/modules/libraries/mbed','%s/.git/modules/libraries/modules' % arguments.projectname])
			moduleFile = open('%s/.gitmodules' % arguments.projectname, 'a')
			moduleFile.write("\n[submodule \"libraries/mbed\"]\n\tpath = libraries/mbed\n\turl = https://github.com/mbedmicro/mbed.git\n")
			moduleFile.close()
			print('Okay')
		except:
			print('ERROR copying')
			exit()


##################
## Object lists ##
##################

## List of Manufacturers
manufacturer_unknown = manufacturer('unknown','none')
manufacturer_ARM = manufacturer('ARM','https://www.arm.com/')
manufacturer_Atmel = manufacturer('Atmel','http://www.atmel.com/')
manufacturer_ST = manufacturer('ST Microsystems','http://www.st.com/')
manufacturer_micropython = manufacturer('micropython.org','http://micropython.org/')

## List of Cores
core_ARMCorte_M0 = core('ARM Cortex-M0','ARMv6-M')
core_ARMCorte_M0Plus = core('ARM Cortex-M0','ARMv6-M')
core_ARMCorte_M1 = core('ARM Cortex-M0','ARMv6-M')
core_ARMCorte_M3 = core('ARM Cortex-M0','ARMv7-M')
core_ARMCorte_M4 = core('ARM Cortex-M0','ARMv7E-M')

## List of MCUs
# TODO Make this such that we only declare the mcu variables when required; not all at once.
mcu_atsamd21j18a = mcu('SAMD21J12A',manufacturer_Atmel,core_ARMCorte_M0Plus)
mcu_stm32f103rct6 = mcu('STM32F103RCT6',manufacturer_ST,core_ARMCorte_M3)
mcu_stm32f103c8t6 = mcu('STM32F103C8T6',manufacturer_ST,core_ARMCorte_M3)
mcu_stm32f407vgt6 = mcu('STM32F407VGT6',manufacturer_ST,core_ARMCorte_M4)
mcu_stm32f411ret6 = mcu('STM32F411RET6',manufacturer_ST,core_ARMCorte_M4)
mcu_stm32f405rgt6 = mcu('STM32F405RGT6',manufacturer_micropython,core_ARMCorte_M4)

## List of boards
# TODO Make this into a list, so I can iteratively search through
# TODO Make this such that we only declare the board variables when required; not all at once.
board_atmel_samd21xplainedpro = board('SAMD21 Xplained Pro',manufacturer_Atmel,mcu_atsamd21j18a,'http://www.atmel.com/tools/ATSAMD21-XPRO.aspx')
board_china_130811_v100 = board('Generic 130811_v1.00',manufacturer_unknown,mcu_stm32f103rct6,'https://github.com/PaxInstruments/armwiz/wiki/130811_v100')
board_china_stm32f103rct6_v102 = board('Generic STM32F103RCT6 V1.02',manufacturer_unknown,mcu_stm32f103rct6,'https://github.com/PaxInstruments/armwiz/wiki/stm32f103rct6_v102')
board_china_stm32f1c8t6_Board_v402 = board('Generic STM32F1x8x6 Board_v4.02',manufacturer_unknown,mcu_stm32f103c8t6,'https://github.com/PaxInstruments/armwiz/wiki/stm32f1c8t6_Board_v402')
board_stmt3f4discovery = board('STM32F4 Discovery',manufacturer_ST,mcu_stm32f407vgt6,'http://www.st.com/web/catalog/tools/FM116/SC959/SS1532/PF252419')
board_nucleo_f411re = board('Nucleo-F411RE',manufacturer_ST,mcu_stm32f411ret6,'http://www.st.com/web/catalog/tools/FM116/SC959/SS1532/LN1847/PF260320')
board_pyboard_v10 = board('PyBoard v1.0',manufacturer_micropython,mcu_stm32f405rgt6,'http://docs.micropython.org/en/latest/pyboard/hardware/index.html')

def main():
	"""The main program loop"""
	arguments = parseArguments()

	if arguments.wizard == True:
		printWizard()

	if arguments.projectname:
		makeProjectDirectoryTree(arguments)

	if arguments.chibios == True:
		deployChibiOS(arguments)

	if arguments.freertos == True:
		deployFreeRTOS(arguments)

	if arguments.mbed == True:
		deployMbed(arguments)

	print(arguments)
	# print("Project name: %s" % arguments.projectname )
	# print("Target name: %s" % arguments.target )
	# directory = "tempDir"

	# targetDetailPrint(board_atmel_samd21xplainedpro)
	# targetDetailPrint(board_china_130811_v100)
	# targetDetailPrint(board_china_stm32f103rct6_v102)
	#targetDetailPrint(board_china_stm32f1c8t6_Board_v402)
	# targetDetailPrint(board_stmt3f4discovery)
	# targetDetailPrint(board_nucleo_f411re)
	# targetDetailPrint(board_pyboard_v10)

if __name__ == "__main__":
	# TODO Read about python file structure
	#      https://www.artima.com/weblogs/viewpost.jsp?thread=4829
	main()














