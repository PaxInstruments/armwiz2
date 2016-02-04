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
		default='helloArmwiz',
		required=False)
	parser.add_argument('-t','--target',
		help='Specify target microcontroller via -t <targetname>',
		metavar="<targetname>",
		default='board_china_stm32f1c8t6_Board_v402',
		required=False)
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
			print('ERROR: targetDetailPrint(): The path,',path,'already exists. Stopping armwiz.')
		else:
			print('ERROR: UNKNOWN')
			raise
		exit()

def makeProjectDirectoryTree(arguments):
	"""
	Make project directory tree
	Takes <projectname> as argument
	"""
	print('Creating {0}/ directory:\n'.format(arguments.projectname), end="")
	sys.stdout.flush()
	try:
		makePath(arguments.projectname)
		makePath('%s/binary' % arguments.projectname)
		makePath('%s/include' % arguments.projectname)
		makePath('%s/libraries' % arguments.projectname)
		makePath('%s/source' % arguments.projectname)
		makePath('%s/tools' % arguments.projectname)
		try:
			call('git init {0}'.format(arguments.projectname),shell=True)
		except:
			exit()
		makePath('%s/.git/modules' % arguments.projectname)
		makePath('%s/.git/modules/libraries' % arguments.projectname)
		print('Okay')
	except OSError as exception:
		if exception.errno == errno.EEXIST:
			print('ERROR: MakeProjectDirectoryTree(): A directory already exists.', self)
		else:
			print('ERROR: UNKNOWN')
			raise
		exit()



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

class library(object):
	"""Libraries in git."""
	def __init__(self,name,gitName,parentDir,gitURL):
		self.name=name
		self.gitName=gitName
		self.parentDir=parentDir
		self.gitURL=gitURL
		self.libTargetDir='{0}/{1}{2}'.format('libraries',self.parentDir,self.gitName)
		self.libSourceDir='{0}/{1}{2}'.format('libraries',self.parentDir,self.gitName)

lib_chibios = library('ChibiOS','ChibiOS','','https://github.com/ChibiOS/ChibiOS.git')
lib_freertos = library('FreeRTOS','freertos','','https://github.com/PaxInstruments/freertos.git')
lib_mbed = library('mbed','mbed','','https://github.com/mbedmicro/mbed.git')

def deployLibrary(arguments,library):
	print('Copying {0} libraries...'.format(library.name), end="")
	sys.stdout.flush()
	try:
		makePath("{0}/{1}".format(arguments.projectname,library.libTargetDir))
		#TODO Rewrite the next two lines using one string and 'shell=True'
		call(['rsync','-ac','{0}/'.format(library.libSourceDir),'{0}/{1}/'.format(arguments.projectname,library.libTargetDir)])
		call(['rsync','-ac','.git/modules/{0}/'.format(library.libSourceDir),'{0}/.git/modules/{1}/'.format(arguments.projectname,library.libTargetDir)])
		moduleFile = open('{0}/.gitmodules'.format(arguments.projectname), 'a')
		moduleFile.write("\n[submodule \"{0}\"]\n".format(library.libTargetDir))
		moduleFile.write("\tpath = {0}\n".format(library.libTargetDir))
		moduleFile.write("\turl = {0}\n".format(library.gitURL))
		moduleFile.close()
		print('Okay')
	except:
		print('ERROR copying')
		exit()
	call('cd {0}; git add .gitmodules; git add {1}; git submodule init'.format(arguments.projectname,library.libTargetDir),shell=True)
	call("cd {0}; git commit -am 'armwiz added {1}'".format(arguments.projectname,library.name),shell=True)

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
		try:
			makeProjectDirectoryTree(arguments)
		except:
			exit()

	if arguments.chibios == True:
		try:
			deployLibrary(arguments,lib_chibios)
		except:
			exit()

	if arguments.freertos == True:
		try:
			deployLibrary(arguments,lib_freertos)
		except:
			exit()

	if arguments.mbed == True:
		try:
			deployLibrary(arguments,lib_mbed)
		except:
			exit()

if __name__ == "__main__":
	# TODO Read about python file structure
	#      https://www.artima.com/weblogs/viewpost.jsp?thread=4829
	main()














