#====================================================================#
#Output files
EXECUTABLE=stm32_executable.elf
BIN_IMAGE=stm32_bin_image.bin

#======================================================================#
#Cross Compiler
CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy

#======================================================================#
#Flags
CFLAGS=-Wall -g -mlittle-endian -mthumb -nostdlib -ffreestanding
CFLAGS+=-mcpu=cortex-m3
CFLAGS+=-D USE_STDPERIPH_DRIVER
CFLAGS+=-I./
CFLAGS+=-D STM32F10X_HD


#stm32-flash
CFLAGS+=-Wl,-T,STM32F103XE_FLASH.ld
#CFLAGS+=-Wl,-T,stm32_flash.ld

#======================================================================#
#Libraries

#Stm32 libraries
#ST_LIB=stm32-libraries/inc

#CMSIS libraries
CFLAGS+=-Iinclude
#CFLAGS+=-Ilibraries/STM32CubeF1/Drivers/CMSIS/Device/ST/STM32F1xx/Include/
#======================================================================#
#setup system clock
SRC=./system_stm32f10x.c
#StdPeriph
SRC+=include/misc.c \
	include/stm32f10x_rcc.c \
	include/stm32f10x_gpio.c \

#Major programs
SRC+=./main.c \

#======================================================================#
#STM32 startup file
STARTUP=./startup_stm32f103xe.s


#======================================================================#
#Make rules

#Make all
all:$(BIN_IMAGE)

$(BIN_IMAGE):$(EXECUTABLE)
	$(OBJCOPY) -O binary $^ $@

STARTUP_OBJ = startup_stm32f103xe.o

$(STARTUP_OBJ): $(STARTUP) 
	$(CC) $(CFLAGS) $^ -c $(STARTUP)

$(EXECUTABLE):$(SRC) $(STARTUP_OBJ)
	$(CC) $(CFLAGS) $^ -o $@

#Make clean
clean:
	rm -rf *.bin *.elf *.o
#Make flash
flash:
	st-flash write $(BIN_IMAGE) 0x8000000
openocd:
	openocd -f "../commom/openocd.cfg"
gdb:
	arm-none-eabi-gdb -x ../commom/gdb_init.gdb
gdbtui:
	arm-none-eabi-gdb -tui -x ../commom/gdb_init.gdb
#======================================================================
.PHONY:all clean flash
