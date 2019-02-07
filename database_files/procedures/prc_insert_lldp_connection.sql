create or replace PROCEDURE prc_insert_lldp_connection
-- l at the beginning of a variable represents that its a local variable used within the function
(
    l_local_device        IN VARCHAR2,
    l_local_port          IN VARCHAR2,
    l_remote_device       IN VARCHAR2,
    l_remote_port         IN VARCHAR2,
    l_updated_datetime    IN VARCHAR2
)
IS
    l_local_device_checker     NUMBER;
    l_remote_device_checker    NUMBER;
    l_local_device_id          NUMBER;
    l_remote_device_id         NUMBER;

BEGIN
    dbms_output.put_line('running fnc_check_if_device_exists......');
    l_local_device_checker  := fnc_check_if_device_exists(l_local_device);
    l_remote_device_checker := fnc_check_if_device_exists(l_remote_device);

    dbms_output.put_line('checking function - fnc_check_if_device_exists - output');
    IF l_local_device_checker = 0 THEN
        prc_insert_device(l_local_device);
    END IF;

    IF l_remote_device_checker = 0 THEN
        prc_insert_device(l_remote_device);
    END IF;

    dbms_output.put_line('checking devices id');
    l_local_device_id   := fnc_check_device_id(l_local_device);
    l_remote_device_id  := fnc_check_device_id(l_remote_device);

    dbms_output.put_line('performing insert......');
    INSERT INTO lldp_connection
    (
        local_device_id,
        local_port,
        remote_device_id,
        remote_port,
        updated_datetime
    )
    VALUES
    (
        l_local_device_id,
        l_local_port,
        l_remote_device_id,
        l_remote_port,
        l_updated_datetime
    );
    dbms_output.put_line('Insert successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;

