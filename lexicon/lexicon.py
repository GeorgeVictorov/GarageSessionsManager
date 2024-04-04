MESSAGES: dict[str, str] = {
    '/start': '<b>Welcome to Garage Sessions Manager.</b>'
              '\n\nPress /new to book a new session.'
              '\n\nPress /upcoming to get sessions info.',
    '/upcoming': '<b>Here are your upcoming sessions:</b>\n\n'
                 '{}'
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
                          "\nSession type: <b>{}</b>"
}
