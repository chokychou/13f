-- TODO: change the file name to be more specific
INSERT INTO SEC_FILINGS.FORM_13F (external_id, company_name, form_type, cik, date_filed, directory_url)
VALUES (
    %s, -- external_id
    %s,
    %s,
    %s,
    %s,
    %s
);