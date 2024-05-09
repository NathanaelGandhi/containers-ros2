# MIT License
#
# Copyright (c) 2024 Nathanael Gandhi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

ARG BASE_IMAGE
# ARG BASE_IMAGE=containers-ros2-base-image:latest
FROM ${BASE_IMAGE}
# Note: ENV ROS_DISTRO is set in BASE_IMAGE
LABEL ROS_DISTRO=${ROS_DISTRO}

# Note: TARGETPLATFORM is set by Docker BuildKit
ARG TARGETPLATFORM
LABEL TARGETPLATFORM=${TARGETPLATFORM}
# Note: You should guard platform specific instructions with TARGETPLATFORM
RUN if [ "${TARGETPLATFORM}" = "linux/amd64" ] ; then \
        echo "Running as linux/amd64"; \
    elif [ "${TARGETPLATFORM}" = "linux/arm64/v8" ] ; then \
        echo "Running as linux/arm64/v8"; \
    elif [ "${TARGETPLATFORM}" = "linux/arm/v7" ] ; then \
        echo "Running as linux/arm/v7"; \
    fi

################################################################################
# Ensures there is a non-root user
# NOTE: Removed for now. There are permission issues when using a non-root user
#   and mounting host directories in the container, even after mapping the
#   username, uid & gid.

# ARG USER_NAME=builder
# ARG USER_ID=2000
# ARG GROUP_ID=$USER_ID
# RUN echo "USER_NAME=${USER_NAME} USER_ID=${USER_ID} GROUP_ID=${GROUP_ID}"

# ## Create the user
# RUN if [ "$(id -un)" != "$USER_NAME" ] ; then \
#         groupadd --gid $GROUP_ID $USER_NAME && \
#         useradd --shell /bin/bash --uid $USER_ID --gid $GROUP_ID -m $USER_NAME && \
#         echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME && \
#         chmod 0440 /etc/sudoers.d/$USER_NAME; \
#     fi
# USER $USER_NAME

################################################################################
# APT
## Only update if the apt cache is older than 30 days
RUN test "$(find /var/lib/apt/lists/ -maxdepth 1 -type f -mtime -30)" || apt-get update
## Install packages: core utils
### editors: vim, nano
### utils-core: git ...
### utils-n2h: tree ...
RUN sudo apt-get install -y \
    vim nano \
    git ssh curl \
    tree file htop direnv

################################################################################
# Ensures extended bash shell
## Oh-My-Bash extensions
RUN if [ -d ~/.oh-my-bash ]; then \
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
RUN if ! grep -q 'eval "$(direnv hook bash)"' ~/.bashrc; then \
    echo 'eval "$(direnv hook bash)"' >> ~/.bashrc; \
fi

################################################################################
# DEVELOPER SOFTWARE - Add new additions below
################################################################################
# PIP
## Install packages
### clang-format from apt is very old (~v14) vs pip v18+
### pdm for python project management
### pre-commit for git hooks
RUN pip install \
    clang-format \
    pdm \
    pre-commit

################################################################################
# APT
## Only update if the apt cache is older than 30 days
RUN test "$(find /var/lib/apt/lists/ -maxdepth 1 -type f -mtime -30)" || apt-get update
## Install general packages
### gitg and gitk for graphical git
RUN sudo apt-get install -y \
    gitg gitk
## Install ros apt packages: ros-${ROS_DISTRO}-*
## note: use individual RUN commands to allow for caching
### rqt and its plugins
# RUN sudo apt-get install -y ros-${ROS_DISTRO}-rqt-common-plugins
# RUN sudo apt-get install -y ros-${ROS_DISTRO}-rqt*
### rviz2
# RUN sudo apt-get install -y ros-${ROS_DISTRO}-rviz2
### gazebo & ros_gz
# RUN sudo apt-get install -y ros-${ROS_DISTRO}-ros-gz

################################################################################
# INSTALL FROM SOURCE
## Install EXAMPLE from source
# WORKDIR /opt
### Clone the repository
# RUN git clone -b v2.1.0 https://github.com/EXAMPLE/example.git
### Create build directory
# RUN mkdir -p /opt/example/build
### Change working directory to build
# WORKDIR /opt/example/build
### Run cmake
# RUN cmake ..
### Run make and install
# RUN make install

################################################################################
# ENTRYPOINT
## Modify ros_entrypoint to drop to a bash shell if no commands are specified
RUN sed -i.bak -e '/^source/ s|^source \(.*\)|source \1|' -e 's/^exec.*/if [ $# -gt 0 ]; then\n    exec "$@"\nelse\n    exec bash\nfi/' /ros_entrypoint.sh && \
    echo "Original ros_entrypoint.sh >> ros_entrypoint.sh.bk:" && cat /ros_entrypoint.sh.bak && \
    echo "\nModified ros_entrypoint.sh:" && cat /ros_entrypoint.sh
## Set the entry point
ENTRYPOINT ["/ros_entrypoint.sh"]
