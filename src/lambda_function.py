import random
import boto3
from datetime import datetime
from zoneinfo import ZoneInfo

from verses import VERSES


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("daily-bread-history")


def get_daily_verse():
    return random.choice(VERSES)


def create_message(verse):
    return (
        f"Good morning ☀️\n"
        f"{verse['text']}\n"
        f"— {verse['reference']}"
    )


def lambda_handler(event=None, context=None):
    eastern = ZoneInfo("America/New_York")
    today = datetime.now(eastern).date().isoformat()

    # Check whether today's verse already exists
    response = table.get_item(
        Key={
            "date": today
        }
    )

    if "Item" in response:
        verse = {
            "reference": response["Item"]["reference"],
            "text": response["Item"]["text"],
            "category": response["Item"]["category"]
        }

        print("Using existing verse for today")

    else:
        verse = get_daily_verse()

        table.put_item(
            Item={
                "date": today,
                "reference": verse["reference"],
                "text": verse["text"],
                "category": verse["category"]
            }
        )

        print("Saved new verse for today")

    message = create_message(verse)

    print(message)

    return {
        "statusCode": 200,
        "verse": verse,
        "message": message
    }


if __name__ == "__main__":
    lambda_handler()