exit 0;
################################################################################
# run the following commands one by one in the root directory of the repository
################################################################################
export PYTHONPATH=.

#python3 src/c001__train_fixer.py --round_name round0 --max_epoch 2
#python3 src/c003__run_fixer.py   --round_name round0 
python3 src/c005__eval_fixer.py  --round_name round0
