select_lldp_connection = \
"""
SELECT 
    x.device_name   local_device, 
    a.local_port    local_port, 
    y.device_name   remote_device,  
    a.remote_port   remote_port
FROM 
    device x, 
    device y, 
    lldp_connection a
WHERE 
    a.local_device_id = x.device_id 
    and  
    a.remote_device_id = y.device_id
"""


a ='''SELECT 
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

