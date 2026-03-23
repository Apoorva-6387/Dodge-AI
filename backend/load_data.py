import psycopg2
import json
import os

# ✅ DB connect
conn = psycopg2.connect(
    dbname="Dodge_ai",
    user="postgres",
    password="1234",
    host="localhost"
)

cur = conn.cursor()

# ✅ Folder path
folder_path = "data/sap-o2c-data/billing_document_headers"

# ✅ Loop through JSON files
for file in os.listdir(folder_path):
    if file.endswith(".jsonl"):
        file_path = os.path.join(folder_path, file)

        with open(file_path, 'r') as f:
            for line in f:
                data = json.loads(line)

                # 🔥 Extract values
                order_id = int(data.get("billingDocument", 0))
                customer_id = int(data.get("soldToParty", 0))

                # ✅ Insert into DB
                cur.execute(
                    "INSERT INTO orders (id, customer_id) VALUES (%s, %s)",
                    (order_id, customer_id)
                )

conn.commit()
print("✅ Data inserted successfully 🚀")