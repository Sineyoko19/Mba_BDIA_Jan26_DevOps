SELECT
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost,

    COUNT(r.reviewer_name) AS total_reviews,

    SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN r.sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    ROUND(
        SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(r.reviewer_name), 0),
    1) AS positive_rate_pct,
    ROUND(
        l.price / NULLIF(COUNT(r.reviewer_name), 1),
    2) AS price_per_review

FROM {{ ref('silver_listings') }} l
LEFT JOIN {{ ref('silver_hosts') }} h
    ON l.host_id = h.host_id
LEFT JOIN {{ ref('silver_reviews') }} r
    ON l.listing_id = r.listing_id

GROUP BY
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost