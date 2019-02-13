create or replace PROCEDURE prc_insert_port_error
-- p at the beginning of a variable represents those variables which are passed to the function
-- l at the beginning of a variable represents that its a local variable used within the function
(
    p_device_name        IN VARCHAR2,
    p_port_name          IN VARCHAR2,
    p_input_error        IN NUMBER,
    p_crc_error          IN NUMBER,
    p_frame_error        IN NUMBER,
    p_overrun_error      IN NUMBER,
    p_ignored_error      IN NUMBER,
    p_updated_datetime   IN DATE
)
IS
    l_device_checker     NUMBER;
    l_device_id          NUMBER;

BEGIN
    dbms_output.put_line('running fnc_check_if_device_exists......');
    l_device_checker  := fnc_check_if_device_exists(p_device_name);

    dbms_output.put_line('checking the output of the function - fnc_check_if_device_exists');
    IF l_device_checker = 0 THEN
        prc_insert_device(p_device_name);
    END IF;

    dbms_output.put_line('retrieving devices id');
    l_device_id   := fnc_check_device_id(p_device_name);

    dbms_output.put_line('performing insert......');
    INSERT INTO port_error
    (
        e_device_id,
        port_name,
        input_error,
        crc_error,
        frame_error,
        overrun_error,
        ignored_error,
        updated_datetime
    )
    VALUES
    (
        l_device_id,
        p_port_name,
        p_input_error,
        p_crc_error,
        p_frame_error,
        p_overrun_error,
        p_ignored_error,
        p_updated_datetime
    );
    dbms_output.put_line('Insert successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;