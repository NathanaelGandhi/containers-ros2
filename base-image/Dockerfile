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
RUN test "$(find /var/lib/apt/lists/ -maxdepth 1 -type f -mtime -30)" || sudo apt-get update
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
# ENTRYPOINT
## Modify ros_entrypoint to drop to a bash shell if no commands are specified
RUN sed -i.bak -e '/^source/ s|^source \(.*\)|source \1|' -e 's/^exec.*/if [ $# -gt 0 ]; then\n    exec "$@"\nelse\n    exec bash\nfi/' /ros_entrypoint.sh && \
    echo "Original ros_entrypoint.sh >> ros_entrypoint.sh.bk:" && cat /ros_entrypoint.sh.bak && \
    echo "\nModified ros_entrypoint.sh:" && cat /ros_entrypoint.sh
## Set the entry point
ENTRYPOINT ["/ros_entrypoint.sh"]
