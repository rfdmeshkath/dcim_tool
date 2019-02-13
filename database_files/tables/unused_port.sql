DROP TABLE unused_port;
CREATE TABLE unused_port
(
    unused_port_id      NUMBER     NOT NULL,
    p_device_id         NUMBER     NOT NULL,
    port_name           VARCHAR2(30),
    updated_datetime    DATE       NOT NULL
);

ALTER TABLE unused_port
ADD CONSTRAINT pk_unused_port_id PRIMARY KEY (unused_port_id);

ALTER TABLE unused_port
ADD CONSTRAINT fk_p_device_id
FOREIGN KEY (p_device_id) REFERENCES device(device_id);

DROP SEQUENCE unused_port_seq;
CREATE SEQUENCE unused_port_seq START WITH 1;

DROP TRIGGER unused_port_trigger;
CREATE OR REPLACE TRIGGER unused_port_trigger
BEFORE INSERT ON unused_port
FOR EACH ROW

BEGIN
  SELECT unused_port_seq.NEXTVAL
  INTO   :new.unused_port_id
  FROM   dual;
END;
/