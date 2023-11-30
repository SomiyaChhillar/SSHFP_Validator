import pandas as pd
import json
import socket
import concurrent.futures
from tqdm import tqdm
import ast
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
import paramiko

IP = pd.read_csv("IP_hostnames_nslookup.csv", index_col=0)

IP.head()

IP_short = IP.dropna(subset=['hostname_nslookup'])
IP_short = IP_short.reset_index(drop=True)

def get_records2(df, result_df):
    ids = 'SSHFP'
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
      j = row['hostname_nslookup']
      sshfp = []
      try:
        answers = dns.resolver.resolve(j, ids)
        #print(answers)
        print("IP:\t"+row['ip_str'])
        print("Hostname:\t"+j)
        for rdata in answers:
          sshfp.append(rdata.to_text())
          print(rdata)
          #print(rdata.to_text())
          #print(rdata.target)
        new_row = (row['ip_str'], j, sshfp )
        result_df.loc[len(result_df)] = new_row
      except:
        #print("error\n")
        continue

columns = ['ip_str', 'host_nslookup', 'sshfp_for_hosts']

# Create an empty DataFrame with these columns
result_df = pd.DataFrame(columns=columns)
print(result_df)

get_records2(IP_short, result_df)
result_df.to_csv("sshp_records_for_host_nslookup.csv", index=False)