#!/bin/bash

# Function to decrypt the token using hasher and extract the decrypted token
decrypt_token() {
    encrypted_token=$1
    decrypted_token=$(./hasher decrypt "$encrypted_token" | grep -o 'Decrypted Token: .*' | cut -d ' ' -f 3-)
    echo "$decrypted_token"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
    -t | --token)
        encrypted_token="$2"
        shift
        shift
        ;;
    -tid | --templateid)
        template_id="$2"
        shift
        shift
        ;;
    -u | --url)
        api_url="$2"
        shift
        shift
        ;;
    *)
        echo "Unknown option: $key"
        exit 1
        ;;
    esac
done

# Decrypt the token if provided
if [ -n "$encrypted_token" ]; then
    decrypted_token=$(decrypt_token "$encrypted_token")
    # Run the Python script with the decrypted token and other arguments
    python3 hashed.py -t "$decrypted_token" -tid "$template_id" -u "$api_url"
else
    echo "No encrypted token provided."
fi
