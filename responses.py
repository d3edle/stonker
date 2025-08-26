def handle_response(message, username, date, time):
    message = message.lower()
    print(message)
    # if message == 'hello':
    return f'{username.mention} - Hey, you gonna remember to do {message} on {date} at {time}?'
    if message == 'hi!':
        return 'hello'
    else:
        return 'Invalid: please enter a different message adhering to the proper format.'