--  TODO: Change name to FORM_13F_METADATA
CREATE TABLE SEC_FILINGS.FORM_13F (
    external_id varchar(255) NOT NULL,
    form_type varchar(255),
    cik varchar(255),
    xml_urls varchar(255),
    directory_url varchar(255),
    date_filed DATE,
    PRIMARY KEY (external_id)
);

CREATE TABLE SEC_FILINGS.FORM_13F_CONTENT (
    external_id VARCHAR(255) NOT NULL,
    info_table TEXT,
    raw_content TEXT,
    full_submission_url varchar(255),
    CONSTRAINT fk_form_13f_content FOREIGN KEY (external_id) REFERENCES SEC_FILINGS.FORM_13F (external_id)
);

CREATE TABLE SEC_FILINGS.CIK_METADATA (
    cik varchar(255),
    name varchar(255),
    last_updated_date DATE,
    PRIMARY KEY (cik)
);
