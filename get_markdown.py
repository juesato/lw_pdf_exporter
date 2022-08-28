import json
import os
import requests
import subprocess
from absl import flags
from absl import app
from dateutil import parser as date_parser

flags.DEFINE_string('post_id', '', 'post id, such as "Sn5NiiD5WBi4dLzaB"')
flags.DEFINE_string('pandoc_extras', '', 'any commands to append to pandoc command')
FLAGS = flags.FLAGS

GRAPHQL_ENDPOINT = 'https://www.lesswrong.com/graphql'

# Example cURL query (uncomment and paste into shell):
# Note that for some reason, we shouldn't pass content-type when calling from Python.
# curl 'https://www.lesswrong.com/graphql' \
# -H 'content-type: application/json' \
# -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36' \
# --data-raw '{"query":"{post(\n            input: {  \n            selector: {\n                _id: \"5bd75cc58225bf06703754b9\"\n            }      \n            }) \n        {\n            result {\n            _id\n            title\n            url\n            contents {\n              markdown\n            }\n            user {\n              username\n              fullName\n            }\n            }\n        }\n}","variables":null,"operationName":null}'

# Slightly modified from examples here:
# https://www.lesswrong.com/posts/LJiGhpq8w4Badr5KJ/graphql-tutorial-for-lesswrong-and-effective-altruism-forum
QUERY_FORMAT = '''{{
    post(
        input: {{  
        selector: {{
            _id: "{post_id}"
        }}      
        }})
    {{
        result {{
        _id
        title
        postedAt
        url
        contents {{
          markdown
        }}
        user {{
          username
          fullName
        }}
        }}
    }}
}}'''
# NB: Headers weren't necessary as of Dec '21, but were necessary by Aug '22.
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

# YAML metadata block can be used by pandoc
OUTPUT_FORMAT = '''---
title: '{title}'
author: {author}
date: {date}
papersize: a4
---

{body}'''
# More options for above:
# documentclass: tufte-handout

PANDOC_FORMAT = (
  'pandoc -o out/{post_id}.pdf out/{post_id}.md -V colorlinks=true -V linkcolor=blue'
  ' -V urlcolor=blue -V geometry:top=1in,bottom=1in,left=1.5in,right=1.5in'
  ' --pdf-engine=xelatex')
COPY_FORMAT = 'cp out/{post_id}.pdf cur.pdf'


def main(unused_argv):
  assert FLAGS.post_id, 'must specify --post_id'
  out_path = f'out/{FLAGS.post_id}.md'
  if not os.path.exists(out_path):
    # Make POST request
    query = QUERY_FORMAT.format(post_id=FLAGS.post_id)
    data = {'query': query}
    response = requests.post(
      GRAPHQL_ENDPOINT, data=data, headers=HEADERS)
    response_data = json.loads(response.text)
    result = response_data['data']['post']['result']

    # Format results into markdown and save
    markdown_text = result['contents']['markdown']
    post_time = date_parser.parse(result['postedAt'])
    date_str = post_time.strftime('%B %d, %Y')
    if result['user']['fullName']:
      author = result['user']['fullName'].replace(':', '\\:')
    else:
      author = result['user']['username']
    output = OUTPUT_FORMAT.format(
        title=result['title'],
        date=date_str,
        author=author,
        body=markdown_text)
    with open(out_path, 'w') as f:
      f.write(output)
    print(f'Saved in: {out_path}')
  else:
    print(f'Markdown file already exists: {out_path}')

  # Run pandoc
  pandoc_cmd = PANDOC_FORMAT.format(post_id=FLAGS.post_id) + ' ' + FLAGS.pandoc_extras
  print(pandoc_cmd)
  subprocess.run(pandoc_cmd.split())
  subprocess.run(COPY_FORMAT.format(post_id=FLAGS.post_id).split())

if __name__ == '__main__':
  app.run(main)