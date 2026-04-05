import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

test_random_state = 6212
dev_random_state = 489

parser = argparse.ArgumentParser(prog='train_test_split.py',
                                 description='Split a dataset')
parser.add_argument('infile')
parser.add_argument('language')
args = parser.parse_args()

data = pd.read_csv(args.infile, header=0, index_col=False, sep='\t')
print(data.head())

model_data, test_data = train_test_split(data, test_size=0.1, random_state=test_random_state)
train_data, dev_data = train_test_split(model_data, test_size=0.1, random_state=dev_random_state)

train_data.to_csv(f'{args.language}.word.train.tsv', index=False, sep='\t', header=False)
dev_data.to_csv(f'{args.language}.word.dev.tsv', index=False, sep='\t', header=False)
test_data.to_csv(f'{args.language}.word.test.gold.tsv', index=False, sep='\t', header=False)
test_data[['form', 'feats']].to_csv(f'{args.language}.word.test.tsv', index=False, sep='\t', header=False)
