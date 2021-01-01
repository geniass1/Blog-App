echo "Hello, world!"
set -e
python3 -m flake8
python3 -m coverage run --source=. test_app.py
python3 -m coverage report --fail-under=100
