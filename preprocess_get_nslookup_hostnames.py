import pandas as pd
import json
import socket
import concurrent.futures
from tqdm import tqdm
import ast
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
import paramiko


df = pd.read_csv('ssh_database_final.csv')

df['domains'] = df['domains'].apply(ast.literal_eval)
df['hostnames'] = df['hostnames'].apply(ast.literal_eval)

df = df[df['is_ssh_available']]
df = df.reset_index(drop=True)
df = df.drop('is_ssh_available', axis=1)


IP_domain = pd.DataFrame(df[['ip_str', 'domains']] )


IP_domain.to_csv("IP_domain.csv")

IP_hostname = pd.DataFrame(df[['ip_str', 'hostnames']] )


File_hostnames = open('Hostnames.txt', 'w')
for i in (IP_hostname['hostnames']):
    for j in i:
      File_hostnames.write("%s\n" % j)

File_hostnames.close()


File_domains = open('Domains.txt', 'w')
for i in (IP_domain['domains']):
    for j in i:
      File_domains.write("%s\n" % j)

File_domains.close()

File_IP = open('IP.txt', 'w')
for i in (IP_domain['ip_str']):
    File_IP.write("%s\n" % i)

File_IP.close()

def remove_empty_line(filename):
  with open(filename) as f_input:
      data = f_input.read().rstrip('\n')

  with open(filename, 'w') as f_output:
      f_output.write(data)

remove_empty_line('Hostnames.txt')

remove_empty_line('Domains.txt')

remove_empty_line('IP.txt')

IP_domain = pd.read_csv("IP_domain.csv")

IP_domain['domains'] = IP_domain['domains'].apply(ast.literal_eval)

IP = pd.read_csv("IP.txt", header=None, names=['ip_str'])


def nslookup(ip_address):
    try:
        # Perform reverse DNS lookup
        host_name, _, _ = socket.gethostbyaddr(ip_address)
        return host_name
    except socket.herror:
        # If an exception occurs (e.g., no PTR record found), return None
        return None

# Function to perform nslookup and store result in a new column
def perform_nslookup(ip_address):
    hostname = nslookup(ip_address)
    return hostname

# Function to track progress
def update_progress(*args):
    pbar.update()

# Set up a progress bar
with tqdm(total=len(IP), desc="Performing nslookup", position=0, unit="ip") as pbar:
    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [executor.submit(perform_nslookup, ip) for ip in IP['ip_str']]

        # Add a callback to update progress when a task is completed
        for future in futures:
            future.add_done_callback(update_progress)

        # Gather results
        results = [future.result() for future in futures]

IP['hostname_nslookup'] = results

IP.to_csv("IP_hostnames_nslookup.csv")
