def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there!'
    if p_message == 'help':
        return '`There is currently no help menu.`'
    if p_message == 'cricket':
        return 'https://tenor.com/view/crickets-crickets-chirping-silence-awkward-silence-gif-5319192'
    if p_message == 'disable':
        return 'The insect repelent has been sprayed'
    if p_message == 'enable':
        return 'A new cricket immune to the repelent has arrived'
