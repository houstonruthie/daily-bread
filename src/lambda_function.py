import random
from verses import VERSES


def get_daily_verse():
    return random.choice(VERSES)


def create_message(verse):
    return (
        f"Good morning ☀️\n\n"
        f"{verse['text']}\n\n"
        f"— {verse['reference']}"
    )


def lambda_handler(event=None, context=None):
    verse = get_daily_verse()
    message = create_message(verse)

    print(message)

    return {
        "statusCode": 200,
        "verse": verse,
        "message": message
    }


if __name__ == "__main__":
    lambda_handler()