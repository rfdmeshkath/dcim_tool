create or replace FUNCTION fnc_check_device_id (l_device_name in VARCHAR2)
   -- l at the begining of a variable represents that its a local variable use within the function
   -- returns the device_id of a device_name
   RETURN NUMBER
   IS l_device_id NUMBER;
   BEGIN
     SELECT
        device_id
    INTO l_device_id
     FROM
        device
    WHERE
        device_name = l_device_name;
      RETURN(l_device_id);
    END;
