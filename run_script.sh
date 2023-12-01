#!/bin/bash

# Run preprocess_convert_json_to_csv.py
echo "Running preprocess_convert_json_to_csv.py..."
python preprocess_convert_json_to_csv.py
echo "Done."

# Run preprocess_get_ssh_enabled.py
echo "Running preprocess_get_ssh_enabled.py..."
python preprocess_get_ssh_enabled.py
echo "Done."

# Run preprocess_get_nslookup_hostnames.py
echo "Running preprocess_get_nslookup_hostnames.py..."
python preprocess_get_nslookup_hostnames.py
echo "Done."

# Run get_domain_sshfp_records.py
echo "Running get_domain_sshfp_records.py..."
python get_domain_sshfp_records.py
echo "Done."

# Run get_host_sshfp_records.py
echo "Running get_host_sshfp_records.py..."
python get_host_sshfp_records.py
echo "Done."

# Run get_server_keys_for_domains.py
echo "Running get_server_keys_for_domains.py..."
get_server_keys_for_domains.py

# Run get_server_keys_for_hosts.py
echo "Running get_server_keys_for_hosts.py..."
get_server_keys_for_hosts.py

# Run post_process_keys.py
echo "Running post_process_keys.py..."
post_process_keys.py

# Run comparison.py
echo "Running comparison.py..."
comparison.py

echo "All scripts executed successfully."
