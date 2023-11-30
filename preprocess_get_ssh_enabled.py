import pandas as pd
import json
import socket
import concurrent.futures
from tqdm import tqdm
import ast
from concurrent.futures import ThreadPoolExecutor

import dns.resolver
import paramiko

df = pd.read_csv('ssh_database1.csv',index_col=None)

def check_ssh(ip_address, port=22, timeout=5):
    try:
        # Create a socket to attempt to connect to the SSH server
        sock = socket.create_connection((ip_address, port), timeout=timeout)
        
        # Close the socket if connection is successful
        sock.close()
        
        # If no exception is raised, assume SSH is available
        return True
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error):
        # AuthenticationException and SSHException indicate a valid SSH server
        # socket.error indicates that the socket connection could not be established
        return False

def parallel_check_ssh(row):
    return check_ssh(row.ip_str)

# Function to track progress
def track_progress(iterable, total):
    return tqdm(iterable, total=total, desc="Processing", unit="record", position=0, leave=True)

# Apply the function in parallel using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(track_progress(executor.map(parallel_check_ssh, df.itertuples(index=False)), total=len(df)))

df.loc[:, 'is_ssh_available'] = results

df.to_csv("ssh_database_final.csv", index=False)