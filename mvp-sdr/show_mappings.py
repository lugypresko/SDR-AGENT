import csv

with open('generated_emails.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("\n" + "=" * 80)
print("PERSONA-TO-PAIN-TO-ANGLE MAPPING")
print("=" * 80)

for r in rows:
    print(f"{r['name']:20} | {r['pain']:35} | {r['angle']}")

print("=" * 80)

# Count unique values
pains = [r['pain'] for r in rows]
angles = [r['angle'] for r in rows]

print(f"\nUnique Pains: {len(set(pains))}")
for pain in sorted(set(pains)):
    print(f"  - {pain}")

print(f"\nUnique Angles: {len(set(angles))}")
for angle in sorted(set(angles)):
    print(f"  - {angle}")
