WITH base_reviews AS (
    SELECT
        r.reviewer_name,
        r.review_date,
        r.sentiment,
        r.listing_id
    FROM {{ ref('silver_reviews') }} r
    WHERE r.review_date IS NOT NULL
      AND r.sentiment IN ('positive', 'negative', 'neutral')
),

moon_flag AS (
    SELECT
        br.*,
        CASE 
            WHEN fm.full_moon_date IS NOT NULL THEN 1
            ELSE 0
        END AS is_near_full_moon
    FROM base_reviews br
    LEFT JOIN {{ ref('silver_full_moon_dates') }} fm
        ON br.review_date BETWEEN (fm.full_moon_date - INTERVAL '3 days')
                              AND (fm.full_moon_date + INTERVAL '3 days')
)

SELECT
    is_near_full_moon,
    sentiment,
    COUNT(*) AS nb_reviews,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (PARTITION BY is_near_full_moon),
    1) AS sentiment_share_pct

FROM moon_flag

GROUP BY is_near_full_moon, sentiment
ORDER BY is_near_full_moon, nb_reviews DESC