CREATE TABLE paymasters (
    id VARCHAR PRIMARY KEY,
    kind  VARCHAR(250),
    name  VARCHAR(250),
    document  VARCHAR(250),
    email_primary  VARCHAR(250),
    email_secondary  VARCHAR(250),
    deleted_at DATE,
    created_at DATE,
    updated_at DATE
);

CREATE TABLE assets_parts (
    id VARCHAR PRIMARY KEY,
    name  VARCHAR(250),
    document_number  VARCHAR(250),
    contact_email  VARCHAR(250),
    contact_phone_number  VARCHAR(250),
    deleted_at DATETIME,
    created_at DATETIME,
    updated_at DATETIME,
    type  VARCHAR(250)
);

CREATE TABLE participants (
    id VARCHAR(250) PRIMARY KEY,
    name VARCHAR(250),
    state  VARCHAR(250),
    contact_phone_number  VARCHAR(250),
    document_number  VARCHAR(250),
    company_name  VARCHAR(250),
    kind  VARCHAR(250),
    paymaster_id  VARCHAR(250),
    FOREIGN KEY (paymaster_id) REFERENCES paymasters(id)
);
CREATE INDEX paymaster_id_idx ON participants(paymaster_id);


CREATE TABLE participant_authorized_third_parties (
    id VARCHAR(250) PRIMARY KEY,
    participant_id  VARCHAR(250),
    authorized_third_party_id  VARCHAR(250) UNIQUE,
    created_at  DATETIME,
    updated_at DATETIME,
    state  VARCHAR(250),
    approved_at DATETIME,
    rejected_at DATETIME,
    FOREIGN KEY (participant_id) REFERENCES participants(id)
);
CREATE INDEX participant_id_idx ON participant_authorized_third_parties(participant_id);


CREATE TABLE fk_authorized_third_party_participants (
    authorized_third_party_id  VARCHAR(250),
    participant_id  VARCHAR(250),
    PRIMARY KEY (authorized_third_party_id, participant_id),
    FOREIGN KEY (authorized_third_party_id) REFERENCES participant_authorized_third_parties(authorized_third_party_id),
    FOREIGN KEY (participant_id) REFERENCES participants(id)
);
create index authorized_third_party_id_idx on fk_authorized_third_party_participants(authorized_third_party_id);
create index participant_id_idx on fk_authorized_third_party_participants(participant_id);

CREATE TABLE assets_trade_bills (
    id VARCHAR(250) PRIMARY KEY,
    due_date DATETIME,
    nfe_number  VARCHAR(250),
    nfe_series  VARCHAR(250),
    kind  VARCHAR(250),
    state  VARCHAR(250),
    payer_id  VARCHAR(250),
    endorser_original_id  VARCHAR(250),
    new_due_date DATETIME, 
    participant_id  VARCHAR(250),
    ballast_kind  VARCHAR(250),
    invoice_number  VARCHAR(250),
    payment_place  VARCHAR(250),
    update_reason_kind  VARCHAR(250),
    finished_at  DATETIME,
    FOREIGN KEY (payer_id) REFERENCES assets_parts(id),
    FOREIGN KEY (endorser_original_id) REFERENCES assets_parts(id),
    FOREIGN KEY (participant_id) REFERENCES participants(id)
);
CREATE INDEX payer_id_idx ON assets_trade_bills(payer_id);
CREATE INDEX endorser_original_id_idx ON assets_trade_bills(endorser_original_id);
CREATE INDEX participant_id_idx ON assets_trade_bills(participant_id);


