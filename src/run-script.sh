#python3 src/c003__run_fixer.py   --round_name round1-FixerOnly_Beam_30_original
#python3 src/c006__generate_paired_data_from_fixer.py --round_name round1-FixerOnly_Beam_30_original --out_round_name round2-FixerOnly_Beam_30_original
python3 src/c001__train_fixer.py --round_name  round2-FixerOnly_Beam_30_original_correct_edit4  --max_epoch 1 --continue_from '/mnt/disks/persist/data/round1-FixerOnly_Beam_30_original_correct_edit4/model-fixer/checkpoint_best.pt'
python3 src/c003__run_fixer.py   --round_name round2-FixerOnly_Beam_30_original_correct_edit4
python3 src/c005__eval_fixer.py   --round_name round2-FixerOnly_Beam_30_original_correct_edit4
