make

rm results/*
./scripts/valid.sh miotcd-train miotcd1
python scripts/csv_result.py miotcd1 train

rm results/*
./scripts/valid.sh miotcd-train miotcd2
python scripts/csv_result.py miotcd2 train

rm results/*
./scripts/valid.sh miotcd-train miotcd3
python scripts/csv_result.py miotcd3 train

rm results/*
./scripts/valid.sh miotcd-train miotcd4
python scripts/csv_result.py miotcd4 train

rm results/*
./scripts/valid.sh miotcd-train miotcd5
python scripts/csv_result.py miotcd5 train

rm results/*
./scripts/valid.sh miotcd-test miotcd1
python scripts/csv_result.py miotcd1 test

rm results/*
./scripts/valid.sh miotcd-test miotcd2
python scripts/csv_result.py miotcd2 test

rm results/*
./scripts/valid.sh miotcd-test miotcd3
python scripts/csv_result.py miotcd3 test

rm results/*
./scripts/valid.sh miotcd-test miotcd4
python scripts/csv_result.py miotcd4 test

rm results/*
./scripts/valid.sh miotcd-test miotcd5
python scripts/csv_result.py miotcd5 test
