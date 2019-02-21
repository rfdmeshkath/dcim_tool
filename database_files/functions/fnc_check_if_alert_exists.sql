create or replace FUNCTION fnc_check_if_alert_exists 
(
    l_device_name  IN VARCHAR2,
    l_alert_code   IN VARCHAR2
)
   -- returns 1 if passed "error code" for the passed "device_name" exists in alert-table else returns 0
   RETURN NUMBER
   IS does_exists NUMBER;
   BEGIN
     SELECT
        COUNT(*)
    INTO does_exists
     FROM
        dashboard_alert
    WHERE
        device_name = l_device_name
    AND
        alert_code = l_alert_code
    AND
        resolved_status = 0;

    RETURN(does_exists);
END;