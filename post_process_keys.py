import pandas as pd
import base64
import ast
import json

df = pd.read_csv('IP_domain_sshfp_and_serverKeys.csv', index_col=0)

df = df.dropna()

df['sshfp'] = df['sshfp'].apply(ast.literal_eval)
df['sshKeys'] = df['sshKeys'].apply(ast.literal_eval)

# Function to convert base64 to hex for a single element
def process_element(element):
    for i, item in enumerate(element):
        parts = item.split(' ')
        number1, number2, base64_str = parts[0], parts[1], parts[2]
        decoded_bytes = base64.b64decode(base64_str)
        hex_string = decoded_bytes.hex()
        element[i] = f"{number1} {number2} {hex_string}"
    return element



# Apply the function to the "sshKeys" column for all rows
df['sshKeys'] = df['sshKeys'].apply(process_element)

df.to_csv("IP_domain_sshfp_and_serverKeys_final.csv")


df_new = pd.read_csv('IP_hosts_sshfp_and_serverKeys.csv', index_col=0)

df_new = df_new.dropna()

df_new['sshfp_for_hosts'] = df_new['sshfp_for_hosts'].apply(ast.literal_eval)
df_new['sshKeys'] = df_new['sshKeys'].apply(ast.literal_eval)

# Function to convert base64 to hex for a single element
def process_element(element):
    for i, item in enumerate(element):
        parts = item.split(' ')
        number1, number2, base64_str = parts[0], parts[1], parts[2]
        decoded_bytes = base64.b64decode(base64_str)
        hex_string = decoded_bytes.hex()
        element[i] = f"{number1} {number2} {hex_string}"
    return element



# Apply the function to the "sshKeys" column for all rows
df_new['sshKeys'] = df_new['sshKeys'].apply(process_element)

df_new.to_csv("IP_hosts_sshfp_and_serverKeys_final.csv")