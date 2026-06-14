SELECT
    listing_id::bigint as listing_id,
    date::timestamptz as review_date,
    reviewer_name,
    comments as review_text,
    sentiment
FROM {{ ref('reviews') }}
WHERE listing_id IS NOT NULL
  AND comments IS NOT NULL
  AND trim(comments) != ''