import psycopg2

conn = psycopg2.connect(database="finance", user="postgres", password="terces##")

cur = conn.cursor()

cur.execute("SELECT vendor_number,vendor_short_desc from finance.vendors ORDER BY vendor_number")

records = cur.fetchall()

print(records)