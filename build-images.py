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
import os
import subprocess


def main():
    # Get the file path of the current script
    file_path = os.path.dirname(os.path.realpath(__file__))
    print("File path: ", file_path)

    # Get the basename of the current scripts parent directory
    parent_dir = os.path.basename(file_path)
    print("Parent dir:", parent_dir)

    try:
        # build base image
        image_dir = "base-image"
        build_script = file_path + "/" + image_dir + "/build-image.py"
        print("Starting: " + build_script)
        subprocess.check_call(["python3", build_script])

        # build dev image with base image
        image_dir = "dev-image"
        build_script = file_path + "/" + image_dir + "/build-image.py"
        print("Starting: " + build_script)
        subprocess.check_call(
            [
                "python3",
                build_script,
                "--build-arg",
                " BASE_IMAGE=" + parent_dir + "-base-image:latest",
            ]
        )

    except subprocess.CalledProcessError:
        print(build_script + " FAILED. Exiting.")
        return

    print("\nAll container image build scripts completed successfully.")


if __name__ == "__main__":
    main()
