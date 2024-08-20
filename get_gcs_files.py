import datetime
import subprocess
import os
import zipfile

weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=500)

# Specify bucket names and corresponding report file names
partner = '{partner_name}'
buckets = {
    '{new_env_bucket}': f'new_env_{partner}_report.txt',
    '{legacy_env_bucket}': f'legacy_{partner}_report.txt',
}

sub_bucket = f'{partner}/drop'

# Process each bucket and generate its reports
for bucket_name, report_file_name in buckets.items():
    # Create a partner- and bucket-specific download directory 
    download_dir = f"downloaded_zips/{partner}/{bucket_name}"
    os.makedirs(download_dir, exist_ok=True)
    # Execute gsutil command for all files in the current bucket and store output
    all_files_output_file_name = f"{bucket_name}_all_files_gsutil_output.txt"
    gsutil_all_files_command = f'gsutil ls -l -r gs://{bucket_name}/{sub_bucket}/**'
    print(f"Executing command for all files: {gsutil_all_files_command}")
    with open(all_files_output_file_name, 'w') as f:
        subprocess.run(gsutil_all_files_command, shell=True, stdout=f, text=True)

    # Execute gsutil command for zip files in the current bucket and store output
    zip_files_output_file_name = f"{bucket_name}_zip_files_gsutil_output.txt"
    gsutil_zip_files_command = f'gsutil ls -l -r gs://{bucket_name}/{sub_bucket}/*.zip'
    print(f"Executing command for zip files: {gsutil_zip_files_command}")
    with open(zip_files_output_file_name, 'w') as f:
        subprocess.run(gsutil_zip_files_command, shell=True, stdout=f, text=True)

    # Process the gsutil output for all files from the saved file
    all_files_data = []
    with open(all_files_output_file_name, 'r') as f:
        for line in f:
            parts = line.split(maxsplit=2) 
            if isinstance(parts[0], str) and parts[0].isdigit() and int(parts[0]) > 0: 

                timestamp_str = parts[1]
                file_name = parts[2].rstrip('\n')  # Remove the newline character from file_name
                partner = file_name.split('/')[3] 
                try:
                    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    print(f"Error parsing timestamp: {timestamp_str}") 
                    continue

                if timestamp >= weeks_ago:
                    all_files_data.append((file_name, partner, timestamp))

    # Check if all_files_data is empty
    if not all_files_data:
        print(f"No files found within the specified time range for {bucket_name}.")

    # Sort the data by timestamp in ascending order
    all_files_data.sort(key=lambda x: x[2], reverse=False)

    # Print the output to the original report file in pipe-delimited format
    with open(report_file_name, 'w') as f:
        for file_name, partner, timestamp in all_files_data:
            f.write(f"{file_name}|{timestamp}\n")

    print(f"Original report for {bucket_name} generated and saved to {report_file_name}")

    # Process the gsutil output for zip files from the saved file
    zip_files_data = []
    with open(zip_files_output_file_name, 'r') as f:
        for line in f:
            parts = line.split()
            if isinstance(parts[0], str) and parts[0].isdigit() and int(parts[0]) > 0: 

                timestamp_str = parts[1]
                file_name = parts[2]
                partner = file_name.split('/')[3] 
                try:
                    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    print(f"Error parsing timestamp: {timestamp_str}") 
                    continue

                if timestamp >= weeks_ago:
                    zip_files_data.append((file_name, partner, timestamp))

    # Check if zip_files_data is empty
    if not zip_files_data:
        print(f"No zip files found within the specified time range for {partner} in {bucket_name}.")

    # Sort the data by timestamp in ascending order
    zip_files_data.sort(key=lambda x: x[2], reverse=False)

    # Create a new report file name for zip files
    zip_report_file_name = report_file_name.replace(".txt", "_zip.txt")

    # Download zip files, extract contents and generate zip report
    with open(zip_report_file_name, 'w') as f:
        for file_name, partner, timestamp in zip_files_data:
            # Download the zip file to the specific directory
            local_zip_path = os.path.join(download_dir, os.path.basename(file_name))
            gsutil_download_command = f'gsutil cp {file_name} {local_zip_path}'
            subprocess.run(gsutil_download_command, shell=True)

            # Extract the zip file and list its contents
            with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                file_contents = zip_ref.namelist()

            # Write the report entry
            f.write(f"{file_name}|{timestamp}|{','.join(file_contents)}\n")

    print(f"Zip report for {bucket_name} generated and saved to {zip_report_file_name}")
