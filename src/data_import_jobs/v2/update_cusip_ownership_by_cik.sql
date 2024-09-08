INSERT INTO SEC_FILINGS.CUSIP_OWNERSHIP (cusip, cik, type, number, value, last_updated_date)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT (cusip, cik) DO NOTHING;
