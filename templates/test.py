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
        'author': 'https://github.com/amckenna/',
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