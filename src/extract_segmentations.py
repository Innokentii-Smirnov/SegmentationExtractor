from os import getenv, path
from json import load
from collections import defaultdict
from morph import parseMorph
from statistics import mean
directory = 'data'
infile = path.join(directory, 'Dictionary.json')
assert path.exists(infile)
outfile = 'word.xhu.tsv'
SEP = ', '
def join(words: list[str]) -> str:
  return SEP.join(sorted(words))
assert path.exists(infile)
with open(infile, 'r', encoding='utf-8') as fin:
  json_data = load(fin)
dictionary = json_data['dictionary']
data = defaultdict(list)
def is_fragment(form: str) -> bool:
  return '[' in form or ']' in form or 'x' in form or '(-)' in form
segmentation_counts = list[int]()
for transcription, values in dictionary.items():
  if (not is_fragment(transcription)
      and transcription.strip() != ''
      and transcription.islower()
      and not any(char.isdigit() for char in transcription)):
    segmentations = list[str]()
    for value in values:
      morph = parseMorph(value)
      if morph.segmentation != '':
        segmentations.append(morph.segmentation.lower())
    segmentation_counts.append(len(segmentations))
    joined_segmentations = join(segmentations)
    data[joined_segmentations].append(transcription)
print('Average segmentation count for a transcription: {0:2f}'.format(mean(segmentation_counts)))
for l in data.values():
  l.sort()
with open(outfile, 'w', encoding='utf-8') as fout:
  for joined_segmentations, transcriptions in sorted(data.items()):
    joined_transcriptions = join(transcriptions)
    print(joined_segmentations, joined_transcriptions, sep='\t', file=fout)
