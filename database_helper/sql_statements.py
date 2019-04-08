def select_lldp_connections(device_name):
    select_statement = '''
    SELECT 
        x.device_name       local_device, 
        a.local_port        local_port, 
        y.device_name       remote_device,  
        a.remote_port       remote_port,
        a.updated_datetime  updated_date_time
    FROM 
        device x, 
        device y, 
        lldp_connection a
    WHERE 
        a.local_device_id = x.device_id 
        AND  
        a.remote_device_id = y.device_id
        AND
        x.device_name = \'{}\'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM lldp_connection)
    '''.format(device_name)
    return select_statement


def select_memory_usage(device_name, row_num=16):
    select_statement = '''
    SELECT 
        device_name, 
        ram_usage,
        cpu_usage,
        date_time
    FROM 
    (
        SELECT 
            x.device_name        device_name, 
            a.ram_usage          ram_usage,
            a.cpu_usage          cpu_usage,
            a.updated_datetime   date_time
        FROM 
            device x, 
            memory_history a
        
        WHERE 
            a.m_device_id = x.device_id
            AND x.device_name = '{}'
    )
    WHERE
    ROWNUM < {} 
    ORDER BY date_time DESC
    '''.format(device_name, row_num)
    return select_statement


def select_device_info(device_name):
    select_statement = '''
    SELECT 
        system_name,
        os_description,
        up_time,
        total_ram
    FROM
    device
    WHERE device_name = \'{}\'
    '''.format(device_name)
    return select_statement


