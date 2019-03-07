CREATE OR REPLACE FUNCTION fnc_check_dashboard_id
(
    p_device_name   IN VARCHAR2,
    p_alert_code    IN VARCHAR2
)
-- returns the dashboard id assigned to a dashboard alert
RETURN NUMBER
IS l_dashboard_id NUMBER;
BEGIN
 SELECT
    dashboard_id
INTO l_dashboard_id
 FROM
    dashboard_alert
WHERE
    device_name = p_device_name
    AND
    alert_code = p_alert_code;
  RETURN(l_dashboard_id);
END;