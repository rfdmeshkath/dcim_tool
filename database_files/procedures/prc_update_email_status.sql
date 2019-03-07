CREATE OR REPLACE PROCEDURE prc_update_email_status
-- l at the beginning of a variable represents that its a local variable used within the function
(
    l_notification_id          IN NUMBER
)
IS
BEGIN
    UPDATE
        notification_status
    SET
        email = 1
    WHERE
        notification_id = l_notification_id;
    COMMIT;

EXCEPTION
WHEN OTHERS THEN
    ROLLBACK;
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;