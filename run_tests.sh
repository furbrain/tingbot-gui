cat <<HERE
Usage instructions for testing:
Click everything!
Remember to test long clicks for buttons, and also moving mouse off button 
before completing click. Cancel alerts by clicking outside them. Also 
cancel the cancel by moving mouse back into alert before releasing
HERE

coverage run --source=. --omit=setup.py ./demo.py
coverage run --source=. --omit=setup.py -a ./test.py
coverage html
