import re


# Получаем тг айди пользователя по пересланному сообщению
def get_tg_id(message):
    # Проверяем, есть ли пересланное сообщение
    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    # Если пересланного сообщения нет, возвращаем ID текущего пользователя
    return message.from_user.id


# Получаем список доступных эмодзи для реакций
def get_available_emoji():
    with open('available_emoji.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    emoji_list = [emoji.strip().strip('"') for emoji in content.split(',')]

    return emoji_list

# Проверяем находится ли эмодзи в доступном списке
def is_available_emoji(emoji):
    if emoji in get_available_emoji():
        return emoji
    else:
        return False

# Перевод пользовательского ввода интервала для sql запроса
def transfer_interval(user_interval):
    pattern = r'^[0-9:]+$'

    if not bool(re.match(pattern, user_interval)):
        return False
    if len(user_interval.split(":")) != 2:
        return False

    minutes = user_interval.split(":")[0]
    seconds = user_interval.split(":")[1]

    if int(minutes) > 60:
        return False
    if int(seconds) > 60:
        return False
    if int(minutes) < 0:
        return False
    if int(seconds) < 0:
        return False
    if int(minutes) == 0 and int(seconds) == 0:
        return False

    return f"{minutes}m {seconds}s"



