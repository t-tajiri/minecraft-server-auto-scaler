import boto3
import requests
import os

region_name = 'ap-northeast-1'
ec2 = boto3.client('ec2', region_name=region_name)

instance_ids       = os.environ.get('instance_ids', '').split(',')

discord_bot_token  = os.environ.get('discord_bot_token', '')
discord_channel_id = os.environ.get('discord_channel_id', '')

def lambda_handler(event, context):
    action = event.get('action')

    if not action or not instance_ids:
        return {
            'statusCode': 400,
            'body': 'Error: "action" (start/stop) and "instance_ids" are required.'
        }

    if action == 'start':
        try:
            ec2.start_instances(InstanceIds=instance_ids)
            message = f"サーバーを起動しました。 インスタンスID: {instance_ids}"
        except Exception as e:
            message = f"サーバーの起動に失敗しました: {e}"
    elif action == 'stop':
        try:
            ec2.stop_instances(InstanceIds=instance_ids)
            message = f"サーバーを停止しました。 インスタンスID: {instance_ids}"
        except Exception as e:
            message = f"サーバーの停止に失敗しました: {e}"
    else:
        return {
            'statusCode': 400,
            'body': 'Error: Invalid "action".  Must be "start" or "stop".'
        }

    send_discord_message(message)

    return {
        'statusCode': 200,
        'body': message
    }

def send_discord_message(message):
    url = f"https://discord.com/api/channels/{discord_channel_id}/messages"
    headers = {
        "Authorization": f"Bot {discord_bot_token}",
        "Content-Type": "application/json"
    }

    # 送信内容
    payload = {
        "content": message
    }
    
    # POSTリクエストを送信
    requests.post(url, json=payload, headers=headers)