import subprocess

# Input file containing server hostnames
input_file = "/Users/dentwistle/server_hostnames.txt"

# Check if the input file exists
try:
    with open(input_file, "r") as f:
        servers = f.readlines()
except FileNotFoundError:
    print(f"Input file '{input_file}' not found.")
    exit(1)

# Output file
output_file = "os_info.csv"

# Function to connect to server and retrieve OS information
def connect_and_get_os_info(server):
    print(f"Connecting to {server.strip()} ...")
    try:
        os_info = subprocess.check_output(
            f"ssh -o StrictHostKeyChecking=no {server.strip()} 'if [ -f /etc/redhat-release ]; then cat /etc/redhat-release && uname -a; elif [ -f /etc/os-release ]; then source /etc/os-release && echo $PRETTY_NAME && uname -a; else echo \"Unknown OS\" && uname -a; fi'",
            shell=True,
            universal_newlines=True
        )
        print(f"Retrieved OS info from {server.strip()}")
        with open(output_file, "a") as f:
            f.write(f"{server.strip()}, {os_info}\n")
        print(f"Disconnected from {server.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {server.strip()}: {e}")

# Iterate through each server in the input file
with open(output_file, "w") as f:
    f.write("Hostname,OS Info\n")  # Write CSV header

for server in servers:
    connect_and_get_os_info(server)

print(f"OS info extracted and saved to {output_file}")
