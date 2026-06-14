
SELECT
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost,

    COUNT(r.reviewer_name) AS total_reviews,

    SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN r.sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    SUM(CASE WHEN r.sentiment = 'neutral' THEN 1 ELSE 0 END) AS neutral_reviews,

    CASE 
        WHEN COUNT(r.reviewer_name) = 0 THEN 0
        ELSE ROUND(
            SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0
            / COUNT(r.reviewer_name),
        1)
    END AS positive_rate_pct

FROM {{ ref('silver_listings') }} l
LEFT JOIN {{ ref('silver_hosts') }} h 
    ON l.host_id = h.host_id
LEFT JOIN {{ ref('silver_reviews') }} r 
    ON l.listing_id = r.listing_id

GROUP BY
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost