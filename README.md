# Ansible Job Monitoring Script

This Python script is designed for monitoring Ansible jobs by interacting with an Ansible API. It allows checking the status of specific jobs, the last job executed from a given template, or jobs listed in a file.

## Import Statements

- `argparse`: For parsing command-line arguments.
- `requests`: To make HTTP requests to the Ansible API.
- `sys`: For accessing system-specific parameters and functions.
- `urllib3`: To handle HTTP client and server communications. The script disables SSL warnings, which is common in environments with self-signed certificates.

## Function: `get_most_recent_job_id(api_url, api_token, template_id)`

### Purpose

Retrieves the ID of the most recent job launched from a specified job template.

### Parameters

- `api_url`: The base URL of the Ansible API.
- `api_token`: Bearer token for API authentication.
- `template_id`: The ID of the Ansible job template.

### Process

1. Constructs the API endpoint URL.
2. Makes a GET request to the API.
3. Parses the response to find the most recent job ID.
4. Handles potential exceptions and errors.

## Function: `check_ansible_job_status(api_url, api_token, job_id)`

### Purpose

Checks the status of a specified Ansible job.

### Parameters

- `api_url`: The base URL of the Ansible API.
- `api_token`: Bearer token for API authentication.
- `job_id`: The ID of the specific job to check.

### Process

1. Constructs the API endpoint URL for the specific job.
2. Makes a GET request and retrieves the job's status.
3. Returns the job status and handles exceptions.

## Function: `check_jobs_from_file(api_url, api_token, file_path)`

### Purpose

Checks the statuses of the most recent jobs from a list of job template IDs provided in a file.

### Parameters

- `api_url`: The base URL of the Ansible API.
- `api_token`: Bearer token for API authentication.
- `file_path`: Path to the file containing the list of template IDs.

### Process

1. Reads the template IDs from the file.
2. For each template ID, retrieves the most recent job ID and checks its status.
3. Collects failed jobs and handles errors.
4. Returns appropriate exit codes based on the job statuses.

## Main Execution Block

### Command-Line Argument Parsing

Parses arguments for API token (`--token`), job ID (`--jobid`), template ID (`--templateid`), API URL (`--url`), and a file containing template IDs (`--file`).

### Conditional Logic

- If a job ID is provided, it checks the status of that specific job.
- If a template ID is provided, it finds the most recent job ID from that template and checks its status.
- If a file is provided, it checks the statuses of the most recent jobs from the template IDs listed in the file.
- If none of these are provided, it prompts the user to supply the necessary arguments.

## Usage

1. **Prepare Command-Line Arguments**:
   - Ensure you have the API token, the API URL, and either a job ID, template ID, or a file containing template IDs.

2. **Execute the Script**:
   - To check a specific job:
     ```bash
     python script_name.py --token YOUR_API_TOKEN --url YOUR_API_URL --jobid 123
     ```
   - To check the most recent job from a template:
     ```bash
     python script_name.py --token YOUR_API_TOKEN --url YOUR_API_URL --templateid 456
     ```
   - To check jobs from a list of templates:
     ```bash
     python script_name.py --token YOUR_API_TOKEN --url YOUR_API_URL --file path/to/template_ids.txt
     ```

## Note

The script is designed to exit with different codes based on the execution outcome (success or failure), which is useful in automated workflows to determine the next steps based on the job status.

# Ansible Job Monitoring with Secure Token Handling

This setup includes a Bash wrapper (`wrapper.sh`) and a Go-based encryption/decryption tool (`hasher.go`) for secure Ansible token handling.

## `wrapper.sh`

### Functionality

This script decrypts an encrypted Ansible API token using the `hasher` utility and then runs the Python script for Ansible job monitoring.

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

- Encrypt a token:
  ```bash
  ./hasher encrypt <token>
  ```
- Decrypt a token:
```bash
./hasher decrypt <encryptedToken>
```  
