import csv
try:
    with open('generated_emails.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f"{'NAME':20} | {'PAIN':30} | {'ANGLE'}")
        print("-" * 80)
        for r in reader:
            print(f'{r["name"]:20} | {r["pain"]:30} | {r["angle"]}')
except Exception as e:
    print(f"Error: {e}")
