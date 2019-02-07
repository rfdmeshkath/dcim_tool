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
    lldp_connection.sql a 
WHERE 
    a.local_device_id = x.device_id 
    and  
    a.remote_device_id = y.device_id
"""


insert_device = """insert into device (device_name) values ('remote-device-2');"""

insert_lldp = \
"""
insert into lldp_connection.sql
(
    local_device_id,
    local_port,
    remote_device_id,
    remote_port,
    updated_datetime
)
values
(
    2,
    'eth3',
    3,
    'eth4',
    '24-09-2018 12:23:45'
);
"""