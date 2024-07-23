#!/usr/bin/python3.9
import argparse
import requests
import sys
import urllib3

# Disable warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_most_recent_job_id(api_url, api_token, template_id):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    api_endpoint = f"{api_url}/api/v2/job_templates/{template_id}/jobs/?order_by=-finished"

    try:
        response = requests.get(api_endpoint, headers=headers, verify=False)
        response.raise_for_status()
        jobs_data = response.json()
        launches = jobs_data.get("results", [])
        if launches:
            most_recent_job = launches[0]
            return most_recent_job["id"]
        else:
            print(f"No jobs found for the specified template ID {template_id}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve job launches. Error: {e}")
        return None

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
        return job_status
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve job status. Error: {e}")
        return "error"

def check_jobs_from_file(api_url, api_token, file_path):
    error_found = False
    pending_found = False
    failed_jobs = []

    try:
        with open(file_path, 'r') as file:
            template_ids = [line.strip() for line in file if line.strip().isdigit()]

        for template_id in template_ids:
            most_recent_job_id = get_most_recent_job_id(api_url, api_token, int(template_id))
            if most_recent_job_id:
                job_status = check_ansible_job_status(api_url, api_token, most_recent_job_id)
                if job_status == "failed":
                    error_found = True
                    failed_jobs.append(most_recent_job_id)
                elif job_status == "pending":
                    pending_found = True
            else:
                error_found = True
    except Exception as e:
        print(f"Failed to read template IDs from file. Error: {e}")
        sys.exit(1)

    if error_found:
        print(f"Failed Job IDs: {', '.join(map(str, failed_jobs))}")
        sys.exit(1)
    elif pending_found:
        print("OK")
        sys.exit(2)
    else:
        print("OK")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Ansible job status through API.")
    parser.add_argument("-t", "--token", type=str, required=True, help="API Token")
    parser.add_argument("-i", "--jobid", type=int, help="Ansible Job ID")
    parser.add_argument("-tid", "--templateid", type=int, help="Ansible Job Template ID")
    parser.add_argument("-u", "--url", type=str, required=True, help="API URL")
    parser.add_argument("-f", "--file", type=str, help="File containing list of Template IDs")
    args = parser.parse_args()

    if args.jobid:
        job_status = check_ansible_job_status(args.url, args.token, args.jobid)
        if job_status == "successful":
            print("OK")
            sys.exit(0)
        elif job_status == "pending":
            print("OK")
            sys.exit(2)
        else:
            print(f"Job ID {args.jobid} failed")
            sys.exit(1)
    elif args.templateid:
        most_recent_job_id = get_most_recent_job_id(args.url, args.token, args.templateid)
        if most_recent_job_id:
            job_status = check_ansible_job_status(args.url, args.token, most_recent_job_id)
            if job_status == "successful":
                print("OK")
                sys.exit(0)
            elif job_status == "pending":
                print("OK")
                sys.exit(2)
            else:
                print(f"Most recent Job ID {most_recent_job_id} failed")
                sys.exit(1)
        else:
            sys.exit(1)
    elif args.file:
        check_jobs_from_file(args.url, args.token, args.file)
    else:
        print("Please provide either an Ansible Job ID, Template ID, or a file containing Template IDs using -i, -tid, or -f parameter.")
        sys.exit(1)
