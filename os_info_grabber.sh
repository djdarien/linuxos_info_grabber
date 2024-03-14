#!/bin/bash

# Input file containing server hostnames
input_file="/Users/dentwistle/server_hostnames.txt"

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file '$input_file' not found."
    exit 1
fi

# Output file
output_file="os_info.csv"

# Write CSV header
echo "Hostname,OS Info" > "$output_file"

# Function to connect to server and retrieve OS information
connect_and_get_os_info() {
    server=$1
    echo "Connecting to $server ..."
    os_info=$(ssh -o StrictHostKeyChecking=no "$server" '
        if [ -f /etc/redhat-release ]; then
            echo "$(cat /etc/redhat-release),$(uname -a)"
        elif [ -f /etc/os-release ]; then
            source /etc/os-release
            echo "$PRETTY_NAME,$(uname -a)"
        else
            echo "Unknown OS, $(uname -a)"
        fi
    ')
    echo "Retrieved OS info from $server"
    echo "$server,$os_info" >> "$output_file"
    echo "Disconnected from $server"
}

# Iterate through each server in the input file
while IFS= read -r server || [ -n "$server" ]; do
    # Connect to server, retrieve OS information, and write to CSV
    connect_and_get_os_info "$server"
done < "$input_file"

echo "OS info extracted and saved to $output_file"
