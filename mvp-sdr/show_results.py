import csv

with open('generated_emails.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("\n" + "=" * 100)
print("ENRICHMENT RESULTS - PERSONA TO PAIN TO ANGLE MAPPING")
print("=" * 100 + "\n")

for i, r in enumerate(rows, 1):
    print(f"{i:2}. {r['name']:20} | Pain: {r['pain']:35} | Angle: {r['angle']}")

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)

pains = [r['pain'] for r in rows]
angles = [r['angle'] for r in rows]

print(f"\nTotal Leads: {len(rows)}")
print(f"Unique Pains: {len(set(pains))}")
print(f"Unique Angles: {len(set(angles))}\n")

print("Pain Distribution:")
for pain in sorted(set(pains)):
    count = pains.count(pain)
    percentage = (count / len(rows)) * 100
    print(f"  {pain:40} : {count:2} leads ({percentage:5.1f}%)")

print("\nAngle Distribution:")
for angle in sorted(set(angles)):
    count = angles.count(angle)
    percentage = (count / len(rows)) * 100
    print(f"  {angle:40} : {count:2} leads ({percentage:5.1f}%)")

print("\n" + "=" * 100)
