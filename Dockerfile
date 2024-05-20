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

ARG INSTALL_DEV_TOOLS=true

ARG ROS_DISTRO=humble
ARG ROS_IMAGE=ros
FROM ${ROS_IMAGE}:${ROS_DISTRO} AS base
LABEL ROS_IMAGE=${ROS_IMAGE}
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

ARG USERNAME=USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
ENV SHELL /bin/bash
## Set the user
USER $USERNAME

################################################################################
# CORE - Note: Install all deps via this script. Enables reproduceable target 
# hardware setups
FROM base AS core
## Copy script into the container
COPY install-core.bash /var/tmp/install-core.bash
## Set script to executable, run and log
RUN sudo chmod +x /var/tmp/install-core.bash && \
    /var/tmp/install-core.bash 2>&1 | sudo tee /var/log/install-core.log

################################################################################
# DEV - Note: Dev tooling that will not be deployed to target hardware / CI
FROM core AS dev
## Copy script into the container
COPY install-dev.bash /var/tmp/install-dev.bash
## Guard on INSTALL_DEV_TOOLS ARG, set script to executable, run and log
RUN if $INSTALL_DEV_TOOLS; then \
        sudo chmod +x /var/tmp/install-dev.bash && \
        /var/tmp/install-dev.bash 2>&1 | sudo tee /var/log/install-dev.log; \
    fi

################################################################################
# ENTRYPOINT
## Modify ros_entrypoint to drop to a bash shell if no commands are specified
USER root
RUN sed -i.bak -e '/^source/ s|^source \(.*\)|source \1|' -e 's/^exec.*/if [ $# -gt 0 ]; then\n    exec "$@"\nelse\n    exec bash\nfi/' /ros_entrypoint.sh && \
    echo "Original ros_entrypoint.sh >> ros_entrypoint.sh.bk:" && cat /ros_entrypoint.sh.bak && \
    echo "\nModified ros_entrypoint.sh:" && cat /ros_entrypoint.sh
USER $USERNAME
## Set the entry point
ENTRYPOINT ["/ros_entrypoint.sh"]
