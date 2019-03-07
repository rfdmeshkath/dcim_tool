DROP TABLE notification_status;
CREATE TABLE notification_status(
    notification_id     NUMBER(10)    NOT NULL,
    text_message        NUMBER(1)     NOT NULL,
    email               NUMBER(1)     NOT NULL

);


ALTER TABLE notification_status
ADD CONSTRAINT fk_notification_id
FOREIGN KEY (notification_id) REFERENCES dashboard_alert(dashboard_id);