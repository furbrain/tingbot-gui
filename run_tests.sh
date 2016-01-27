coverage run --source=. --omit=setup.py ./demo.py
coverage run --source=. --omit=setup.py -a ./local_test.py
coverage html
