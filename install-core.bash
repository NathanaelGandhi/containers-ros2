#! /bin/bash

################################################################################
# ALL DEPS FOR HARDWARE/RUNNERS SHOULD BE INSTALLED HERE                        
# Install all deps via this script. Enables reproduceable target hardware setups
################################################################################

################################################################################
# APT - Note: Architecture agnostic
## Only update if the apt cache is older than 30 days
test "$(find /var/lib/apt/lists/ -maxdepth 1 -type f -mtime -30)" || sudo apt-get update
## build-essential cmake git: required for building from source (in base image)
# python3-pip: required by ros2
# sudo apt-get install -y \
    # package_thing package_thing2 \
    # package_stuff

################################################################################
# PIP - Note: Architecture agnostic
## clang-format from apt is very old (~v14) vs pip v18+
pip install \
    clang-format

################################################################################
# Create directories for filesystem mapping
## Could be mounted as non-volatile memory
sudo mkdir -p /mnt/storage
## Could be mounted as volatile memory
sudo mkdir -p /mnt/ram
sudo mkdir -p /tmp/ram
## Guard against existing symbolic link
if [ ! -L /mnt/ram ]; then
    sudo ln -s /tmp/ram /mnt/ram
fi

################################################################################
# Install from source - Note: Architecture agnostic
## Install EXAMPLE from source
### Set the directory
### Clone the repository
### Create and change to build directory
### Run cmake, make and install
# cd ~ && \
#   git clone -b v2.1.0 https://github.com/EXAMPLE/example.git && \
#   mkdir -p ~/example/build && cd ~/example/build && \
#   cmake .. && make install

################################################################################
# Architecture specific installs
## Detect architecture
arch=$(uname -m)
## Determine the appropriate installation package or binary
case $arch in
  x86_64|i386|i686)
    echo "Detected architecture: x86 or x86_64"
    # Add commands to install packages for x86 (32-bit) or x86_64 (64-bit)
    sudo apt-get install -y ros-humble-behaviortree-cpp
    # Example: Install a package with architecture-specific handling
    if [[ $arch == "x86_64" ]]; then
      echo "Detected architecture: x86_64"
      # Commands to install 64-bit package
    else
      echo "Detected architecture: x86"
      # Commands to install 32-bit package
    fi
    ;;
  armv7l)
    echo "Detected architecture: ARM (32-bit)"
    # Add commands to install ARM 32-bit packages
    ;;
  aarch64)
    echo "Detected architecture: ARM (64-bit)"
    # Add commands to install ARM 64-bit packages
    ;;
  riscv32)
    echo "Detected architecture: RISC-V (32-bit)"
    # Add commands to install RISC-V 32-bit packages
    ;;
  riscv64)
    echo "Detected architecture: RISC-V (64-bit)"
    # Add commands to install RISC-V 64-bit packages
    ;;
  *)
    echo "Unknown architecture: $arch"
    # Add commands for unknown architecture or exit
    exit 1
    ;;
esac
