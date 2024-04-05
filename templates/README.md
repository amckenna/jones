## Template Format

```
{
"empty": {
        "title": "",        # a short title for the template
        "author": "",       # the author of the template
        "created": "",      # when the template was created in YYYY-MM-DD format
        "updated": "",      # when the template was last updated in YYYY-MM-DD format
        "description": "",  # a few sentence description of the template
        "notes": "",        # general guidance, caveats, help, etc. for using the template
        "supplement": "",   # any supplemental text that will be included as tokens with the prompt
        "prompt": "",       # the prompt itself
        "suggested_model": "",      # the suggested llm model to use with this prompt
        "suggested_temperature": "",# the suggested model temperature parameter to use with this model and prompt
        "suggested_max-tokens": "", # the suggested number of max tokens parameter to set for this model and prompt
        "suggested_top-p": "",      # the suggested top-p parameter to set for this model and prompt
        "suggested_top-k": "",      # the suggested top-k parameter to set for this model and prompt
    }
}
```