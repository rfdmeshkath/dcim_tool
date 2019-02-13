DROP TABLE memory_history;
CREATE TABLE memory_history
(
    memory_history_id      NUMBER    NOT NULL,
    m_device_id            NUMBER    NOT NULL,
    ram_usage              NUMBER,
    cpu_usage              NUMBER,
    updated_datetime       DATE      NOT NULL
);

ALTER TABLE memory_history
ADD CONSTRAINT pk_memory_history PRIMARY KEY (memory_history_id);

ALTER TABLE memory_history
ADD CONSTRAINT fk_m_device_id
FOREIGN KEY (m_device_id) REFERENCES device(device_id);

DROP SEQUENCE memory_history_seq;
CREATE SEQUENCE memory_history_seq START WITH 1;

DROP TRIGGER memory_history_trigger;
CREATE OR REPLACE TRIGGER memory_history_trigger
BEFORE INSERT ON memory_history
FOR EACH ROW

BEGIN
  SELECT memory_history_seq.NEXTVAL
  INTO   :new.memory_history_id
  FROM   dual;
END;
/
