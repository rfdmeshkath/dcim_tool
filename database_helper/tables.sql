CREATE TABLE connections
(
    conn_id           NUMBER(10)    NOT NULL,
    local_device VARCHAR2(50),
    local_port VARCHAR2(50),
    remote_device VARCHAR2(50),
    remote_port VARCHAR2(50),
    collection_date VARCHAR2(50),
    collection_time VARCHAR2(50)
);

ALTER TABLE connections ADD
(
    CONSTRAINT conn_pk PRIMARY KEY (conn_id)
);

DROP SEQUENCE conn_seq;
CREATE SEQUENCE conn_seq START WITH 1;

DROP TRIGGER conn_trigger;
CREATE OR REPLACE TRIGGER conn_trigger
BEFORE INSERT ON connections
FOR EACH ROW

BEGIN
  SELECT conn_seq.NEXTVAL
  INTO   :new.conn_id
  FROM   dual;
END;
/