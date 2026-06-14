SELECT
    h.host_id,
    h.host_name,
    h.is_superhost,

    COUNT(DISTINCT l.listing_id) AS nb_listings,

    ROUND(AVG(l.price), 2) AS avg_price,

    COUNT(r.reviewer_name) AS total_reviews,

    SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN r.sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_reviews,

    ROUND(
        SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(r.reviewer_name), 0),
    1) AS satisfaction_rate_pct,

    ROUND(
        COUNT(r.reviewer_name)::FLOAT
        / NULLIF(COUNT(DISTINCT l.listing_id), 0),
    2) AS engagement_per_listing,

    ROUND(
        AVG(l.price) *
        (SUM(CASE WHEN r.sentiment = 'positive' THEN 1 ELSE 0 END)::FLOAT
        / NULLIF(COUNT(r.reviewer_name), 1)),
    2) AS performance_index

FROM {{ ref('silver_hosts') }} h
LEFT JOIN {{ ref('silver_listings') }} l
    ON h.host_id = l.host_id
LEFT JOIN {{ ref('silver_reviews') }} r
    ON l.listing_id = r.listing_id

GROUP BY
    h.host_id,
    h.host_name,
    h.is_superhost
