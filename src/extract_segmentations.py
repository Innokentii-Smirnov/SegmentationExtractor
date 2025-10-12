from os import getenv, path
from json import load
from collections import defaultdict
from morph import parseMorph
directory = path.join(getenv('HOME'), 'Documents', 'HurrianCorpus')
infile = path.join(directory, 'PrecompiledDictionary.json')
outfile = path.join(directory, 'word.xhu.tsv')
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
      and transcription.islower()):
    for value in values:
      morph = parseMorph(value)
      data[morph.segmentation.lower()].append(transcription)
for l in data.values():
  l.sort()
with open(outfile, 'w', encoding='utf-8') as fout:
  for key, values in sorted(data.items()):
    print(key, ', '.join(values), sep='\t', file=fout)
