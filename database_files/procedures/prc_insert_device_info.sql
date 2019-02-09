create or replace PROCEDURE prc_insert_device_info
-- p at the beginning of a variable represents those variables which are passed to the function
-- l at the beginning of a variable represents that its a local variable used within the function
(
    p_device_name        IN VARCHAR2,
    p_system_name        IN VARCHAR2,
    p_os_description     IN VARCHAR2,
    p_up_time            IN NUMBER,
    p_total_ram          IN NUMBER
)
IS
    l_device_checker     NUMBER;

BEGIN
    dbms_output.put_line('running fnc_check_if_device_exists......');
    l_device_checker  := fnc_check_if_device_exists(p_device_name);

    dbms_output.put_line('checking function - fnc_check_if_device_exists - output');
    IF l_device_checker = 0 THEN

        dbms_output.put_line('performing insert......');
        INSERT INTO device
        (
            device_name,
            system_name,
            os_description,
            up_time,
            total_ram
        )
        VALUES
        (
            p_device_name,
            p_system_name,
            p_os_description,
            p_up_time,
            p_total_ram
        );
    ELSE
        dbms_output.put_line('performing update......');
        UPDATE device SET
            system_name      = p_system_name,
            os_description   = p_os_description,
            up_time          = p_up_time,
            total_ram        = p_total_ram
        WHERE device_name    = p_device_name;

    END IF;

    dbms_output.put_line('Insert/Update successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;