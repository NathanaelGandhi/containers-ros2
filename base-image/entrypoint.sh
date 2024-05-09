#!/bin/bash

################################################################################
# NOTE:                                                                        #
#   You can use any combination of:                                            #
#       --uid, --gid, --uname, or --user uid:gid:username                      #
#   If any parameter is not provided, you will be prompted to enter it         # 
################################################################################

# Default values
USER_UID=""
USER_GID=""
USER_NAME=""

# Check if the script is being run as root.
# If the script is not being run as root, the exec command is used to replace 
# the current process with a new process running the same script ("$0") and 
# passing along any command line arguments ("$@") to it. The sudo command is 
# used to elevate the script's privileges to root
if [[ $EUID -ne 0 ]]; then
    echo "Elevating script privileges to sudo"
    exec sudo "$0" "$@"
fi

# Function to check if a variable is empty
is_empty() {
    [[ -z $1 ]]
}

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        --uid)
            USER_UID="$2"
            shift 2 # shift twice to consume both the option and its argument
            ;;
        --gid)
            USER_GID="$2"
            shift 2 # shift twice to consume both the option and its argument
            ;;
        --uname)
            USER_NAME="$2"
            shift 2 # shift twice to consume both the option and its argument
            ;;
        --user)
            USER_INFO="$2"
            IFS=':' read -r -a user_info <<< "$USER_INFO"
            USER_UID="${user_info[0]}"
            USER_GID="${user_info[1]}"
            USER_NAME="${user_info[2]}"
            shift 2 # shift twice to consume both the option and its argument
            ;;
        *)    # unknown option
            shift # move to the next argument
            ;;
    esac
done

# Prompt for user input if any required information is missing
if is_empty "$USER_UID"; then
    read -p "Enter UID: " USER_UID
fi

if is_empty "$USER_GID"; then
    read -p "Enter GID: " USER_GID
fi

if is_empty "$USER_NAME"; then
    read -p "Enter username: " USER_NAME
fi

# Check if all required variables are set
if is_empty "$USER_UID" || is_empty "$USER_GID" || is_empty "$USER_NAME"; then
    echo "Error: User information not provided or incomplete." >&2
    exit 1
fi

# Check if the user already exists
if id "$USER_NAME" &>/dev/null; then
    echo "Error: User '$USER_NAME' already exists." >&2
    exit 1
fi

# Create a new group with specified GID and name
if ! groupadd --gid "$USER_GID" "$USER_NAME"; then
    echo "Error: Failed to create group '$USER_NAME'." >&2
    exit 1
fi

# Add a new user with specified UID, GID, and name
if ! useradd --shell /bin/bash --uid "$USER_UID" --gid "$USER_GID" -m "$USER_NAME"; then
    echo "Error: Failed to create user '$USER_NAME'." >&2
    exit 1
fi

# Grant sudo privileges to the user
if ! echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/$USER_NAME"; then
    echo "Error: Failed to grant sudo privileges to '$USER_NAME'." >&2
    exit 1
fi

# Set appropriate permissions for the sudoers file
chmod 0440 "/etc/sudoers.d/$USER_NAME"

echo "User '$USER_NAME' created successfully."

# Switch to the new user's shell
su - "$USER_NAME"
