MESSAGES: dict[str, str] = {
    '/admin': '<b>Welcome, {}!</b>'
              '\n\nPress /admin_upcoming to view upcoming sessions.'
              '\n\nPress /admin_cancel to cancel any session.'
              '\n\nPress /admin_payment to approve payment.'
              '\n\nPress /admin_sessions to get all session history.'
              '\n\nPress /admin_price to view type prices.'
              '\n\nPress /update_price to update session type price.'
              '\n\nPress /admin_users to view all users.'
              '\n\nPress /ban_user to ban or unban the user.'
              '\n\nPress /send_message to send a message to all users.',
    '/admin_cancel': '<b>To cancel a sessions, simply click on it:</b>',
    '/admin_no_payment': '<b>All sessions have been paid for.</b>',
    '/admin_no_upcoming': "<b>There are no upcoming sessions.</b>",
    '/admin_payment': '<b>To confirm session payment, simply click on it:</b>',
    '/admin_sessions': '<b>All session history (CSV file):</b>',
    '/admin_update_price': "<b>Please provide the type ID and the new price in the following format:</b>\n\n"
                           "<i>/update_price type_id new_price</i>\n\n"
                           "For instance: /update_price 2 350\n\n"
                           "<b>Session types and their corresponding type IDs:</b>\n\n"
                           "- Drummer - type ID: 1\n"
                           "- Small band - type ID: 2\n"
                           "- Norm band - type ID: 3",
    '/admin_update_price_error': "Incorrect format. Please provide the type ID and the new price.",
    '/admin_upcoming': '<b>Here are all upcoming sessions:</b>\n\n'
                       '{}',
    '/ban_user': "<b>To ban or unban a user, please provide user_id and status:</b>\n\n"
                 "<i>/ban_user user_id status</i>\n\n"
                 "For instance: /ban_user 123456321 true\n\n"
                 "<b>User status:</b>\n\n"
                 "- Banned: true\n"
                 "- Unbanned: false",
    '/ban_user_error': "Incorrect format. Please provide user_id and status.",
    '/cancel': '<b>To cancel your booked sessions, simply click on it:</b>',
    '/cancel_success': 'Your session has been successfully canceled.',
    '/change_number': "<b>Please provide your new phone number in the following format:\n\n</b>"
                      "<i>/change_number new_number</i>\n\n"
                      "For example: /change_number +79261234455\n\n",
    '/change_number_error': "<b>Invalid phone number format.</b>\n\n"
                            "Please provide your phone number in the following format:\n\n"
                            "<i>/change_number new_number</i>\n\n"
                            "For example: /change_number +79261234455\n\n",
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
             '\n\nPress /change_number to change your phone number.',
    '/no_upcoming': "<b>You have no upcoming sessions.</b>",
    '/phone_number': "<b>Invalid phone number format.</b>\n\n"
                     "Please provide your phone number in the following format:\n\n"
                     "For example: <b>+79261234455</b>\n\n"
                     "<i>By providing your phone number, you consent to the processing of your personal data.</i>\n\n"
                     "Please ensure that your phone number is correctly formatted to proceed.",
    '/phone_success': "<b>Thank you for providing your phone number:</b>"
                      "\n\n<b>{}</b>\n\n"
                      "<i>By providing your phone number, you consent to the processing of your personal data.</i>\n\n"
                      "Press /start to begin.",
    '/registration': "<b>You are not registered.</b>\n\n"
                     "Please provide your phone number in the following format:\n\n"
                     "For example: <b>+79261234455</b>\n\n"
                     "<i>By providing your phone number, you consent to the processing of your personal data.</i>\n\n"
                     "Please ensure that your phone number is correctly formatted to proceed.",
    '/send_message': "<b>Please provide a message to all users in the following format:</b>\n\n"
                     "<i>/send_message your message</i>\n\n",
    '/start': '<b>Welcome to Garage Sessions Manager.</b>'
              '\n\nPress /new to book a new session.'
              '\n\nPress /upcoming to view upcoming sessions.',
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

INFO: dict[str, str] = {
    'cancel': '<b>You have canceled your booking.</b>'
              '\n\nPress /new to book a new session.',
    'close': "<b>All in all, you're just another brick in the wall.</b>"
             "\n\nPress /start to begin again.",
    'session': "New session for <b>{}</b>"
               "\n\nSession date: <b>{}</b>"
               "\nDuration: <b>{} hours</b>"
               "\nSession type: <b>{}</b>",
    'session_admin_cancel': "Session canceled for <b>{}</b>"
                            "\n\nSession date: <b>{}</b>"
                            "\nDuration: <b>{} hours</b>"
                            "\nSession type: <b>{}</b>",
    'session_admin_info': "New session booked for <b>{}</b>"
                          "\n\nSession date: <b>{}</b>"
                          "\nDuration: <b>{} hours</b>"
                          "\nSession type: <b>{}</b>",
    'session_admin_payment': "Payment confirmed for <b>{}</b> session"
                             "\n\nSession date: <b>{}</b>"
                             "\nDuration: <b>{} hours</b>"
                             "\nSession type: <b>{}</b>",
    'session_booked': "You have booked a new session for <b>{}</b>"
                      "\n\nSession date: <b>{}</b>"
                      "\nDuration: <b>{} hours</b>"
                      "\nSession type: <b>{}</b>"
                      "\n\n<b>Thank you for choosing us!</b>"
}
