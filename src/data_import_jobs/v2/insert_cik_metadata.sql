INSERT INTO SEC_FILINGS.CIK_METADATA (cik, name, last_updated_date)
VALUES (
    %s,
    %s,
    %s
)
ON CONFLICT (cik) DO UPDATE SET 
    name = excluded.name,
    last_updated_date = excluded.last_updated_date;
