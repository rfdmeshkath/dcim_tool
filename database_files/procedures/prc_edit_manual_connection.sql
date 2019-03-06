CREATE OR REPLACE PROCEDURE prc_edit_manual_connection
-- l at the beginning of a variable represents that these variables were passed to this procedure
-- v at the beginning of a variable represents that these variables are created within this function
(
    p_connection_id            IN NUMBER,
    p_local_device             IN VARCHAR2,
    p_local_port               IN VARCHAR2,
    p_remote_device            IN VARCHAR2,
    p_remote_port              IN VARCHAR2,
    p_interconnect_1           IN VARCHAR2,
    p_interconnect_2           IN VARCHAR2
)
IS
    v_local_port_checker       NUMBER;
    v_remote_port_checker      NUMBER;
    v_local_device_checker     NUMBER;
    v_remote_device_checker    NUMBER;
    v_local_device_id          NUMBER;
    v_remote_device_id         NUMBER;

    ex_l_port_active           EXCEPTION;
    ex_r_port_active           EXCEPTION;
BEGIN
    DBMS_OUTPUT.PUT_LINE('connection  id: '  || p_connection_id);
    v_local_port_checker  := fnc_check_if_l_port_active(p_local_device, p_local_port);
    v_remote_port_checker := fnc_check_if_r_port_active(p_remote_device, p_remote_port);

    IF v_local_port_checker > 0 THEN
        RAISE ex_l_port_active;
    END IF;

    IF v_remote_port_checker > 0 THEN
        RAISE ex_r_port_active;
    END IF;

    dbms_output.put_line('running fnc_check_if_device_exists......');
    v_local_device_checker  := fnc_check_if_device_exists(p_local_device);
    v_remote_device_checker := fnc_check_if_device_exists(p_remote_device);
    DBMS_OUTPUT.PUT_LINE('local device checker value : '  || v_local_device_checker);
    DBMS_OUTPUT.PUT_LINE('remote device checker value : '  || v_remote_device_checker);

    dbms_output.put_line('checking function - fnc_check_if_device_exists - output');
    IF v_local_device_checker = 0 THEN
        prc_insert_device(p_local_device);
    END IF;

    IF v_remote_device_checker = 0 THEN
        prc_insert_device(p_remote_device);
    END IF;

    dbms_output.put_line('checking devices id');
    v_local_device_id   := fnc_check_device_id(p_local_device);
    v_remote_device_id  := fnc_check_device_id(p_remote_device);
    DBMS_OUTPUT.PUT_LINE('local device id : '  || v_local_device_id);
    DBMS_OUTPUT.PUT_LINE('remote device id : '  || v_remote_device_id);

    dbms_output.put_line('performing update......');
    UPDATE
        manual_connection
    SET
        mc_local_device_id         = v_local_device_id,
        mc_local_port              = p_local_port,
        mc_remote_device_id        = v_remote_device_id,
        mc_remote_port             = p_remote_port,
        mc_interconnect_1          = p_interconnect_1,
        mc_interconnect_2          = p_interconnect_2
    WHERE
        mc_id = p_connection_id;

    dbms_output.put_line('update successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN ex_l_port_active THEN
    ROLLBACK;
    raise_application_error(-20021,'Local Port is active - '||SQLCODE||' -ERROR- '||SQLERRM);
WHEN ex_r_port_active THEN
    ROLLBACK;
    raise_application_error(-20022,'Remote Port is active - '||SQLCODE||' -ERROR- '||SQLERRM);
WHEN OTHERS THEN
    ROLLBACK;
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;