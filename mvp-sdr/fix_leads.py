import csv

def fix_leads():
    input_file = 'leads.csv'
    output_file = 'leads_clean.csv'
    
    clean_rows = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Header
    header = lines[0].strip().split(',')
    clean_rows.append(header)
    
    for line in lines[1:]:
        line = line.strip()
        if not line: continue
        
        if '\t' in line:
            # Tab separated (New Leads)
            cols = line.split('\t')
            # Mapping based on observation:
            # 0:First, 1:Last, 2:Title, 3:Email, 4:LinkedIn, ..., 8:Company, 9:Employees
            if len(cols) > 9:
                name = f"{cols[0]} {cols[1]}"
                title = cols[2]
                linkedin = cols[4]
                company = cols[8]
                employees = cols[9]
                
                clean_rows.append([name, company, title, linkedin, employees])
        else:
            # Comma separated (Old Leads)
            # Handle potential commas in quotes? Basic split for now as original data was simple
            # But csv module is better.
            # Let's just assume the original lines are well-formed CSV strings
            # We can parse them with csv.reader
            reader = csv.reader([line])
            for row in reader:
                clean_rows.append(row)

    # Write back
    with open(input_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(clean_rows)
        
    print(f"Fixed {len(clean_rows)} rows in leads.csv")

if __name__ == "__main__":
    fix_leads()
