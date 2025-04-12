import json
import os

from discord_interactions import InteractionResponseType, InteractionType, verify_key

discord_public_key = os.environ.get("DISCORD_PUBLIC_KEY", "")


def lambda_handler(event, context):
    request_body = json.loads(event.get("body", "{}"))
    headers = event.get("headers", {})

    # Verify request
    signature = headers.get("x-signature-ed25519")
    timestamp = headers.get("x-signature-timestamp")
    raw_body = event.get("body", "{}").encode()
    if (
        signature is None
        or timestamp is None
        or not verify_key(raw_body, signature, timestamp, discord_public_key)
    ):  # Authorization
        return {"statusCode": 401, "body": "Bad request signature"}

    # Handle request
    interaction_type = request_body.get("type")

    if interaction_type in [
        InteractionType.APPLICATION_COMMAND,
        InteractionType.MESSAGE_COMPONENT,
    ]:
        data = request_body.get("data", {})
        command_name = data.get("name")

        if command_name == "start":
            response_text = "Hello there!"
        elif command_name == "echo":
            response_text = f"Echoing: {data['options'][0]['value']}"
        else:
            raise NotImplementedError(f"Command '{command_name}' not implemented")

        response_data = {
            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {"content": response_text},
        }
    else:
        response_data = {"type": InteractionResponseType.PONG}

    return {"statusCode": 200, "body": json.dumps(response_data)}
