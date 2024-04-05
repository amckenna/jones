import boto3
import click
import json
import logging
import os
import pdb
import sys
import templates.test as templates

logger = logging.getLogger(__name__)

@click.command()
@click.argument('user_input', required=True, default=sys.stdin.readline)
@click.option('--envcreds', '-e', is_flag=True, default=False, show_default=True, help='User environment variables for loading AWS credentials or ~/.aws/credentials file')
@click.option('--region', '-r', default='us-west-2', show_default=True, help='Specify AWS region')
@click.option('--verbose', '-v', is_flag=True, default=False, show_default=True, help='Display verbose output')
@click.option('--template', '-t', help='Specify a prompt template to include')
@click.option('--temperature', '-tmp', type=click.FLOAT, default=0.9, help='Set the model temperature parameter') # temperature
@click.option('--top-p', '-tp', type=click.FLOAT, default=0.999, help='Set the model Top-P parameter') # top-p
@click.option('--top-k', '-tk', type=click.INT, default=250, help='Set the model Top-K parameter') # top-k
@click.option('--max-tokens', '-mt', type=click.INT, default=250, help='Set the max tokens returned by the model') # tokens
def main(user_input, envcreds, region, verbose, template, temperature, top_p, top_k, max_tokens):
    if verbose: logging.basicConfig(level=logging.INFO)
    logger.info('received from stdin: {}'.format(user_input))
    model_params = {'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k,
                    'max_tokens': max_tokens}
    prompt = build_prompt(user_input, template)
    if envcreds:
        logger.info('fetching creds from environment variables')
        session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                aws_session_token=os.getenv('AWS_SESSION_TOKEN'),)
        client = session.client(service_name='bedrock-runtime', region_name='us-west-2')
    else:
        logger.info('fetching creds from aws credentials file')
        client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    click.echo(send_prompt(prompt, model_params, client))

def build_prompt(user_input, template):
    """Combine template with user input"""
    if template and template in templates.templates:
        logger.info('template specified and found')
        logger.info('adding template: {} - {}'.format(template, templates.templates[template]))
        user_input = templates.templates[template]['prompt'] + user_input
    elif template and template not in templates.templates:
        logger.error('incorrect template specified')
        sys.exit()
    return user_input

def send_prompt(user_input, model_params, client):
    """Send user input to the model"""
    logger.info('prompt: {}'.format(user_input))

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",    
        "max_tokens": model_params['max_tokens'],
        "system": "",    
        "messages": [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": user_input }
          ]
            }
        ],
        "temperature": model_params['temperature'],
        "top_p": model_params['top_p'],
        "top_k": model_params['top_k'],
    })

    modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
    accept = 'application/json'
    contentType = 'application/json'

    response = client.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    logger.info(json.dumps(response_body, indent=4))

    return response_body['content'][0]['text']

if __name__ == "__main__":
    main()


