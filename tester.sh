#!/bin/bash
# Tester for ordinary
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
echo "25%"
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
python supervisor.py computer ordinary >> res1.txt
echo "50%"
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
echo "75%"
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt
python supervisor.py ordinary computer >> res2.txt

echo "100%"