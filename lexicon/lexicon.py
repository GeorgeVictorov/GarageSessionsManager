MESSAGES: dict[str, str] = {
    '/start': '<b>Welcome to Garage Sessions Manager.</b>'
              '\n\nPress /new to book a new session.'
              '\n\nPress /upcoming to view upcoming sessions.',
    '/upcoming': '<b>Here are your upcoming sessions:</b>\n\n'
                 '{}',
    '/no_upcoming': "<b>You have no upcoming sessions.</b>",
    '/admin_no_upcoming': "<b>There are no upcoming sessions.</b>",
    '/admin': '<b>Welcome, {}!</b>'
              '\n\nPress /admin_upcoming to view upcoming sessions.'
              '\n\nPress /admin_cancel to cancel any session.'
              '\n\nPress /admin_payment to approve payment.'
              '\n\nPress /admin_sessions to get all session history.',
    '/admin_upcoming': '<b>Here are all upcoming sessions:</b>\n\n'
                       '{}',
    '/cancel': '<b>To cancel your booked sessions, simply click on it:</b>',
    '/admin_cancel': '<b>To cancel a sessions, simply click on it:</b>',
    '/cancel_success': 'Your session has been successfully canceled.',
    '/admin_payment': '<b>To confirm session payment, simply click on it:</b>',
    '/admin_no_payment': '<b>All sessions have been paid for.</b>',
    '/admin_sessions': '<b>All session history (CSV file):</b>',
    '/help': '<b>Welcome to Garage Sessions Manager.</b>'
             '\n\n<i>Garage Sessions Manager is a tool that facilitates booking sessions.'
             '\n\nThe goal is to provide you with a seamless experience of managing your sessions.</i>'
             '\n\n<b>There are 3 types of sessions available:</b>'
             '\n\n- Drummer: for solo drummers.'
             '\n- Small band: for bands consisting of two people.'
             '\n- Norm Band: for three or more people.'
             '\n\nPress /start to begin.'
             '\n\nPress /new to book a new session.'
             '\n\nPress /upcoming to view sessions.'
             '\n\nPress /cancel to cancel a session.'
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Welcome home boi.',
    '/new': 'Book new session.',
    '/upcoming': 'View booked sessions.',
    '/cancel': 'Abandon ship.',
    '/help': 'Mayday, mayday. Man overboard again.'
}

INFO: dict[str, str] = {
    'cancel': '<b>You have canceled your booking.</b>'
              '\n\nPress /new to book a new session.',
    'session': "New session for <b>{}</b>"
               "\n\nSession date: <b>{}</b>"
               "\nDuration: <b>{} hours</b>"
               "\nSession type: <b>{}</b>",
    'session_booked': "You have booked a new session for <b>{}</b>"
                      "\n\nSession date: <b>{}</b>"
                      "\nDuration: <b>{} hours</b>"
                      "\nSession type: <b>{}</b>"
                      "\n\n<b>Thank you for choosing us!</b>",
    'session_admin_info': "New session booked for <b>{}</b>"
                          "\n\nSession date: <b>{}</b>"
                          "\nDuration: <b>{} hours</b>"
                          "\nSession type: <b>{}</b>",
    'session_admin_cancel': "Session canceled for <b>{}</b>"
                            "\n\nSession date: <b>{}</b>"
                            "\nDuration: <b>{} hours</b>"
                            "\nSession type: <b>{}</b>",
    'session_admin_payment': "Payment confirmed for <b>{}</b> session"
                             "\n\nSession date: <b>{}</b>"
                             "\nDuration: <b>{} hours</b>"
                             "\nSession type: <b>{}</b>",
    'close': "<b>All in all, you're just another brick in the wall.</b>"
             "\n\nPress /start to begin again."
}
