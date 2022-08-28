from absl import flags
from absl import app

flags.DEFINE_string('file', '', 'file to strip unicode')
FLAGS = flags.FLAGS

REPLACE_VALS = {
  u"\u2060": " ",
  u"\u2009": " ",
  u"\u200A": " ",
  u"\U0001D4AA": "O",
  u"\u03B5": "$\\epsilon$",
  u"\uFE0E": " ",
  u"\u21A9": " ", # return arrow
}

def main(unused_argv):
  with open(FLAGS.file) as f:
    s = f.read()

  s2 = ''
  for c in s:
    # if c in REPLACE_VALS:
    #   print('yes', c)
    s2 += REPLACE_VALS.get(c, c)

  with open(FLAGS.file.split('.md')[0] + '_clean.md', 'w') as f2:
    f2.write(s2)

if __name__ == '__main__':
  app.run(main)