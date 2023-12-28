# Ansible Job Monitoring Script

This Python script is designed for monitoring Ansible jobs by interacting with an Ansible API. It allows checking the status of specific jobs or the last job executed from a given template.

## Import Statements

- `argparse`: For parsing command-line arguments.
- `requests`: To make HTTP requests to the Ansible API.
- `sys`: For accessing system-specific parameters and functions.
- `urllib3`: To handle HTTP client and server communications. The script disables SSL warnings, which is common in environments with self-signed certificates.

## Function: `get_last_job_id(api_url, api_token, template_id)`

### Purpose

Retrieves the ID of the last job launched from a specified job template.

### Parameters

- `api_url`: The base URL of the Ansible API.
- `api_token`: Bearer token for API authentication.
- `template_id`: The ID of the Ansible job template.

### Process

1. Constructs the API endpoint URL.
2. Makes a GET request to the API.
3. Parses the response to find the last job ID.
4. Handles potential exceptions and errors.

## Function: `check_ansible_job_status(api_url, api_token, job_id)`

### Purpose

Checks the status of a specified Ansible job.

### Parameters

- `api_url`, `api_token`, `job_id`: Same as above, with `job_id` being the specific job to check.

### Process

1. Constructs the API endpoint URL for the specific job.
2. Makes a GET request and retrieves the job's status.
3. Prints the job status and handles exceptions.

## Main Execution Block

### Command-Line Argument Parsing

Parses arguments for API token (`--token`), job ID (`--jobid`), template ID (`--templateid`), and API URL (`--url`).

### Conditional Logic

- If a job ID is provided, it checks the status of that specific job.
- If a template ID is provided, it finds the last job ID from that template and checks its status.
- If neither is provided, it prompts the user to supply the necessary arguments.

## Usage

1. **Prepare Command-Line Arguments**:
   - Ensure you have the API token, the API URL, and either a job ID or template ID.

2. **Execute the Script**:
   - Run the script with the necessary arguments. For example:
     ```bash
     python script_name.py --token YOUR_API_TOKEN --url YOUR_API_URL --jobid 123
     ```
   - Alternatively, use the template ID to check the last job from that template:
     ```bash
     python script_name.py --token YOUR_API_TOKEN --url YOUR_API_URL --templateid 456
     ```

## Note

The script is designed to exit with different codes based on the execution outcome (success or failure), which is useful in automated workflows to determine the next steps based on the job status.


# Ansible Job Monitoring with Secure Token Handling

This setup includes a Bash wrapper (`wrapper.sh`) and a Go-based encryption/decryption tool (`hasher.go`) for secure Ansible token handling.

## `wrapper.sh`

### Functionality

This script decrypts an encrypted Ansible API token using the `hasher` utility and then runs a Python script for Ansible job monitoring.

### `decrypt_token` Function

- **Purpose**: Decrypts the provided encrypted token using `hasher`.
- **Input**: Encrypted token.
- **Output**: Decrypted token.

### Command-Line Argument Parsing

- Handles arguments for the encrypted token (`-t | --token`), template ID (`-tid | --templateid`), and API URL (`-u | --url`).

### Execution Flow

1. Decrypts the provided token.
2. Runs the Python script `check_job.py` with the decrypted token and other provided arguments.

## `hasher.go`

### Functionality

A Go program for encrypting and decrypting tokens using AES encryption.

### Constants

- `hardcodedSalt`: A predefined salt for encryption and decryption.

### Key Functions

#### `generateKey(salt string)`

- Generates a 32-byte key using the provided salt and `hardcodedSalt`.

#### `encryptToken(token, salt string)`

- Encrypts a token using AES cipher.

#### `decryptToken(encryptedToken string)`

- Decrypts an encrypted token using AES cipher.

### Main Function

- Handles command-line arguments for encryption (`encrypt`) and decryption (`decrypt`) actions.

### Usage

- Encrypt a token: `./hasher encrypt <token>`
- Decrypt a token: `./hasher decrypt <encryptedToken>`

### Note

- The use of a hardcoded salt in production environments is not recommended for security reasons. Consider using a securely stored or dynamically generated salt.
