create or replace PROCEDURE prc_insert_device
-- l at the beginning of a variable represents that its a local variable used within the function
(
    l_device_name IN VARCHAR2
)
IS
BEGIN
    INSERT INTO device
    (
        device_name
    )
    VALUES
    (
        l_device_name
    );
    COMMIT;

EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;