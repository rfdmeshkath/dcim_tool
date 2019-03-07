CREATE OR REPLACE PROCEDURE prc_insert_dashboard_alert
-- l at the beginning of a variable represents that its a local variable used within the function
(
    l_device_name         IN VARCHAR2,
    l_alert_code          IN VARCHAR2,
    l_severity            IN VARCHAR2,
    l_alert_details       IN VARCHAR2,
    l_occurred_datetime   IN VARCHAR2
)
IS
    alert_checker         NUMBER;
    l_dashboard_id        NUMBER;

BEGIN
    dbms_output.put_line('running fnc_check_if_alert_exists......');
    alert_checker := fnc_check_if_alert_exists(l_device_name, l_alert_code);

    dbms_output.put_line('checking function - fnc_check_if_alert_exists - output');
    IF alert_checker = 0 THEN

        dbms_output.put_line('performing insert......');
        INSERT INTO dashboard_alert
        (
            device_name,
            alert_code,
            severity,
            alert_details,
            occurred_datetime,
            resolved_status
        )
        VALUES
        (
            l_device_name,
            l_alert_code,
            l_severity,
            l_alert_details,
            l_occurred_datetime,
            0
        );

    dbms_output.put_line('running fnc_check_dashboard_id');
    l_dashboard_id  := fnc_check_dashboard_id(l_device_name, l_alert_code);

    INSERT INTO notification_status
    (
        notification_id,
        text_message,
        email
    )
    VALUES
    (
        l_dashboard_id,
        0,
        0
    );

    dbms_output.put_line('Insert successfull. commiting');
    COMMIT;
    END IF;

EXCEPTION
WHEN OTHERS THEN
    ROLLBACK;
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;