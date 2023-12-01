import pandas as pd
import matplotlib.pyplot as plt


df_final_dataset = pd.read_csv("ssh_database_final.csv")

df_final_dataset = df_final_dataset[df_final_dataset['is_ssh_available']]
# Assuming correctness_percentages is a list of correctness percentages for each condition
conditions = ['Total Dataset', 'Dataset with SSH enabled']
correctness_percentages = [300000, df_final_dataset.shape[0]]

plt.pie(correctness_percentages, labels=conditions, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'deepskyblue'])
plt.title('SSH enabled Percentage')
plt.show()


#second plot
total_count = df_final_dataset.shape[0]
df_domain_with_sshfp = pd.read_csv("sshp_records_for_domains.csv")
number_of_domains_with_sshfp = df_domain_with_sshfp.shape[0]
percentage_domain_sshfp = (float(number_of_domains_with_sshfp)/float(total_count))*100


df_domain_with_sshfp_matching = pd.read_csv("IP_domain_sshfp_and_serverKeys_comparison.csv")
df_domain_with_sshfp_matching = df_domain_with_sshfp_matching[df_domain_with_sshfp_matching['comparison']]
number_of_domains_with_sshfp_matching = df_domain_with_sshfp_matching.shape[0]
percentage_domain_matching = (float(number_of_domains_with_sshfp_matching)/float(total_count))*100

# Plotting the bar chart
categories = ['Domains with SSHFP', 'IP uses Domain SSHFP']
counts = [number_of_domains_with_sshfp, number_of_domains_with_sshfp_matching]
percentages = [percentage_domain_sshfp, percentage_domain_matching]

fig, ax = plt.subplots()

bars = ax.bar(categories, counts, color=['blue', 'orange'])

# Adding labels and percentages to each bar
for bar, percentage in zip(bars, percentages):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}\n({percentage:.{3}f}%)', ha='center', va='bottom')

# Adding titles and labels
plt.title('Number and Percentage of Domain Records')
plt.xlabel('Categories')
plt.ylabel('Number of Records')

# Display the plot
plt.show()

#third plot
df_hosts_with_sshfp = pd.read_csv("sshp_records_for_host_nslookup.csv")
number_of_hosts_with_sshfp = df_hosts_with_sshfp.shape[0]
percentage_hosts_sshfp = (float(number_of_hosts_with_sshfp)/float(total_count))*100


df_hosts_with_sshfp_matching = pd.read_csv("IP_hosts_sshfp_and_serverKeys_comparison.csv")
df_hosts_with_sshfp_matching = df_hosts_with_sshfp_matching[df_hosts_with_sshfp_matching['comparison']]
number_of_hosts_with_sshfp_matching = df_hosts_with_sshfp_matching.shape[0]
percentage_hosts_matching = (float(number_of_hosts_with_sshfp_matching)/float(total_count))*100

# Plotting the bar chart
categories_ = ['Sub-domains with SSHFP', 'IP uses Sub-domain SSHFP']
counts_ = [number_of_hosts_with_sshfp, number_of_hosts_with_sshfp_matching]
percentages_ = [percentage_hosts_sshfp, percentage_hosts_matching]

fig, ax = plt.subplots()

bars_ = ax.bar(categories_, counts_, color=['blue', 'orange'])

# Adding labels and percentages to each bar
for bar, percentage in zip(bars_, percentages_):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}\n({percentage:.{3}f}%)', ha='center', va='bottom')

# Adding titles and labels
plt.title('Number and Percentage of Sub-domain Records')
plt.xlabel('Categories')
plt.ylabel('Number of Records')

# Display the plot
plt.show()