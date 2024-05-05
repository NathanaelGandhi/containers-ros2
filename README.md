# containers-ros2

**What is going on here?**<br>A collection of Dockerfiles/Containerfiles and build scripts for building ROS2 base & development images.

**Why have you made this?**<br>It was fun and solves challenges I faced while developing projects as part of a team. Primarily the *"it works on my machine"* statements, also as a happy accident the *"CI doesn't reflect dev/deploy"* ones.

**What can I do with this?**<br>Whatever you want. It's under an [MIT License](LICENSE)

## Overview:
- [base-image/](base-image)
  - Designed to contain all dependencies that are required to run/build/test your ROS2 project via CI/CD pipelines.
  - Inherits from an official ROS Docker image
  - [Base Image Containerfile](base-image/Containerfile)
  - [Base Image Build Script (python)](base-image/build-image.py)
- [dev-image/](dev-image)
  - Designed to contain all additional dependencies and tools that are useful for developing your ROS2 project.
  - Inherits from ```base-image```
  - [Dev Image Containerfile](base-image/Containerfile)
  - [Dev Image Build Script (python)](base-image/build-image.py)
- [Build Images Script (python)](build-images.py)
  - Designed to call the build scipts of child container images and provide a status print on success/failure
  - Can be called directly in a devcontainer
    - Intended to be added as a submodule in the root devcontainer workspace
      - Example:<br>```"initializeCommand": "./containers-ros2/build-images.py"```
      - See [NathanaelGandhi/devcontainer-ros2](https://github.com/NathanaelGandhi/devcontainer-ros2) for more details

## Notes:
### Your Custom Personalisations
To make custom personalisations just [fork this project](https://github.com/NathanaelGandhi/containers-ros2/fork) and modify it as you wish

### Modifying the git remote
If you cloned this repo (maybe as part of [NathanaelGandhi/devcontainer-ros2](https://github.com/NathanaelGandhi/devcontainer-ros2)) you can update the git remote by:
  - Changing directory to containers-ros2 directory:<br>
  ```cd <YOUR_DEVCONTAINER_DIR>/containers-ros2```
  - Setting a new remote URL:<br>
  ```git remote set-url origin https://github.com/<YOU>/<YOUR_FORK>.git```<br>or<br>```git remote set-url origin git@github.com:<YOU>/<YOUR_FORK>.git```
  - Verifing the new remote URL:<br>
  ```git remote -v```

## base-image
***The base-image can be treated as your projects source-of-truth when it comes to development.<br>We all want to avoid the classic "but it works on my machine" problem.***

The [Base Image Containerfile](base-image/Containerfile) is where you want to be adding all your project dependencies that are required to run/build/test your project via CI/CD pipelines. This gives you a much smaller (and hopefully cheaper/faster) image to be used in runners.

This also has added benefits when you work in a team. You can distribute/maintain a common "standard" config while allowing your colleagues to define their own dev-images on top that contains all their own creature comforts of choice.

## dev-image
***The dev-image is your developer playground. Define a standard development environment, get each developer make their own or throw out all the rules. It can be the wild wild west, the choice is yours.***

The [Dev Image Containerfile](dev-image/Containerfile) is where you want to be adding all your developer luxuries. They make your life easier, but be real, no automated bot ever needs access to any of it. There is also no reason to only have a single dev-image. Copy it, rename it, do whatever.

The [dev-image Build Script](base-image/build-image.py) (also the base-image one, they are the same) has a provision for a ```--name``` arg. Just populate this when you are modifying the [Build All Your Images Script](build-images.py) and the build process will spit out separate images for each. This arg (and all the others) can also just be passed directly to an images own build script. There is freedom here to work it how you like, and if you don't, just modify it!

## Final remarks
I made this project to solve some of challenges I face when developing a ROS2 project as part of a team, so expect this space to slowly evolve over time as my needs require. I'm always happy to hear suggestions and receive feedback, but if something is really not to your liking or is a custom personalisation we don't see eye-to-eye on, just remember you are free to  [fork this project](https://github.com/NathanaelGandhi/containers-ros2/fork) and modify it as you wish.
