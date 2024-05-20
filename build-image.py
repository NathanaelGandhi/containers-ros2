#!/usr/bin/env python3
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
import argparse
import logging
import os


def run_command(command_string):
    logging.info(f"{command_string}")
    try:
        return_code = os.system(command_string)
        if return_code != 0:
            raise RuntimeError(
                f"'{command_string}' returned non-zero exit status: {return_code}"
            )
    except RuntimeError as e:
        logging.error(e)


def main():
    # SETUP
    build_options = ""  # string list of build args
    platform_list = []  # list of platforms to be populated in multi-platform cases
    images_built = ""  # list of images built for logging
    logging.basicConfig(level=logging.INFO)

    # Get the file path of the current script
    file_path = os.path.dirname(os.path.realpath(__file__))
    logging.debug(f"File path: {file_path}")

    # Get the basename of the current scripts parent directory
    parent_dir = os.path.basename(file_path)
    logging.debug(f"Parent dir: {parent_dir}")

    # Create an ArgumentParser object.
    # This object will hold all the information necessary to parse the command-line arguments into Python data types.
    parser = argparse.ArgumentParser(
        description="base image builder for ROS2",
        epilog="PDM is the preferred Python package management tool for this project",
    )

    # Add arguments to the parser using the add_argument() method.
    # Each argument typically consists of a flag (e.g., -f or --foo), a help string, and other optional parameters.
    parser.add_argument(
        "-f",
        "--file",
        help="Name of the Dockerfile",
        default="Dockerfile",
        metavar="<DOCKERFILE>",
    )
    parser.add_argument(
        "--platform",
        help="Set platform if server is multi-platform (eg. linux/amd64,linux/arm64/v8)",
        metavar="<PLATFORM[,<PLATFORM>][...]>",
    )
    parser.add_argument(
        "--target",
        help="Set the target build stage to build. Default is dev",
        default="dev",
        metavar="<TARGET>",
    )
    parser.add_argument(
        "-t", "--tag", 
        help="Name and optionally a tag in the name:tag format", 
        default=f"{parent_dir}:latest",
        metavar="<NAME[:TAG]>",
    )

    # Call the parse_known_args() method to parse the command-line arguments.
    # This method returns objects containing the values of the parsed arguments.
    args, unhandled_args = parser.parse_known_args()
    logging.debug(f"Args: {args}")
    logging.debug(f"Unhandled args: {unhandled_args}")

    # Set build options
    # Note: access the values of the parsed arguments using dot notation on the args object.
    build_options += f"-f {file_path}/{args.file} "
    build_options += f"--target {args.target} "

    logging.debug(f"Build options: {build_options}")

    # run_command("docker buildx create --use --driver docker-container --platform linux/amd64,linux/arm64/v8 builder")

    # handle optional tag element
    if ':' not in args.tag:
        args.tag = f"{args.tag}:latest"

    # insert target into tag
    # split the string at the first occurrence of ':'
    parts = args.tag.split(':', 1)
    # insert the substring before the ':'
    new_tag = f"{parts[0]}-{args.target}:{parts[1]}"

    # build image(s) - depends on number of platform(s)    
    if args.platform:
        platform_list = args.platform.split(",")
        # loop over all platforms and build
        for platform in platform_list:
            # insert platform into tag
            parts = args.tag.split(':', 1)
            new_tag = f"{parts[0]}-{platform}:{parts[1]}"
            # set final build options
            image_build_options = f"-t {new_tag} "
            image_build_options += f"--platform={platform} "
            image_build_options += build_options
            run_command(f"docker build {image_build_options} {file_path}")
            images_built += f"\n{new_tag}"
    else:
        # set final build options
        image_build_options = f"-t {args.tag} "
        image_build_options += build_options
        run_command(f"docker build {image_build_options} {file_path}")
        images_built += f"\n{args.tag}"

    # run_command("docker context rm builder")

    logging.info(f"Finished building:{images_built}")
    print("")


if __name__ == "__main__":
    main()
