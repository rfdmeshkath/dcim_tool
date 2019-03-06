DROP TABLE dashboard_alert;
CREATE TABLE dashboard_alert
(
    dashboard_id        NUMBER             NOT NULL,
    device_name         VARCHAR2(50),
    alert_code          VARCHAR2(50)       NOT NULL,
    severity            VARCHAR2(15)       DEFAULT 'danger',
    alert_details       VARCHAR2(50),
    occurred_datetime    DATE               NOT NULL,
    resolved_comment    VARCHAR2(500),
    resolved_datetime   DATE,
    resolved_status     NUMBER             DEFAULT 0,
    resolved_by         VARCHAR2(50)
);

ALTER TABLE dashboard_alert
ADD CONSTRAINT pk_dashboard_id PRIMARY KEY (dashboard_id);

DROP SEQUENCE dashboard_alert_seq;
CREATE SEQUENCE dashboard_alert_seq START WITH 1;

DROP TRIGGER dashboard_alert_trigger;
CREATE OR REPLACE TRIGGER dashboard_alert_trigger
BEFORE INSERT ON dashboard_alert
FOR EACH ROW

BEGIN
  SELECT dashboard_alert_seq.NEXTVAL
  INTO   :new.dashboard_id
  FROM   dual;
END;
/