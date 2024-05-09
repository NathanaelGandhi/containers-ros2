# containers-ros2
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/NathanaelGandhi/containers-ros2/main.svg)](https://results.pre-commit.ci/latest/github/NathanaelGandhi/containers-ros2/main)
[![Release Drafter](https://github.com/NathanaelGandhi/containers-ros2/actions/workflows/release-drafter.yml/badge.svg?branch=release)](https://github.com/NathanaelGandhi/containers-ros2/actions/workflows/release-drafter.yml)
[![Mirror release to humble](https://github.com/NathanaelGandhi/containers-ros2/actions/workflows/mirror-release-to-humble.yaml/badge.svg?branch=release)](https://github.com/NathanaelGandhi/containers-ros2/actions/workflows/mirror-release-to-humble.yaml)

**What is going on here?**<br>A collection of container images for ROS2 development, testing and deployment.

**Why have you made this?**<br>It was fun and solves challenges I faced while developing projects as part of a team. Primarily the *"it works on my machine"* statements, also as a happy accident the *"CI doesn't reflect dev/deploy"* ones.

**What can I do with this?**<br>Whatever you want. It's under an [MIT License](LICENSE).

## Requirements:
- python3
- Docker (Docker-Desktop if you want to build arm images)

## Overview:
- [base-image/](base-image)
  - Designed to contain all dependencies that are required to run/build/test your ROS2 project. Can be used for multi-arch builds or via CI/CD pipelines.
  - Inherits from an official ROS Docker image
  - Supports multi-architecture (multi-platform) images
    - ros:humble only supports ```"linux/amd64,linux/arm64/v8"```
  - [Base Image Dockerfile](base-image/Dockerfile)
  - [Base Image Build Script (python)](base-image/build-image.py)
- [dev-image/](dev-image)
  - Designed to contain all additional dependencies and tools that are useful for developing your ROS2 project.
  - Inherits from ```base-image```
  - Supports multi-architecture (multi-platform) images
  - [Dev Image Dockerfile](base-image/Dockerfile)
  - [Dev Image Build Script (python)](base-image/build-image.py)
- [Build Images Script (python)](build-images.py)
  - Designed to call the build scipts of child container images and provide a status print on success/failure
  - Supports multi-architecture (multi-platform) images
    - Limited to the architectures of inherited images. Example: ros:humble only supports ```"linux/amd64,linux/arm64/v8"```

## Notes:
### Your Custom Personalisations
To make custom personalisations just [fork this project](https://github.com/NathanaelGandhi/containers-ros2/fork) and modify it as you wish

### Modifying the git remote
If you cloned this repo you can update the git remote by:
  - Changing directory to containers-ros2 directory:<br>
  ```cd <YOUR_PATH>/containers-ros2```
  - Setting a new remote URL:<br>
  ```git remote set-url origin https://github.com/<YOU>/<YOUR_FORK>.git```<br>or<br>```git remote set-url origin git@github.com:<YOU>/<YOUR_FORK>.git```
  - Verifying the new remote URL:<br>
  ```git remote -v```

### Non-root container user
This is currently unsupported as the there are permission issues when using a non-root user and mounting host directories in the container, even after mapping the username, uid & gid to that of the host. By disabling this you can mount directories into the container and operate on them (example calling ```colcon build```) without changing ownership (that would affect the host) or by prefixing all your commands with sudo. I'm sure there is a more elegant solution to this problem, I'm all ears.

### Running a container in a terminal
The following command will start an interactive container, mount your current dir at ```/mnt/host``` and remove it on exit. Modify this command to suit your own image naming/flags if needed.
```
docker run --rm -it -v $(pwd):/mnt/host containers-ros2-dev-image/linux/amd64
```

### Running a container in the background
The following command will start an interactive container in the background, mount your current dir at ```/mnt/host``` and name the container. You will need to call ```docker stop <name>``` to stop it. Modify this command to suit your own image naming/flags if needed.
```
docker run -d -it -v $(pwd):/mnt/host --name containers-ros2-dev-image-amd64 containers-ros2-dev-image/linux/amd64
```

### Having to run a container daily
Your docker run command is probably a good candidate for a shell alias or direnv.

### Attaching VSCode to a running container
RTFM: [code.visualstudio.com/docs/devcontainers/attach-container](https://code.visualstudio.com/docs/devcontainers/attach-container).

## build-images
***The [build-images.py](build-images.py) script is your helper to configure and build one-to-many images. All the supported flags can be passed to the underlying container build-image scripts.***

Note: Pushing directly to a registry is currently unsupported (see Issue: #18).

## base-image
***The base-image can be treated as your projects source-of-truth when it comes to development.<br>We all want to avoid the classic "but it works on my machine" problem.***

The [Base Image Dockerfile](base-image/Dockerfile) is where you want to be adding all your project dependencies that are required to run/build/test your project via CI/CD pipelines. This gives you a much smaller (and hopefully cheaper/faster) image to be used in runners.

This also has added benefits when you work in a team. You can distribute/maintain a common "standard" config while allowing your colleagues to define their own dev-images on top that contains all their own creature comforts of choice.

## dev-image
***The dev-image is your developer playground. Define a standard development environment, get each developer make their own or throw out all the rules. It can be the wild wild west, the choice is yours.***

The [Dev Image Dockerfile](dev-image/Dockerfile) is where you want to be adding all your developer luxuries. They make your life easier, but be real, no automated bot ever needs access to any of it. There is also no reason to only have a single dev-image. Copy it, rename it, do whatever.

The [dev-image Build Script](base-image/build-image.py) (also the base-image one, they are the same) has a provision for a ```--name``` arg. Just populate this when you are modifying the [Build All Your Images Script](build-images.py) and the build process will spit out separate images for each. This arg (and all the others) can also just be passed directly to an images own build script. There is freedom here to work it how you like, and if you don't, just modify it!

## Final remarks
I made this project to solve some of challenges I face when developing a ROS2 project as part of a team, so expect this space to slowly evolve over time as my needs require. I'm always happy to hear suggestions and receive feedback, but if something is really not to your liking or is a custom personalisation we don't see eye-to-eye on, just remember you are free to  [fork this project](https://github.com/NathanaelGandhi/containers-ros2/fork) and modify it as you wish.
