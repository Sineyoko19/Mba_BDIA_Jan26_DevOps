import duckdb

db = duckdb.connect("airbnb_analytics_platform/dev.duckdb")

db.execute("""
    CREATE OR REPLACE TABLE main.reviews AS
    SELECT *
    FROM read_csv(
        'airbnb_analytics_platform/seeds/reviews.csv',
        columns = {
            'listing_id': 'VARCHAR',
            'date': 'VARCHAR',
            'reviewer_name': 'VARCHAR',
            'comments': 'VARCHAR',
            'sentiment': 'VARCHAR'
        },
        strict_mode = false,
        ignore_errors = true
    )
""")


count = db.execute("SELECT COUNT(*) FROM main.reviews").fetchone()[0]
print(f"✅ Loaded {count} rows into main.reviews")
db.close()