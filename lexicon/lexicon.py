MESSAGES: dict[str, str] = {
    '/start': '<b>Welcome to Garage Sessions Manager.</b>'
              '\n\nPress /new to book a new session.'
              '\n\nPress /upcoming to view upcoming sessions.',
    '/upcoming': '<b>Here are your upcoming sessions:</b>\n\n'
                 '{}',
    '/a_upcoming': '<b>Here are all upcoming sessions:</b>\n\n'
                   '{}',
    '/cancel': '<b>To cancel your booked sessions, simply click on it:</b>',
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
             '\n\nPress /cancel to cancel a session.',
    '/admin': '<b>403 Forbidden</b>',
    '/admin_upcoming': '<b>403 Forbidden</b>',
    '/admin_cancel': '<b>403 Forbidden</b>',
    '/admin_payment': '<b>403 Forbidden</b>',
    '/admin_sessions': '<b>403 Forbidden</b>'
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Welcome home boi.',
    '/new': 'Book new session.',
    '/upcoming': 'View booked sessions.',
    '/cancel': 'Abandon ship.',
    '/help': 'Mayday, mayday. Man overboard again.'
}

INFO = {
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
    '/admin': '<b>Welcome, {}!</b>'
              '\n\nPress /admin_upcoming to view upcoming sessions.'
              '\n\nPress /admin_cancel to cancel any session.'
              '\n\nPress /admin_payment to approve payment.'
              '\n\nPress /admin_sessions to get all session history.'
}
