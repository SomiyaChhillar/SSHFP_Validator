import pandas as pd
import json
import ast
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import socket
import paramiko
import argparse
import sys
import hashlib
import binascii
import base64
import signal
import time

def handler(signum, frame):
    # This function will be called when the timeout occurs
    print("Timeout occurred")


def hex_to_base64(hex_string):

    # Convert hex string to bytes
    hex_bytes = binascii.unhexlify(hex_string)

    # Encode the bytes as base64
    base64_encoded = base64.b64encode(hex_bytes).decode('utf-8')

    return base64_encoded

def sha256_base64(input_string):
    # Decode the base64 input string
    decoded_bytes = base64.b64decode(input_string)

    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(decoded_bytes).digest()

    # Encode the hash in base64
    base64_encoded_hash = base64.b64encode(sha256_hash).decode('utf-8')

    return (base64_encoded_hash)

def sha1_base64(input_string):
    # Decode the base64 input string
    decoded_bytes = base64.b64decode(input_string)

    # Calculate the SHA-1 hash
    sha1_hash = hashlib.sha1(decoded_bytes).digest()

    # Encode the hash in base64
    base64_encoded_hash = base64.b64encode(sha1_hash).decode('utf-8')

    return base64_encoded_hash


def ssh_keyscan(address):
    pub_keys = []
    try:
      transport = paramiko.Transport(address)
    except paramiko.IncompatiblePeer as e:
      return None
    except paramiko.SSHException as e:
        return None
    except Exception as e:
        return None

    opts = paramiko.transport.Transport(socket.socket()).get_security_options()
    #print(opts.key_types)

    for i in opts.key_types:

        try:
            transport = paramiko.Transport(address)
            transport.get_security_options().key_types = [i]
            transport.connect()
            key = transport.get_remote_server_key()
            print(i+":")
            key_base64 = key.get_base64()
            key_sha256 = sha256_base64(key_base64)
            key_sha1 = sha1_base64(key_base64)
            algo = ""
            if ((i=='ecdsa-sha2-nistp256') or(i=='ecdsa-sha2-nistp384') or (i=='ecdsa-sha2-nistp521')):
              algo = str(3)
            elif((i== 'rsa-sha2-512') or(i=='rsa-sha2-256') or (i=='ssh-rsa')):
              algo = str(1)
            elif(i == 'ssh-ed25519'):
              algo = str(4)
            elif(i == 'ssh-dss'):
              algo = str(2)
            else:
              algo = 0
            tuple_input1 = algo+" "+str(2)+" "+ str(key_sha256)
            tuple_input2 = algo+" "+str(1)+" "+ str(key_sha1)
            pub_keys.append(tuple_input1)
            pub_keys.append(tuple_input2)

        except (paramiko.IncompatiblePeer,paramiko.SSHException) as e:
            pass
            # Handle the IncompatiblePeer exception here

        except paramiko.SSHException as e:
            pass

        except Exception as e:
            pass
        finally:
            transport.close()

    return pub_keys

def get_key_for_IP(IP):
    host = IP
    address = host+':'+"22"

    # Set the timeout to 5 seconds
    timeout_duration = 15

    # Set the alarm (timeout)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)

    try:
        # Call your function here
        keys = ssh_keyscan(address)
    except TimeoutError as e:
        print(e)
        # Handle the timeout exception here
    finally:
        # Cancel the alarm (cleanup)
        signal.alarm(0)
    return(keys)

def get_keys_for_dataframe(df):
    # Create a tqdm progress bar for the apply function
    #tqdm.pandas(desc="Processing IPs", position=0, leave=True)

    # Apply the get_keys_for_IP function to the 'ip_str' column
    #df['sshKeys'] = df['ip_str'].progress_apply(get_key_for_IP)
    print(df['ip_str'])
    df['sshKeys'] = df['ip_str'].apply(get_key_for_IP)

    # Close the tqdm progress bar
    return df

IPs = pd.read_csv("sshp_records_for_host_nslookup.csv", encoding='utf-8')

new_df = get_keys_for_dataframe(IPs)

new_df.to_csv("IP_hosts_sshfp_and_serverKeys.csv")