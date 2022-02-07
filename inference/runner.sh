#!/bin/bash
START_TIME=$(date +%s)
python model_001.py
python model_002.py
python model_003.py
python run_ensemble.py
END_TIME=$(date +%s)
echo "It took $(($END_TIME - $START_TIME)) seconds to inference..."

