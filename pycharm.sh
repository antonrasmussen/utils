#!/bin/bash

# https://www.jetbrains.com/help/pycharm/working-with-the-ide-features-from-command-line.html
#
# To run PyCharm from the shell, use the open command with the following options:

  # -a: specify the application.

  # --args: specify additional arguments when passing more than just the file or directory to open.

  # -n: open a new instance of the application even if one is already running.

  # For example, you can run PyCharm.app with the following command:

  # open -na "PyCharm.app"

# You can create a shell script with this command in a directory from your PATH environment variable.
# For example, create the file /usr/local/bin/pycharm with the following contents:

open -na "PyCharm CE.app" --args "$@"

# Make sure you have permissions to execute the script and since /usr/local/bin should be in the
# PATH environment variable by default, you should be able to run pycharm from anywhere in the shell.

