CREATE OR REPLACE PROCEDURE prc_delete_manual_connection
(
    p_connection_id            IN NUMBER
)
IS
BEGIN
    dbms_output.put_line('deactivating connection......');
    UPDATE
        manual_connection
    SET
        mc_is_active = 0
    WHERE
        mc_id = p_connection_id;

    dbms_output.put_line('delete successfull. commiting.....');
    COMMIT;
EXCEPTION
WHEN OTHERS THEN
    ROLLBACK;
   raise_application_error(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;