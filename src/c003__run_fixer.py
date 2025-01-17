import sys
import argparse
from utils.fairseq_utils import *


parser = argparse.ArgumentParser()
parser.add_argument('--round_name')
parser.add_argument('--destdir_root', default='')
parser.add_argument('--gpu_ids', default='0', help='Comma separated list')
args = parser.parse_args()
args.gpu_ids = args.gpu_ids.split(",")


data_dir = Path('/mnt/disks/persist/data')
round_dir = data_dir/args.round_name
destdir_root = Path(args.destdir_root) if args.destdir_root else round_dir/'orig_bad'


n_splits = 5  #all the original bad code is split into 5 chunks for faster processing

#Preprocess inputs
for split in range(n_splits):
    destdir = destdir_root/f'fairseq_preprocess__orig_bad.{split}'
    if os.path.exists(str(destdir)):
        continue
    fairseq_preprocess(src='bad', tgt='good', workers=10,
                          destdir  = str(destdir),
                          testpref = str(data_dir/f'orig_bad_code/orig.{split}'),
                          srcdict  = str(data_dir/'token_vocab.txt'),
                          only_source=True )
    os.system('cp {} {}'.format(data_dir/'token_vocab.txt', destdir/'dict.good.txt'))

#Run fixer
model_dir  = round_dir/'model-fixer'
model_path = model_dir/'checkpoint_best.pt'
gpus = (args.gpu_ids * (n_splits//len(args.gpu_ids) +1))[:n_splits]
use_Popen = (len(args.gpu_ids) > 1)
ps = []
for split, gpu in zip(range(n_splits), gpus):
    destdir    = destdir_root/f'fairseq_preprocess__orig_bad.{split}'
    pred_path  = destdir/'model-fixer.pred.txt'
    p = fairseq_generate(str(gpu), str(destdir), str(model_path), str(pred_path),
                      src='bad', tgt='good', gen_subset='test', use_Popen=use_Popen,
                      beam=10, nbest=10, max_len_a=1, max_len_b=50, max_tokens=7000)
    ps.append(p)

if use_Popen:
    exit_codes = [p.wait() for p in ps]
