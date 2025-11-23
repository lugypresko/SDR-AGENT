import csv

with open('generated_emails.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("=" * 100)
print("PERSONA-TO-PAIN ANALYSIS")
print("=" * 100)

for i, r in enumerate(rows[:5], 1):
    print(f"\n{i}. {r['name']:20} ({r['title']})")
    print(f"   Company: {r['company']:20} | Employees: {r['employees']}")
    print(f"   Pain:    {r['pain']}")
    print(f"   Angle:   {r['angle']}")

print("\n" + "=" * 100)
print("PAIN DISTRIBUTION")
print("=" * 100)

pains = [r['pain'] for r in rows]
unique_pains = set(pains)
print(f"\nTotal Leads: {len(rows)}")
print(f"Unique Pains: {len(unique_pains)}\n")

for pain in sorted(unique_pains):
    count = pains.count(pain)
    percentage = (count / len(rows)) * 100
    print(f"  {pain:40} : {count:2} leads ({percentage:5.1f}%)")

print("\n" + "=" * 100)
