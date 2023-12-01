import pandas as pd
import ast

df = pd.read_csv("IP_domain_sshfp_and_serverKeys_final.csv")

df['sshfp'] = df['sshfp'].apply(ast.literal_eval)
df['sshKeys'] = df['sshKeys'].apply(ast.literal_eval)

for index, row in df.iterrows():
    # Access values in each row using column names
    sshfp = row['sshfp']
    sshKeys = row['sshKeys']

    result = any(element in sshKeys for element in sshfp)

    df.at[index, "comparison"] = result

df.to_csv("IP_domain_sshfp_and_serverKeys_comparison.csv")


df_new = pd.read_csv("IP_hosts_sshfp_and_serverKeys_final.csv")

df_new['sshfp_for_hosts'] = df_new['sshfp_for_hosts'].apply(ast.literal_eval)
df_new['sshKeys'] = df_new['sshKeys'].apply(ast.literal_eval)

for index, row in df_new.iterrows():
    # Access values in each row using column names
    sshfp = row['sshfp_for_hosts']
    sshKeys = row['sshKeys']

    result = any(element in sshKeys for element in sshfp)

    df_new.at[index, "comparison"] = result

df_new.to_csv("IP_hosts_sshfp_and_serverKeys_comparison.csv")