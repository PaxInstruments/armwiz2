# STM32 Development Environment

## Overview
The goal of this project is to create a system that easily generates STM32 ARM microcontroller projects using command line tools. This is a fork of [Iztok Starc's original repository](https://github.com/istarc/stm32) and at this point is entirely Iztok's work. Over time we hope to extend his project and generalize the system to support additional microcontroller and boards beyond the STM32F4-Discovery board.

Build and Test Environment based on Ubuntu 14.04 LTS for the STM32F4-Discovery board.

## File Organization

- [examples](https://github.com/istarc/stm32/tree/master/examples) - Example projects
- [build-ARM-toolchain](http://istarc.wordpress.com/2014/07/21/stm32f4-build-your-toolchain-from-scratch/) - Compile the ARM toolchain from scratch.
- [freertos](https://github.com/istarc/freertos) - FreeRTOS as a git submodule that is not tracked in this repository. It is automatically downloaded from https://github.com/PaxInstruments/freertos.
- [mbed](http://mbed.org/) - mbed as a git submodule that is not tracked in this repository. It is automatically downloaded from https://github.com/mbedmicro/mbed.
- [mbed-project-wizard](http://istarc.wordpress.com/2014/08/04/stm32f4-behold-the-project-wizard/) - A wizard that generates STM32 project templates.
- [STM32F4-Discovery_FW_V1.1.0 library](http://www.st.com/web/catalog/tools/FM116/SC959/SS1532/PF252419) library
- [test]()

## How to Setup the Environment
### 2.1 Ubuntu 14.04 LTS Users

Ubuntu 14.04 LTS users install the environment directly on host OS. :-)

    cd ~
    sudo apt-get install git
    git clone https://github.com/paxinstruments/stm32.git
    cd ~/stm32
    git submodule update --init
    ./setup-env.sh

## Usage
### 3.1 Build Existing Projects

    cd ~/stm32/
    make clean
    make -j4

### 3.2 Deploy an Existing Project

    cd ~/stm32/examples/Template.mbed
    make clean
    make -j4
    sudo make deploy

## More Info

 - [http://istarc.wordpress.com/][1]
 - [https://github.com/istarc/stm32][2]
 - [https://registry.hub.docker.com/u/istarc/stm32/][3]
 - [https://vagrantcloud.com/istarc/stm32][4]

  [1]: http://istarc.wordpress.com/
  [2]: https://github.com/istarc/stm32
  [3]: https://registry.hub.docker.com/u/istarc/stm32/
  [4]: https://vagrantcloud.com/istarc/stm32

