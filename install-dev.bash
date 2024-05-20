#! /bin/bash

################################################################################
# DEVELOPER TOOLING. DEPS FOR HARDWARE/RUNNERS SHOULD BE INSTALLED BY CORE     #
################################################################################

################################################################################
# APT
## Note: Architecture agnostic
## Only update if the apt cache is older than 30 days
test "$(find /var/lib/apt/lists/ -maxdepth 1 -type f -mtime -30)" || apt-get update
## Install packages: core utils
### editors: vim, nano
### utils-core: git ...
## Install packages: nice to have
### utils: tree ...
### graphical-git: gitg ...
### ros: ...
sudo apt-get install -y \
    vim nano \
    git ssh curl \
    tree file htop direnv \
    gitg gitk \
    ros-${ROS_DISTRO}-rqt*

################################################################################
# PIP
## Note: Architecture agnostic
## clang-format from apt is very old (~v14) vs pip v18+
pip install \
    pdm \
    pre-commit

################################################################################
# Extend bash shell
## Oh-My-Bash extensions
if [ -d ~/.oh-my-bash ]; then \
    echo "Directory ~/.oh-my-bash already exists. Not installing"; \
else \
    echo "Downloading oh-my-bash" && \
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)" --unattended && \
    sed -i 's/OSH_THEME="font"/OSH_THEME="roderik"/g' ~/.bashrc && \
    if [ $? -eq 0 ]; then \
        echo "Oh My Bash installed and theme modified"; \
    fi; \
fi

## Hook direnv
if ! grep -q 'eval "$(direnv hook bash)"' ~/.bashrc; then \
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc; \
fi

################################################################################
# Architecture specific installs
## Detect architecture
arch=$(uname -m)
## Determine the appropriate installation package or binary
case $arch in
  x86_64|i386|i686)
    echo "Detected architecture: x86 or x86_64"
    # Add commands to install packages for x86 (32-bit) or x86_64 (64-bit)
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
