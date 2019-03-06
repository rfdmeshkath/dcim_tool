
DROP TABLE manual_connection;
CREATE TABLE manual_connection (
    mc_id                     NUMBER(10)    NOT NULL,
    mc_local_device_id        NUMBER(10)    NOT NULL,
    mc_local_port             VARCHAR2(20)  NOT NULL,
    mc_remote_device_id       NUMBER(10)    NOT NULL,
    mc_remote_port            VARCHAR2(20)  NOT NULL,
    mc_interconnect_1         VARCHAR2(20)
    mc_interconnect_2         VARCHAR2(20)
    mc_is_active              NUMBER(1)     NOT NULL

);


ALTER TABLE manual_connection
ADD CONSTRAINT fk_mc_local_device_id
FOREIGN KEY (mc_local_device_id) REFERENCES device(device_id);

ALTER TABLE manual_connection
ADD CONSTRAINT fk_mc_remote_device_id
FOREIGN KEY (mc_remote_device_id) REFERENCES device(device_id);


DROP SEQUENCE manual_connection_seq;
CREATE SEQUENCE manual_connection_seq START WITH 1;

DROP TRIGGER manual_connection_trigger;
CREATE OR REPLACE TRIGGER manual_connection_trigger
BEFORE INSERT ON manual_connection
FOR EACH ROW

BEGIN
  SELECT manual_connection_seq.NEXTVAL
  INTO   :new.mc_id
  FROM   dual;
END;
/