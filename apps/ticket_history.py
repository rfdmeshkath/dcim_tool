from database_helper.query import execute_query
from database_helper.sql_statements import select_resolved_dashboard_tickets, select_searched_tickets


def get_recent_tickets():
    query = select_resolved_dashboard_tickets(50)
    resolved_tickets_df = execute_query(query)
    resolved_tickets_df.columns = ['Device Name', 'Severity', 'Alert Details', 'Occurred Datetime', 'Resolved Comment',
                                   'Resolved Datetime', 'Resolved By']
    return resolved_tickets_df


def get_searched_ticket(searched_item):
    query = select_searched_tickets(searched_item)
    tickets_info_df = execute_query(query)
    tickets_info_df.columns = ['Device Name', 'Severity', 'Alert Details', 'Occurred Datetime', 'Resolved Comment',
                               'Resolved Datetime', 'Resolved By']
    return tickets_info_df
