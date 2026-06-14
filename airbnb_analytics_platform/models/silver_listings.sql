select
    id as listing_id,
    listing_url,
    name as listing_name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at,
    updated_at
from {{ ref('listings') }}
where listing_id is not null
    and price is not null
    and minimum_nights > 0