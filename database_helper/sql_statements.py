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


a = '''SELECT 
    x.device_name, 
    a.local_port
FROM 
    device x, 
    lldp_connection a
WHERE 
    a.local_device_id = x.device_id
    AND
    device_name='local-device-1'
    AND
    local_port='eth1';
'''
