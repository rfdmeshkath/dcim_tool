DROP TABLE founded_error;
CREATE TABLE founded_error
(
    error_id               NUMBER         NOT NULL,
    err_device_id          NUMBER         NOT NULL,
    error_code             VARCHAR2(50)   NOT NULL,
    error_description      VARCHAR2(200)  NOT NULL,
    aknowlwdge_status      NUMBER         NOT NULL
);

ALTER TABLE founded_error
ADD CONSTRAINT pk_error_id PRIMARY KEY (error_id);

ALTER TABLE founded_error
ADD CONSTRAINT fk_err_device_id
FOREIGN KEY (err_device_id) REFERENCES device(device_id);

DROP SEQUENCE founded_error;
CREATE SEQUENCE founded_error_seq START WITH 1;

DROP TRIGGER founded_error_trigger;
CREATE OR REPLACE TRIGGER founded_error_trigger
BEFORE INSERT ON founded_error
FOR EACH ROW

BEGIN
  SELECT founded_error_seq.NEXTVAL
  INTO   :new.error_id
  FROM   dual;
END;
/