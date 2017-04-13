make
rm results/*
./scripts/valid.sh miotcd2 miotcd2
python scripts/csv_result.py miotcd2 train
