DROP TABLE port_error;
CREATE TABLE port_error
(
    port_error_id      NUMBER        NOT NULL,
    e_device_id        NUMBER        NOT NULL,
    port_name          VARCHAR2(30), 
    input_error        NUMBER,
    crc_error          NUMBER,
    frame_error        NUMBER,
    overrun_error      NUMBER,
    ignored_error      NUMBER,
    updated_datetime   DATE          NOT NULL
);

ALTER TABLE port_error
ADD CONSTRAINT pk_port_error_id PRIMARY KEY (port_error_id);

ALTER TABLE port_error
ADD CONSTRAINT fk_e_device_id
FOREIGN KEY (e_device_id) REFERENCES device(device_id);

DROP SEQUENCE port_error_seq;
CREATE SEQUENCE port_error_seq START WITH 1;

DROP TRIGGER port_error_trigger;
CREATE OR REPLACE TRIGGER port_error_trigger
BEFORE INSERT ON port_error
FOR EACH ROW

BEGIN
  SELECT port_error_seq.NEXTVAL
  INTO   :new.port_error_id
  FROM   dual;
END;
/