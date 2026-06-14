WITH reviews_with_flag AS (
    SELECT
        r.reviewer_name,
        r.review_date,
        r.sentiment,
        r.listing_id,

        CASE
            WHEN EXISTS (
                SELECT 1
                FROM {{ ref('silver_full_moon_dates') }} fm
                WHERE r.review_date BETWEEN
                    (fm.full_moon_date - INTERVAL '3 days')
                    AND
                    (fm.full_moon_date + INTERVAL '3 days')
            ) THEN TRUE
            ELSE FALSE
        END AS is_near_full_moon

    FROM {{ ref('silver_reviews') }} r
    WHERE r.review_date IS NOT NULL
      AND r.sentiment IN ('positive', 'negative', 'neutral')
)

SELECT
    is_near_full_moon,
    sentiment,

    COUNT(*) AS nb_reviews,

    ROUND(
        CASE
            WHEN SUM(COUNT(*)) OVER (PARTITION BY is_near_full_moon) = 0 THEN 0
            ELSE (
                COUNT(*) * 100.0
                / SUM(COUNT(*)) OVER (PARTITION BY is_near_full_moon)
            )
        END,
    1) AS pct_within_period

FROM reviews_with_flag

GROUP BY
    is_near_full_moon,
    sentiment

ORDER BY
    is_near_full_moon,
    nb_reviews DESC