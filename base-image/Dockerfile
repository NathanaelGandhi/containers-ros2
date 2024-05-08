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

ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}
ENV ROS_DISTRO=${ROS_DISTRO}
LABEL ROS_DISTRO=${ROS_DISTRO}

# Note: TARGETPLATFORM is set by Docker BuildKit
ARG TARGETPLATFORMdoc
LABEL TARGETPLATFORM=${TARGETPLATFORM}
# Note: You should guard platform specific instructions with TARGETPLATFORM
RUN if [ "${TARGETPLATFORM}" = "linux/amd64" ] ; then \
        echo "Running on linux/amd64"; \
    elif [ "${TARGETPLATFORM}" = "linux/arm64/v8" ] ; then \
        echo "Running on linux/arm64/v8"; \
    elif [ "${TARGETPLATFORM}" = "linux/arm/v7" ] ; then \
        echo "Running on linux/arm/v7"; \
    fi
    
################################################################################
# Ensures there is a non-root user
ARG USERNAME=builder
ARG USER_UID=1000
ARG USER_GID=$USER_UID

## Create the user
RUN if [ "$(id -un)" != "$USERNAME" ] ; then \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --shell /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME; \
    fi
USER $USERNAME

################################################################################
# APT
## Check if the apt cache is older than 30 days
RUN test "$(find /var/lib/apt/lists/ -maxdepth 0 -mtime -30)" || sudo apt-get update
## Install packages
### python3-pip required by ros2
### tools to build from source
### more...
RUN sudo apt-get install -y \
    python3-pip \
    git cmake build-essential

################################################################################
# PIP
## Install packages
# RUN pip install \

################################################################################
# Create directories for filesystem mapping
## Could be mounted as non-volatile memory
RUN sudo mkdir -p /mnt/storage
## Could be mounted as volatile memory
RUN sudo mkdir -p /mnt/ram && \
    sudo mkdir -p /tmp/ram && \
    sudo ln -s /tmp/ram /mnt/ram

################################################################################
# Dependencies that need to be installed for CI/CD pipelines
## ros2: ros-$ROS_DISTRO-*
## note: use individual RUN commands to allow for caching
# RUN apt-get install -y ros-humble-behaviortree-cpp

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
ENTRYPOINT ["/bin/bash"]
