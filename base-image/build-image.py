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
import sys


def main():
    # SETUP
    build_options = ""
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

    # Create an ArgumentParser object. This object will hold all the information necessary to parse the command-line arguments into Python data types.
    parser = argparse.ArgumentParser(
        description="base image builder for ROS2",
        epilog="PDM is the preferred Python package management tool for this project",
    )

    # Add arguments to the parser using the add_argument() method. Each argument typically consists of a flag (e.g., -f or --foo), a help string, and other optional parameters.
    parser.add_argument(
        "--build-arg",
        help="Set build-time variables: stringArray",
        metavar="<key>=<value>",
    )
    parser.add_argument(
        "--builder",
        help="Building application (docker/podman)",
        default="docker",
        metavar="<APP>",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Name of the Containerfile",
        default="Containerfile",
        metavar="<CONTAINERFILE>",
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
        "-t", "--tag", help="Tag for the image", default="latest", metavar="<IMAGE_TAG>"
    )

    # Call the parse_args() method to parse the command-line arguments. This method returns an object containing the values of the parsed arguments.
    args = parser.parse_args()
    logging.debug(f"Args: {args}")

    # Set build options
    # Note: access the values of the parsed arguments using dot notation on the args object.
    if args.build_arg:
        build_options += f"--build-arg {args.build_arg} "
    build_options += f"-t {args.name}:{args.tag} "
    build_options += f"-f {file_path}/{args.file} "
    if args.no_cache:
        build_options += "--no-cache "
    logging.debug(f"Build options:{build_options}")

    # build image
    build_string = f"{args.builder} build {build_options} {file_path}"
    logging.info(f"{build_string}")
    try:
        return_code = os.system(build_string)
        if return_code != 0:
            raise RuntimeError(
                f"'{build_string}' returned non-zero exit status: {return_code}"
            )
    except RuntimeError as e:
        logging.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
