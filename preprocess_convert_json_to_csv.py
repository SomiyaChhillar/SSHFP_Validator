import zipfile

zip_file_name = 'data.json.zip'
json_file_name = 'data.json'

with zipfile.ZipFile(zip_file_name, 'r') as z:
    with z.open(json_file_name) as f:
        file_content = f.read().decode('utf-8')

# Split the content assuming each JSON object is separated by a newline
json_objects = file_content.split('\n')

# Extract only the required fields
data = []
for obj in json_objects:
    if obj.strip():
        json_data = json.loads(obj)
        # Extract only the specified fields
        selected_data = {key: json_data.get(key, None) for key in ['ip_str','domains', 'hostnames']}
        data.append(selected_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

df.to_csv("ssh_database1.csv", index=False)