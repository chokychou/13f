INSERT INTO SEC_FILINGS.CUSIP_METADATA (cusip, name)
VALUES (
    %s,
    %s
)
ON CONFLICT (cusip) DO NOTHING;
