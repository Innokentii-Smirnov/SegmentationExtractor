from os import getenv, path
from json import load
from collections import defaultdict
from morph import parseMorph
directory = path.join(getenv('HOME'), 'bwSyncShare', 'TIVE BASISCORPUS ARBEITSBEREICH')
infile = path.join(directory, 'Dictionary.json')
assert path.exists(infile)
outfile = 'word.xhu.tsv'
assert path.exists(infile)
with open(infile, 'r', encoding='utf-8') as fin:
  json_data = load(fin)
dictionary = json_data['dictionary']
data = defaultdict(list)
def is_fragment(form: str) -> bool:
  return '[' in form or ']' in form or 'x' in form or '(-)' in form
for transcription, values in dictionary.items():
  if (not is_fragment(transcription)
      and transcription.strip() != ''
      and transcription.islower()
      and not any(char.isdigit() for char in transcription)):
    for value in values:
      morph = parseMorph(value)
      data[morph.segmentation.lower()].append(transcription)
for l in data.values():
  l.sort()
with open(outfile, 'w', encoding='utf-8') as fout:
  for key, values in sorted(data.items()):
    print(key, ', '.join(sorted(set(values))), sep='\t', file=fout)
