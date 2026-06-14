SELECT
    h.host_id,
    h.host_name,
    h.is_superhost,

    COUNT(DISTINCT l.listing_id) AS nb_listings,

    AVG(l.price) AS avg_price,
    MIN(l.price) AS min_price,
    MAX(l.price) AS max_price,

    COUNT(r.reviewer_name) AS total_reviews,

    SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN r.sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,
    SUM(CASE WHEN r.sentiment = 'neutral' THEN 1 ELSE 0 END) AS neutral_reviews,

    CASE
        WHEN COUNT(r.reviewer_name) = 0 THEN 0
        ELSE (
            SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0
            / COUNT(r.reviewer_name)
        )
    END AS positive_rate_pct

FROM {{ ref('silver_hosts') }} h
LEFT JOIN {{ ref('silver_listings') }} l 
    ON h.host_id = l.host_id
LEFT JOIN {{ ref('silver_reviews') }} r 
    ON l.listing_id = r.listing_id

GROUP BY
    h.host_id,
    h.host_name,
    h.is_superhost