import boto3
import click
import json
import logging
import pdb
import sys

logger = logging.getLogger(__name__)

templates = {
    'empty': {
        'title': '',        # a short title for the template
        'author': '',       # the author of the template
        'created': '',      # when the template was created in YYYY-MM-DD format
        'updated': '',      # when the template was last updated in YYYY-MM-DD format
        'description': '',  # a few sentence description of the template
        'notes': '',        # general guidance, caveats, help, etc. for using the template
        'supplement': '',   # any supplemental text that will be included as tokens with the prompt
        'prompt': '',       # the prompt itself
        'suggested_model': '',      # the suggested llm model to use with this prompt
        'suggested_temperature': '',# the suggested model temperature parameter to use with this model and prompt
        'suggested_max-tokens': '', # the suggested number of max tokens parameter to set for this model and prompt
        'suggested_top-p': '',      # the suggested top-p parameter to set for this model and prompt
        'suggested_top-k': '',      # the suggested top-k parameter to set for this model and prompt
    },
    'pirate': {
        'title': 'Speak like a pirate',
        'author': 'Andrew McKenna',
        'created': '2024-04-01',
        'updated': '2024-04-02',
        'notes': 'The answer will mostly stay the same, in terms of content, but be in the voice of a pirate. It\'s silly, so not to be used seriously',
        'description': 'This prompt will instruct the model to speak like a pirate, changing the tone, structure, and grammer.',
        'supplement': '',
        'prompt': 'Please answer the following question as if you were a pirate: ',
        'suggested_model': 'Claude v3',
        'suggested_temperature': '0.9',
        'suggested_max-tokens': '100',
        'suggested_top-p': '0.999',
        'suggested_top-k': '250',
    }
}

@click.command()
@click.argument('user_input', required=True, default=sys.stdin.readline)
@click.option('--verbose', '-v', is_flag=True, default=False, show_default=True, help='Display verbose output')
@click.option('--template', '-t', help='Specify a prompt template to include')
@click.option('--temperature', '-tmp', type=click.FLOAT, default=0.9, help='Set the model temperature parameter') # temperature
@click.option('--top-p', '-tp', type=click.FLOAT, default=0.999, help='Set the model Top-P parameter') # top-p
@click.option('--top-k', '-tk', type=click.INT, default=250, help='Set the model Top-K parameter') # top-k
@click.option('--max-tokens', '-mt', type=click.INT, default=250, help='Set the max tokens returned by the model') # tokens
def main(user_input, verbose, template, temperature, top_p, top_k, max_tokens):
    if verbose: logging.basicConfig(level=logging.INFO)
    logger.info('received from stdin: {}'.format(user_input))
    model_params = {'temperature': temperature,
                    'top_p': top_p,
                    'top_k': top_k,
                    'max_tokens': max_tokens}
    prompt = build_prompt(user_input, template)
    click.echo(send_prompt(prompt, model_params))

def build_prompt(user_input, template):
    """Combine template with user input"""
    if template:
        logger.info('adding template: {} - {}'.format(template, templates[template]))
        user_input = templates[template]['prompt'] + user_input
    return user_input

def send_prompt(user_input, model_params):
    """Send user input to the model"""
    logger.info('prompt: {}'.format(user_input))
    brt = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')

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

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    logger.info(json.dumps(response_body, indent=4))

    return response_body['content'][0]['text']

if __name__ == "__main__":
    main()


