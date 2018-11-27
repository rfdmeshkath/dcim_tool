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

------------------------------------------------------------------------------------------------
CREATE TABLE device_status
(
    status_id           NUMBER(10)    NOT NULL,
    device_name         VARCHAR2(50),
    total_ram           NUMBER(5),
    currently_used      NUMBER(5),
    currently_free      NUMBER(5),
    cpu_usage           NUMBER(3),
    collection_date     VARCHAR2(50),
    collection_time     VARCHAR2(50)
);


ALTER TABLE device_status ADD
(
    CONSTRAINT status_pk PRIMARY KEY (status_id)
);

DROP SEQUENCE status_seq;
CREATE SEQUENCE status_seq START WITH 1;

DROP TRIGGER status_trigger;
CREATE OR REPLACE TRIGGER status_trigger
BEFORE INSERT ON device_status
FOR EACH ROW

BEGIN
  SELECT status_seq.NEXTVAL
  INTO   :new.status_id
  FROM   dual;
END;
/


insert into device_status
(
    device_name,
    total_ram,
    currently_used,
    currently_free,
    cpu_usage,
    collection_date,
    collection_time
)
values
(
    'r1',
     128,
     50,
     62,
     15,
    '12-23-1890',
    '13:08'
);



select * from device_status;