select
    id as listing_id,
    listing_url,
    name as listing_name,
    room_type,
    minimum_nights,
    host_id,
    TRY_CAST(price As float) AS price,
    created_at,
    updated_at
from {{ ref('listings') }}
where TRY_CAST(listing_id AS bigint) IS NOT NULL
    and price is not null
    and minimum_nights > 0