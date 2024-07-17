import json
import os
import requests

def handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

    try:
        body = json.loads(event['body'])
        source = body['source']

        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            raise ValueError("GitHub token not found in environment variables")

        response = requests.post(
            'https://api.github.com/repos/Saimadhav2/youtube/dispatches',
            headers={
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            },
            json={
                'event_type': 'log_source',
                'client_payload': {'source': source}
            }
        )

        response.raise_for_status()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Logging triggered successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }