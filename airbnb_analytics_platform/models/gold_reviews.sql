SELECT
    l.room_type,
    r.sentiment,

    COUNT(*) AS nb_reviews,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (PARTITION BY l.room_type),
    1) AS sentiment_share_pct

FROM {{ ref('silver_reviews') }} r
JOIN {{ ref('silver_listings') }} l
    ON r.listing_id = l.listing_id

WHERE r.sentiment IN ('positive', 'negative', 'neutral')

GROUP BY
    l.room_type,
    r.sentiment

ORDER BY
    l.room_type,
    nb_reviews DESC;