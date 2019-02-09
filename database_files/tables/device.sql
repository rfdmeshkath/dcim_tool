DROP TABLE device;
CREATE TABLE device
(
    device_id         NUMBER(10)    NOT NULL,
    device_name       VARCHAR2(50)  NOT NULL
);

ALTER TABLE device
ADD CONSTRAINT pk_device PRIMARY KEY (device_id);

ALTER TABLE device
ADD CONSTRAINT uniq_device_name UNIQUE (device_name);

DROP SEQUENCE device_seq;
CREATE SEQUENCE device_seq START WITH 1;

DROP TRIGGER device_trigger;
CREATE OR REPLACE TRIGGER device_trigger
BEFORE INSERT ON device
FOR EACH ROW

BEGIN
  SELECT device_seq.NEXTVAL
  INTO   :new.device_id
  FROM   dual;
END;
/


ALTER TABLE device ADD
(
    system_name       VARCHAR2(50),
    os_description    VARCHAR2(200),
    up_time           NUMBER,
    total_ram         NUMBER
);