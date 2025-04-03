import boto3
import os

region_name = 'ap-northeast-1'
ec2 = boto3.client('ec2', region_name=region_name)
instance_ids = os.environ.get('instance_ids', '').split(',')

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
            message = f"Started instances: {instance_ids}"
        except Exception as e:
            message = f"Error starting instances: {e}"
    elif action == 'stop':
        try:
            ec2.stop_instances(InstanceIds=instance_ids)
            message = f"Stopped instances: {instance_ids}"
        except Exception as e:
            message = f"Error stopping instances: {e}"
    else:
        return {
            'statusCode': 400,
            'body': 'Error: Invalid "action".  Must be "start" or "stop".'
        }

    return {
        'statusCode': 200,
        'body': message
    }