def select_unused_ports(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name, 
        a.port_name          port_name,
        a.updated_datetime   date_time
    FROM 
        device x, 
        unused_port a
    
    WHERE 
        a.p_device_id = x.device_id
        AND 
        x.device_name = '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM unused_port)
        '''.format(device_name)
    return select_statement


def select_port_error(device_name):
    select_statement = '''
    SELECT 
        a.port_name          port_name,
        a.input_error        input_error,
        a.crc_error          crc_error,
        a.frame_error        frame_error,
        a.overrun_error      overrun_error,
        a.ignored_error      ignored_error,
        a.updated_datetime   date_time
    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name = '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
    '''.format(device_name)
    return select_statement


def select_input_error(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name,
        a.port_name          port_name,
        a.input_error        input_error,
        a.updated_datetime   date_time

    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name like '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
        AND
        input_error > 0 
        '''.format(device_name)
    return select_statement


def select_crc_error(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name,
        a.port_name          port_name,
        a.crc_error          crc_error,
        a.updated_datetime   date_time

    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name like '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
        AND
        crc_error > 0
        '''.format(device_name)
    return select_statement


def select_frame_error(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name,
        a.port_name          port_name,
        a.frame_error        frame_error,
        a.updated_datetime   date_time

    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name like '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
        AND
        frame_error > 0
        '''.format(device_name)
    return select_statement


def select_overrun_error(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name,
        a.port_name          port_name,
        a.overrun_error      overrun_error,
        a.updated_datetime   date_time

    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name like '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
        AND
        overrun_error > 0
        '''.format(device_name)
    return select_statement


def select_ignored_error(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name,
        a.port_name          port_name,
        a.ignored_error      ignored_error,
        a.updated_datetime   date_time

    FROM 
        device x, 
        port_error a
    WHERE 
        a.e_device_id = x.device_id
        AND 
        x.device_name like 'R1'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM port_error)
        AND
        ignored_error > 0
        '''.format(device_name)
    return select_statement


def select_total_alerts():
    select_statement = '''
    SELECT 
        COUNT(*) 
    FROM 
        dashboard_alert
    WHERE
        resolved_status = 0
    '''
    return select_statement


def select_all_alerts_info():
    select_statement = '''
    SELECT 
        dashboard_id,
        device_name,
        severity,
        alert_details,
        occurred_datetime
    FROM 
        dashboard_alert
    WHERE 
        resolved_status = 0
    '''
    return select_statement


def select_alert_info(dashboard_id):
    select_statement = '''
    SELECT 
        dashboard_id,
        device_name, 
        severity, 
        alert_details, 
        occurred_datetime 
    FROM
        dashboard_alert
    WHERE
        dashboard_id = {}
    '''.format(dashboard_id)
    return select_statement


def select_all_connections(searched_item):
    select_satement = '''
    SELECT 
        a.mc_id                 connection_id, 
        x.device_name           local_device, 
        a.mc_local_port         local_port, 
        y.device_name           remote_device,  
        a.mc_remote_port        remote_port,
        a.mc_interconnect_1     interconnect_1,
        a.mc_interconnect_2     interconnect_2
    FROM 
        device x, 
        device y, 
        manual_connection a
    WHERE 
        a.mc_local_device_id = x.device_id 
        AND  
        a.mc_remote_device_id = y.device_id
        AND 
        a.mc_is_active = 1
        AND
        x.device_name LIKE '%{}%'
    '''.format(searched_item)
    return select_satement


def select_connection_for_edit(connection_id):
    select_statement = '''
    SELECT 
        a.mc_id                 connection_id, 
        x.device_name           local_device, 
        a.mc_local_port         local_port, 
        y.device_name           remote_device,  
        a.mc_remote_port        remote_port,
        a.mc_interconnect_1     interconnect_1,
        a.mc_interconnect_2     interconnect_2
    FROM 
        device x, 
        device y, 
        manual_connection a
    WHERE 
        a.mc_local_device_id = x.device_id 
        AND  
        a.mc_remote_device_id = y.device_id
        AND
        a.mc_id = '{}'
        '''.format(connection_id)
    return select_statement


def select_notification_status(device_name, alert_code):
    select_statement = '''
    SELECT
        notification_id,
        text_message,
        email
    FROM 
        notification_status x,
        dashboard_alert     y
    WHERE
        x.notification_id = y.dashboard_id
        AND
        y.device_name = '{}'
        AND
        y.alert_code = '{}'
    '''.format(device_name, alert_code)
    return select_statement


def select_second_highest_date(device_name):
    select_statement = '''
    SELECT 
        MAX(updated_datetime) 
    FROM 
        lldp_connection
    WHERE 
        local_device_id = (SELECT fnc_check_device_id('{}') from DUAL)
        AND
        updated_datetime NOT IN 
        (
            SELECT 
                MAX(updated_datetime) 
            FROM 
                lldp_connection
            WHERE 
                local_device_id = (SELECT fnc_check_device_id('{}') from DUAL)
        )
    '''.format(device_name, device_name)
    return select_statement


def select_disconnected_connections(device_name, datetime):
    select_statement = '''
    (SELECT 
        x.device_name       local_device, 
        a.local_port        local_port, 
        y.device_name       remote_device,  
        a.remote_port       remote_port
    FROM 
        device x, 
        device y, 
        lldp_connection a
    WHERE 
        a.local_device_id = x.device_id 
        AND  
        a.remote_device_id = y.device_id
        AND
        x.device_name = '{}'
        AND
        a.updated_datetime = '{}')
    MINUS
    (SELECT 
            x.device_name       local_device, 
            a.local_port        local_port, 
            y.device_name       remote_device,  
            a.remote_port       remote_port
        FROM 
            device x, 
            device y, 
            lldp_connection a
        WHERE 
            a.local_device_id = x.device_id 
            AND  
            a.remote_device_id = y.device_id
            AND
            x.device_name = '{}'
            AND
            a.updated_datetime = (SELECT MAX(updated_datetime) FROM lldp_connection))
    '''.format(device_name, datetime, device_name)
    return select_statement


def select_latest_memory_usage(device_name):
    select_statement = '''
    SELECT 
        x.device_name        device_name, 
        a.ram_usage          ram_usage,
        a.cpu_usage          cpu_usage,
        a.updated_datetime   date_time
    FROM 
        device            x, 
        memory_history    a
    
    WHERE 
        a.m_device_id = x.device_id
        AND 
        x.device_name = '{}'
        AND
        a.updated_datetime = (SELECT MAX(updated_datetime) FROM memory_history)
    '''.format(device_name)
    return select_statement


def select_resolved_dashboard_tickets(row_num=50):
    select_statement ='''
    SELECT 
        device_name,
        severity,
        alert_details,
        occurred_datetime,
        resolved_comment,
        resolved_datetime,
        resolved_by
    FROM
        dashboard_alert
    WHERE
        resolved_status = 1
        AND
        ROWNUM < {}
    '''.format(row_num)
    return select_statement


def select_searched_tickets(searched_item):
    select_statement = '''
    SELECT 
    device_name,
    severity,
    alert_details,
    occurred_datetime,
    resolved_comment,
    resolved_datetime,
    resolved_by
FROM
    dashboard_alert
WHERE
    resolved_status = 1
    AND
    (
    device_name LIKE \'%{dn}%\'
    OR
    alert_details LIKE \'%{ad}%\'
    OR
    resolved_by LIKE \'%{rb}%\'
    )'''.format(dn=searched_item, ad=searched_item,rb=searched_item)
    return select_statement