create or replace FUNCTION fnc_check_if_r_port_active
(
    l_device_name   IN VARCHAR2,
    l_port_name     IN VARCHAR2
)
-- returns 1 if passed "port" of the given "device" exists in manual-connection-table else returns 0
RETURN NUMBER
   IS does_exists NUMBER;
BEGIN
    SELECT 
        COUNT(*)
    INTO does_exists
    FROM 
        device             x, 
        manual_connection  a
    WHERE 
        a.mc_remote_device_id = x.device_id
    AND
        device_name = l_device_name
    AND
        mc_remote_port = l_port_name
    AND
        mc_is_active = 1;
RETURN(does_exists);
END;