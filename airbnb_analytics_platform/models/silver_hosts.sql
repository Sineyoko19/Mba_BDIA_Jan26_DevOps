SELECT
    id AS host_id,
    name AS host_name,
    is_superhost::BOOLEAN AS is_superhost,
    created_at,
    updated_at
FROM{{ ref('hosts')}}
WHERE host_id IS NOT NULL