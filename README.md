# Jones

> Jones is the cybernetically enhanced dolphin from the 1995 film Johnny Mnemonic

This is a simple command line tool for interacting with the Claude Sonnet model available via Amazon Bedrock. The tool uses a repository of templates that to augment user input to facilitate common language tasks such as rephrasing, summarization, review, alternate modeling, etc. Because the tool is command line based and can accepted piped input, it can be used with other command line tools such as `cat`, `tail`, `grep`, etc.

## Install

Recommend first installing `aws-cli` and running `aws configure`

Then clone this repository and run `pip install -r requirements.txt` to install dependencies.

To test jones, run: `echo "why is the sky blue" | python jones.py -t pirate` or `python jones.py -t pirate "why is the sky blue"`

```sh
python jones.py --help

Usage: jones.py [OPTIONS] USER_INPUT

Options:
  -e, --envcreds             Set to use environment variables for loading AWS
                             credentials. Leave unset to use
                             ~/.aws/credentials file.
  -r, --region TEXT          Specify AWS region  [default: us-west-2]
  -v, --verbose              Verbosity. v = INFO, vv = DEBUG
  -t, --template TEXT        Specify a prompt template to include
  -ts, --template-settings   Set to use suggested model settings from
                             template. If set, will override user supplied
                             settings and default settings. Leave unset to use
                             user settings, if specified, or default global
                             settings.
  -l, --list-templates       List available templates
  -tmp, --temperature FLOAT  Set the model temperature parameter  [default:
                             0.9]
  -tp, --top-p FLOAT         Set the model Top-P parameter  [default: 0.999]
  -tk, --top-k INTEGER       Set the model Top-K parameter  [default: 250]
  -mt, --max-tokens INTEGER  Set the max tokens returned by the model
                             [default: 250]
  --help                     Show this message and exit.
```

## Templates

### Default

```sh
python jones.py --list-templates " "

name: 
  title: 
  description: 
name: pirate
  title: Speak like a pirate
  description: This prompt will instruct the model to speak like a pirate, changing the tone, structure, and grammer.
```

### Adding Your Own

To add new templates, place them in the templates directory. Directory nesting is not supported. Template files are in the JSON format following the structure in the \_empty.json file.  Refer to the README.md file in the templates directory for more information on the structure.