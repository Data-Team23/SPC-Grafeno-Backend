CREATE TABLE pm_masters (
    id_masters VARCHAR PRIMARY KEY,
    kind_masters  VARCHAR(250),
    name_masters  VARCHAR(250),
    document_masters  VARCHAR(250),
    email_primary_masters  VARCHAR(250),
    email_secondary_masters  VARCHAR(250),
    deleted_at DATE,
    created_at DATE,
    updated_at DATE
);

CREATE TABLE as_parts (
    id_as_parts VARCHAR PRIMARY KEY,
    name_parts  VARCHAR(250),
    parts_document_number  VARCHAR(250),
    ct_email  VARCHAR(250),
    ct_phone  VARCHAR(250),
    deleted_at DATETIME,
    created_at DATETIME,
    updated_at DATETIME,
    parts_type  VARCHAR(250)
);

CREATE TABLE pt_participants (
    id_participants VARCHAR(250) PRIMARY KEY,
    name_participants VARCHAR(250),
    participant_state  VARCHAR(250),
    pt_ct_phone_number  VARCHAR(250),
    pt_document_number  VARCHAR(250),
    company_name  VARCHAR(250),
    participants_kind  VARCHAR(250),
    id_masters  VARCHAR(250),
    FOREIGN KEY (id_masters) REFERENCES pm_masters(id_masters)
);
CREATE INDEX pm_masters_id_idx ON pt_participants(id_masters);


CREATE TABLE pt_third_parties (
    id_third_parties VARCHAR(250) PRIMARY KEY,
    id_participants  VARCHAR(250),
    created_at  DATETIME,
    updated_at DATETIME,
    third_parties_state  VARCHAR(250),
    approved_at DATETIME,
    rejected_at DATETIME,
    FOREIGN KEY (id_participants) REFERENCES pt_participants(id_participants)
);
CREATE INDEX pt_participant_id_idx ON pt_third_parties(id_participants);


CREATE TABLE proxy_third_parties_participants (
    id_third_parties  VARCHAR(250),
    id_participants  VARCHAR(250),
    PRIMARY KEY (id_third_parties, id_participants),
    FOREIGN KEY (id_third_parties) REFERENCES pt_third_parties(id_third_parties),
    FOREIGN KEY (id_participants) REFERENCES pt_participants(id_participants)
);
create index third_party_id_idx on proxy_third_parties_participants(id_third_parties);
create index pt_participant_id_idx on proxy_third_parties_participants(id_participants);

CREATE TABLE as_bills (
    id_bills VARCHAR(250) PRIMARY KEY,
    due_date DATETIME,
    bills_nfe_number  VARCHAR(250),
    bills_nfe_series  VARCHAR(250),
    bills_kind  VARCHAR(250),
    bills_state  VARCHAR(250),
    payer_id  VARCHAR(250),
    endorser_original_id  VARCHAR(250),
    new_due_date DATETIME, 
    participant_id  VARCHAR(250),
    ballast_kind  VARCHAR(250),
    invoice_number  VARCHAR(250),
    payment_place  VARCHAR(250),
    update_reason_kind  VARCHAR(250),
    finished_at  DATETIME,
    FOREIGN KEY (payer_id) REFERENCES as_parts(id_as_parts),
    FOREIGN KEY (endorser_original_id) REFERENCES as_parts(id_as_parts),
    FOREIGN KEY (participant_id) REFERENCES pt_participants(id_participants)
);
CREATE INDEX payer_id_idx ON as_bills(payer_id);
CREATE INDEX endorser_original_id_idx ON as_bills(endorser_original_id);
CREATE INDEX participant_id_idx ON as_bills(id_participants);


