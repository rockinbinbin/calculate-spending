#!/bin/bash
echo 'Running complex input...'
python even.py complex.input.json;
echo 'Running simple input...'
python even.py simple.input.json;
echo 'Running test1 input...'
python even.py test1.input.json;
echo 'Running insolvent input...'
python even.py insolvent.input.json