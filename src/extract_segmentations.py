from os import path
from json import load
from morph import parseMorph
import argparse
import regex as re
import pandas as pd
from morphosyntactic_word import MorphosyntacticWord

def is_fragment(form: str) -> bool:
  return '[' in form or ']' in form or 'x' in form or '(-)' in form

def preprocess_segmentation(segmentation: str) -> str:
  return re.sub(r'(?<=^|\.)\p{Lu}(?!\p{Lu})', lambda match: str.lower(match.group(0)), segmentation)

parser = argparse.ArgumentParser(
  prog='extract_segmentations.py',
  description='Extract morpheme segmentations from a morphological dictionary'
)
parser.add_argument('infile', help='The dictionary file')
parser.add_argument('outfile', help='The resulting dataset file')
parser.add_argument('graphic_variants', help='A file for graphic variants')
parser.add_argument('homonyms', help='A file for homonyms')
args = parser.parse_args()

if not path.exists(args.infile):
  print('The dictionary file does not exist.')
  exit()

with open(args.infile, 'r', encoding='utf-8') as fin:
  json_data = load(fin)
dictionary = json_data['dictionary']

morphosyntactic_words = set[MorphosyntacticWord]()

for transcription, values in dictionary.items():
  if (not is_fragment(transcription)
      and transcription.strip() != ''
      and transcription.islower()
      and not any(char.isdigit() for char in transcription)
      and not transcription.startswith('*')):
    for value in values:
      morph = parseMorph(value)
      if morph.segmentation != '' and not morph.segmentation.startswith('-') and morph.pos != 'unclear':
        segmentation = preprocess_segmentation(morph.segmentation)
        morphosyntactic_word = MorphosyntacticWord(transcription, segmentation, morph.pos)
        morphosyntactic_words.add(morphosyntactic_word)

df = pd.DataFrame(sorted(morphosyntactic_words))

df.sort_values(['segmentation', 'pos'], inplace=True)
df[df.duplicated(['segmentation', 'pos'], False)].to_csv(args.graphic_variants, sep='\t', index=False)

df.sort_values(['form', 'pos'], inplace=True)
df[df.duplicated(['form', 'pos'], False)].to_csv(args.homonyms, sep='\t', index=False)

df.sort_values(['segmentation', 'pos'], inplace=True)
df.drop_duplicates(['segmentation', 'pos'], inplace=True)

df.sort_values(['form', 'pos'], inplace=True)
df.drop_duplicates(['form', 'pos'], inplace=True)

df.to_csv(args.outfile, sep='\t', index=False)
