INSERT INTO SEC_FILINGS.FORM_13F (external_id, form_type, cik, date_filed, directory_url)
VALUES (
    %s, -- external_id
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT DO NOTHING;
