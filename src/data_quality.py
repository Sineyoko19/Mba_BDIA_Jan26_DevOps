import duckdb

db = duckdb.connect(database="airbnb_analytics_platform/dev.duckdb")

print("Verify the unicity of host_id")
check_hosts_query = """
SELECT count(host_id) AS total_hosts,
       count(DISTINCT host_id) AS unique_hosts,
FROM silver_hosts;
"""
print(db.execute(check_hosts_query).fetchdf())

print("Superhost distribution")
check_superhost_query = """
SELECT is_superhost, COUNT(*) as count
FROM main.silver_hosts
GROUP BY is_superhost
ORDER BY count DESC
"""
print(db.execute(check_superhost_query).fetchdf())

print("Check hosts with no listings")
check_no_listings_query = """
SELECT COUNT(*) as hosts_without_listings
FROM main.silver_hosts h
LEFT JOIN main.listings l ON h.host_id = l.host_id
WHERE l.host_id IS NULL
"""
print(db.execute(check_no_listings_query).fetchdf())
#------------
print("Verify the integrity of minimum_nights column")
check_min_nights_query = """
SELECT
    MIN(minimum_nights)     as min,
    MAX(minimum_nights)     as max,
    AVG(minimum_nights)     as avg
FROM silver_listings;"""

print(db.execute(check_min_nights_query).fetchdf())


#---------------
print("Verify room type distribution")
check_room_type_query = """
SELECT 
    room_type, 
    COUNT(*) as count_rooms
FROM silver_listings
GROUP BY room_type
ORDER BY count_rooms DESC
"""
print(db.execute(check_room_type_query).fetchdf())


#------------
print("verify reviews scores")

check_reviews_scores_query = """SELECT sentiment, COUNT(*) as count
from silver_reviews
group by sentiment
order by count DESC;"""
print(db.execute(check_reviews_scores_query).fetchdf())

# ---- 
print("Verify duplicates in reviews table")
check_duplicated_query = """
SELECT listing_id, review_date, reviewer_name, COUNT(*) as occurrences
FROM silver_reviews
GROUP BY listing_id, review_date, reviewer_name
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
"""

print(db.execute(check_duplicated_query).fetchdf())