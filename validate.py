import dns.resolver
import dns.dnssec
import pandas
import ast

def validate_rrsig(domain, record_type):
    try:
        # Query for DNSKEY records
        dnskey_response = dns.resolver.resolve(domain, dns.rdatatype.DNSKEY)
        dnskey_records = [record for record in dnskey_response]

        # Query for RRSIG records
        rrsig_response = dns.resolver.resolve(domain, dns.rdatatype.RRSIG, raise_on_no_answer=False)
        rrsig_records = [record for record in rrsig_response]

        if not rrsig_records:
            #print(f"No RRSIG records found for {record_type} in {domain}.")
            return False

        # Validate RRSIG with DNSKEY
        dns.dnssec.validate(rrsig_records, dnskey_records)
        #print(f"RRSIG for {record_type} records in {domain} is valid.")
        return True

    except dns.resolver.NoAnswer:
        #print(f"No DNSKEY records found for {domain}.")
        return False
    except dns.resolver.NXDOMAIN:
        #print(f"The domain {domain} does not exist.")
        return False
    except dns.resolver.Timeout:
        #print(f"Timeout while resolving records for {domain}.")
        return False
    except dns.exception.DNSException as e:
        #print(f"Error validating RRSIG for {record_type} in {domain}: {e}")
        return False



df_new = pandas.read_csv("IP_hosts_sshfp_and_serverKeys_comparison.csv")
df_new['sshfp_for_hosts'] = df_new['sshfp_for_hosts'].apply(ast.literal_eval)
df_new['sshKeys'] = df_new['sshKeys'].apply(ast.literal_eval)

df_new = df_new[df_new['comparison']]

df_new.reset_index(drop=True, inplace=True)

for index, row in df_new.iterrows():
    #print(index)
    # Access values in each row using column names
    domain_to_check = row['host_nslookup']
    sshfp_record_type = dns.rdatatype.SSHFP
    result = validate_rrsig(domain_to_check, sshfp_record_type)

    df_new.at[index, "DNSSEC"] = result


df_new.to_csv("IP_hosts_sshfp_and_serverKeys_comparison_dnssec.csv", index=False)

df = pandas.read_csv("IP_domain_sshfp_and_serverKeys_comparison.csv")
df['sshfp'] = df['sshfp'].apply(ast.literal_eval)
df['sshKeys'] = df['sshKeys'].apply(ast.literal_eval)

df = df[df['comparison']]

df.reset_index(drop=True, inplace=True)

for index, row in df.iterrows():
    #print(index)
    # Access values in each row using column names
    domain_to_check = row['domain']
    sshfp_record_type = dns.rdatatype.SSHFP
    result = validate_rrsig(domain_to_check, sshfp_record_type)

    df.at[index, "DNSSEC"] = result


df.to_csv("IP_domain_sshfp_and_serverKeys_comparison_dnssec.csv", index=False)