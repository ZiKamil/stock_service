echo "Running migrate"
python -m flask db migrate
echo "Running upgrade"
python -m flask db upgrade
echo "Running the app"
python -m flask run --host=0.0.0.0