def fill(message):
    return message + '=' * (4096 - len(message))


def strip(message):
    return message.strip('=')
