CREATE TABLE SEC_FILINGS.FORM_13F (
    id integer NOT NULL,
    filing_num varchar(255) NOT NULL,
    url varchar(255),
    raw_content TEXT,
    date_filed DATE,
    CONSTRAINT unique_filing_num PRIMARY KEY (ID, filing_num)
);
