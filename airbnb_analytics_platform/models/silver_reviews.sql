SELECT
    TRY_CAST(listing_id AS bigint) as listing_id,
    TRY_CAST(date AS timestamptz) as review_date,
    reviewer_name,
    comments as review_text,
    sentiment
FROM {{ ref('reviews') }}
WHERE TRY_CAST(listing_id AS bigint) IS NOT NULL
  AND TRY_CAST(date AS timestamptz) IS NOT NULL  
  AND comments IS NOT NULL
  AND trim(comments) != ''