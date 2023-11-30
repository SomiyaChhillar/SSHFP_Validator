import pandas as pd
import json
import ast
from tqdm import tqdm

import dns.resolver
import paramiko


df = pd.read_csv('ssh_database_final.csv')


df['domains'] = df['domains'].apply(ast.literal_eval)

df['hostnames'] = df['hostnames'].apply(ast.literal_eval)

df = df[df['is_ssh_available']]



df = df.reset_index(drop=True)
df = df.drop('is_ssh_available', axis=1)



IP_domain = pd.DataFrame(df[['ip_str', 'domains']] )


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


def get_records2(df, result_df):
    ids = 'SSHFP'
    count = 1
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
      for j in row['domains']:
        sshfp = []
        try:
          answers = dns.resolver.resolve(j, ids)
          #print(answers)
          print("IP:\t"+row['ip_str'])
          print("Domain:\t"+j)
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

columns = ['ip_str', 'domain', 'sshfp']

# Create an empty DataFrame with these columns
result_df = pd.DataFrame(columns=columns)

get_records2(IP_domain, result_df)


result_df.to_csv("sshp_records_for_domains.csv", index=False)
