import argparse
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_last_job_id(api_url, api_token, template_id):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    api_endpoint = f"{api_url}/api/v2/job_templates/{template_id}/jobs/"
    
    try:
        response = requests.get(api_endpoint, headers=headers, verify=False)
        response.raise_for_status()
        launches = response.json().get("results", [])
        if launches:
            last_job_id = launches[-1]["id"]
            return last_job_id
        else:
            print("No jobs found for the specified template.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve job launches. Error: {e}")
        sys.exit(1)

def check_ansible_job_status(api_url, api_token, job_id):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    api_endpoint = f"{api_url}/api/v2/jobs/{job_id}/"
    
    try:
        response = requests.get(api_endpoint, headers=headers, verify=False)
        response.raise_for_status()
        job_details = response.json()
        job_status = job_details.get("status", "Unknown")
        print(f"Job ID: {job_id}, Status: {job_status}")

        if job_status != "successful":
            sys.exit(1)  # Exit with code 1 if the job status is not "successful"
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve job status. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Ansible job status through API.")
    parser.add_argument("-t", "--token", type=str, required=True, help="API Token")
    parser.add_argument("-i", "--jobid", type=int, help="Ansible Job ID")
    parser.add_argument("-tid", "--templateid", type=int, help="Ansible Job Template ID")
    parser.add_argument("-u", "--url", type=str, required=True, help="API URL")
    args = parser.parse_args()

    if args.jobid:
        check_ansible_job_status(args.url, args.token, args.jobid)
    elif args.templateid:
        last_job_id = get_last_job_id(args.url, args.token, args.templateid)
        if last_job_id:
            check_ansible_job_status(args.url, args.token, last_job_id)
            sys.exit(0)  # Exit with code 0 to indicate successful execution
        else:
            sys.exit(1)  # Exit with code 1 to indicate an error
    else:
        print("Please provide either Ansible Job ID or Template ID using -i or -tid parameter.")
        sys.exit(1)  # Exit with code 1 to indicate an error
