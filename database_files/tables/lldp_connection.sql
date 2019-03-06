ALTER SESSION set NLS_DATE_FORMAT = 'DD-MM-YYYY HH24:MI:SS';

DROP TABLE lldp_connection;
CREATE TABLE lldp_connection (
    lldp_connection_id     NUMBER(10)    NOT NULL,
    local_device_id        NUMBER(10)    NOT NULL,
    local_port             VARCHAR2(20)  NOT NULL,
    remote_device_id       NUMBER(10)    NOT NULL,
    remote_port            VARCHAR2(20)  NOT NULL,
    updated_datetime       DATE          NOT NULL

);


ALTER TABLE lldp_connection
ADD CONSTRAINT fk_local_device_id
FOREIGN KEY (local_device_id) REFERENCES device(device_id);

ALTER TABLE lldp_connection
ADD CONSTRAINT fk_remote_device_id
FOREIGN KEY (remote_device_id) REFERENCES device(device_id);


DROP SEQUENCE lldp_connection_seq;
CREATE SEQUENCE lldp_connection_seq START WITH 1;

DROP TRIGGER lldp_connection_trigger;
CREATE OR REPLACE TRIGGER lldp_connection_trigger
BEFORE INSERT ON lldp_connection
FOR EACH ROW

BEGIN
  SELECT lldp_connection_seq.NEXTVAL
  INTO   :new.lldp_connection_id
  FROM   dual;
END;
/
