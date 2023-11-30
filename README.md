# SSHFP_Validator

This project retrieves SSH key information for a list of IP addresses and performs additional preprocessing steps. The process involves converting JSON to CSV, checking for SSH-enabled hosts, performing DNS lookups for hostnames, and retrieving SSHFP records for domains and hosts.

# Installations

Make sure to install the required dependencies using the following commands:

```bash
pip install dnspython
pip install paramiko
```

# How to Run
To execute the project files in the correct order, you can use the provided shell script.

1. Open your terminal.
2. Navigate to the project directory
   ```bash
   cd /path_to_your_project
3. Run the following command to execute the scripts:
   ```bash
   ./run_script.sh
4. The provided run_scripts.sh script will run the necessary Python files in the required order. Ensure that you have the appropriate permissions to execute the script:
   ```bash
   chmod +x run_script.sh

# Output Files
- ssh_database1.csv: Output of preprocess_convert_json_to_csv.py
- ssh_database_final.csv: Output of preprocess_get_ssh_enabled.py
- IP_hostnames_nslookup.csv: Output of preprocess_get_nslookup_hostnames.py
- sshp_records_for_domains.csv: Output of get_domain_sshfp_records.py
- sshp_records_for_host_nslookup.csv: Output of get_host_sshfp_records.py
