CREATE OR REPLACE PROCEDURE prc_resolve_alert
-- l at the beginning of a variable represents that its a local variable used within the function
(
    l_dashboard_id          IN VARCHAR2,
    l_resolved_comment      IN VARCHAR2,
    l_resolved_datetime     IN VARCHAR2,
    l_resolved_by           IN VARCHAR2
)
IS
BEGIN
    UPDATE
        dashboard_alert
    SET
        resolved_comment    = l_resolved_comment,
        resolved_datetime   = l_resolved_datetime,
        resolved_status     = 1,
        resolved_by         = l_resolved_by
    WHERE
        dashboard_id = l_dashboard_id;
    COMMIT;

EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;
/
