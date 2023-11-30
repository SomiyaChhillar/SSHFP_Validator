# SSHFP_Validator

This project retrieves SSH key information for a list of IP addresses and performs additional preprocessing steps. The process involves converting JSON to CSV, checking for SSH-enabled hosts, performing DNS lookups for hostnames, and retrieving SSHFP records for domains and hosts.

## Installations

Make sure to install the required dependencies using the following commands:

pip install dnspython
pip install paramiko

# How to Run
Follow the order below to run the provided scripts:

Run preprocess_convert_json_to_csv.py.

Outputs the file ssh_database1.csv.
Run preprocess_get_ssh_enabled.py.

Outputs the file ssh_database_final.csv.
Run preprocess_get_nslookup_hostnames.py.

Outputs the file IP_hostnames_nslookup.csv.
Run get_domain_sshfp_records.py.

Outputs the file sshp_records_for_domains.csv.
Run get_host_sshfp_records.py.

Outputs the file sshp_records_for_host_nslookup.csv.
Make sure to check the respective output files after running each script.

# File Descriptions
ssh_database1.csv: Initial SSH database in CSV format.
ssh_database_final.csv: Processed SSH database with SSH-enabled hosts.
IP_hostnames_nslookup.csv: Hostnames retrieved through DNS lookups.
sshp_records_for_domains.csv: SSHFP records for domains.
sshp_records_for_host_nslookup.csv: SSHFP records for hostnames obtained through DNS lookups.
