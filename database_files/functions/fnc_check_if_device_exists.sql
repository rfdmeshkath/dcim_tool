create or replace FUNCTION fnc_check_if_device_exists (l_device_name in VARCHAR2)
   -- returns 1 if passed "device name" exists in device-table else returns 0
   RETURN NUMBER
   IS does_exists NUMBER;
   BEGIN
     SELECT
        COUNT(*)
    INTO does_exists
     FROM
        device
    WHERE
        device_name = l_device_name;
      RETURN(does_exists);
    END;
