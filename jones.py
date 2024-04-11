import boto3
import click
import glob
import json
import logging
import os
import pdb
import sys

logger = logging.getLogger(__name__)

@click.command()
@click.argument('user_input', required=True, default=sys.stdin.readline)
@click.option('--envcreds', '-e', is_flag=True, default=False, show_default=True, help='User environment variables for loading AWS credentials or ~/.aws/credentials file')
@click.option('--region', '-r', default='us-west-2', show_default=True, help='Specify AWS region')
@click.option('--verbose', '-v', count=True, help='Verbosity. v = INFO, vv = DEBUG')
@click.option('--template', '-t', help='Specify a prompt template to include')
@click.option('--list-templates', '-l', is_flag=True, default=False, help='List available templates')
@click.option('--temperature', '-tmp', type=click.FLOAT, default=0.9, help='Set the model temperature parameter')
@click.option('--top-p', '-tp', type=click.FLOAT, default=0.999, help='Set the model Top-P parameter')
@click.option('--top-k', '-tk', type=click.INT, default=250, help='Set the model Top-K parameter')
@click.option('--max-tokens', '-mt', type=click.INT, default=250, help='Set the max tokens returned by the model')
def main(user_input, envcreds, region, verbose, template, list_templates, temperature, top_p, top_k, max_tokens):
    if verbose == 1: logging.basicConfig(level=logging.INFO)
    if verbose > 1: logging.basicConfig(level=logging.DEBUG)
    if list_templates:
        lst_templates()
    else:
        logger.info('loading templates')
        templates = load_templates()
        logger.info('templates loaded')
        model_params = {'temperature': temperature,
                        'top_p': top_p,
                        'top_k': top_k,
                        'max_tokens': max_tokens}
        logger.info('setting model params: {}'.format(model_params))
        logger.info('user input from stdin: {}'.format(user_input))
        prompt = build_prompt(user_input, template, templates)
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

def build_prompt(user_input, template, templates):
    """Combine template with user input"""
    if template and template in templates:
        logger.info('template specified and found')
        logger.info('adding template: {} - {}'.format(template, templates[template]))
        prompt = templates[template]['prompt'] + user_input
    elif template and template not in templates:
        logger.error('incorrect template specified')
        sys.exit()
    return prompt

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

def load_templates():
    templates = {}
    for file in glob.glob('templates/*.json'):
        with open(file) as f:
            d = json.load(f)
            logger.info('loaded: {} - {}'.format(f.name,d))
            templates[d['name']] = d
    return templates

def lst_templates():
    for file in glob.glob('templates/*.json'):
        with open(file) as f:
            d = json.load(f)
            logger.info('loaded: {} - {}'.format(f.name,d))
            click.echo('name: {}\n  title: {}\n  description: {}'.format(d['name'], d['title'], d['description']))

if __name__ == "__main__":
    main()


