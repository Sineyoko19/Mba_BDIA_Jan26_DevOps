import csv
import os

input_path = "seeds/reviews.csv"
output_path = "seeds/reviews_fixed.csv"

good_rows = 0
skipped_rows = 0

with open(input_path, 'r', encoding='utf-8') as infile, \
     open(output_path, 'w', encoding='utf-8', newline='') as outfile:

    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)

    for i, line in enumerate(infile):
        line = line.rstrip('\r\n')
        try:
            # Try parsing normally first
            row = list(csv.reader([line]))[0]

            # If we got 1 column, the whole row is wrapped in quotes — unwrap it
            if len(row) == 1:
                inner = row[0]  # unwrap outer quotes
                row = list(csv.reader([inner]))[0]

            if len(row) == 5:
                writer.writerow(row)
                good_rows += 1
            else:
                skipped_rows += 1
        except Exception:
            skipped_rows += 1

os.replace(output_path, input_path)
print(f"✅ Done — kept: {good_rows} rows, skipped: {skipped_rows} rows")