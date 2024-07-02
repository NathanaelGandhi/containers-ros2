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

    # Get the basename of the current scripts grandparent directory
    grandparent_dir = os.path.basename(os.path.dirname(file_path))
    logging.debug(f"Grandparent dir: {grandparent_dir}")

    # Create an ArgumentParser object.
    # This object will hold all the information necessary to parse the command-line arguments into Python data types.
    parser = argparse.ArgumentParser(
        description="base image builder for ROS2",
        epilog="PDM is the preferred Python package management tool for this project",
    )

    # Add arguments to the parser using the add_argument() method.
    # Each argument typically consists of a flag (e.g., -f or --foo), a help string, and other optional parameters.
    parser.add_argument(
        "--build-arg",
        action="append",
        help="Set build-time variables: stringArray",
        metavar="<key>=<value>",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Name of the Dockerfile",
        default="Dockerfile",
        metavar="<DOCKERFILE>",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name for the image",
        default=grandparent_dir + "-" + parent_dir,
        metavar="<IMAGE_NAME>",
    )
    parser.add_argument(
        "--no-cache",
        help="Do not use cache when building the image",
        action="store_true",
    )
    parser.add_argument(
        "--platform",
        help="Set platform if server is multi-platform (eg. linux/amd64,linux/arm64/v8)",
        metavar="<PLATFORM>[,<PLATFORM>][...]",
    )
    parser.add_argument(
        "--progress",
        help="Set build progress output",
        default="auto",
        metavar="<OUTPUT_MODE>",
    )
    parser.add_argument(
        "-t", "--tag", help="Tag for the image", default="latest", metavar="<IMAGE_TAG>"
    )

    # Call the parse_args() method to parse the command-line arguments.
    # This method returns an object containing the values of the parsed arguments.
    args = parser.parse_args()
    logging.debug(f"Args: {args}")

    # Set build options
    # Note: access the values of the parsed arguments using dot notation on the args object.
    if args.build_arg:
        for build_arg in args.build_arg:
            build_options += f"--build-arg {build_arg} "
    if args.no_cache:
        build_options += "--no-cache "
    if args.progress:
        build_options += f"--progress={args.progress} "
    build_options += f"-f {file_path}/{args.file} "
    logging.debug(f"Build options: {build_options}")

    # run_command("docker buildx create --use --driver docker-container --platform linux/amd64,linux/arm64/v8 builder")

    # build image(s)
    if args.platform:
        platform_list = args.platform.split(",")
        # loop over all platforms and build
        for platform in platform_list:
            image_name = f"{args.name}/{platform}"
            images_built += f"\n{image_name}"
            image_build_options = build_options
            image_build_options += f"--platform={platform} "
            image_build_options += f"-t {image_name}:{args.tag}"
            run_command(f"docker build --load {image_build_options} {file_path}")
    else:
        image_name = f"{args.name}"
        images_built += f"\n{image_name}"
        image_build_options = build_options
        image_build_options += f"-t {image_name}:{args.tag}"
        run_command(f"docker build --load {image_build_options} {file_path}")

    # run_command("docker context rm builder")

    logging.info(f"Finished building:{images_built}")
    print("")


if __name__ == "__main__":
    main()
