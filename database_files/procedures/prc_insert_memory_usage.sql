create or replace PROCEDURE prc_insert_memory_usage
-- p at the beginning of a variable represents those variables which are passed to the function
-- l at the beginning of a variable represents that its a local variable used within the function
(
    p_device_name       IN VARCHAR2,
    p_ram_usage         IN NUMBER,
    p_cpu_usage         IN NUMBER,
    p_updated_datetime  IN DATE
)
IS
    l_device_checker     NUMBER;
    l_device_id          NUMBER;

BEGIN
    dbms_output.put_line('running fnc_check_if_device_exists......');
    l_device_checker  := fnc_check_if_device_exists(p_device_name);

    dbms_output.put_line('checking function - fnc_check_if_device_exists - output');
    IF l_device_checker = 0 THEN
        prc_insert_device(p_device_name);
    END IF;

    dbms_output.put_line('checking devices id');
    l_device_id   := fnc_check_device_id(p_device_name);

    dbms_output.put_line('performing insert......');
    INSERT INTO memory_history
    (
        m_device_id,
        ram_usage,
        cpu_usage,
        updated_datetime
    )
    VALUES
    (
        l_device_id,
        p_ram_usage,
        p_cpu_usage,
        p_updated_datetime
    );
    dbms_output.put_line('Insert successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN OTHERS THEN
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;
/