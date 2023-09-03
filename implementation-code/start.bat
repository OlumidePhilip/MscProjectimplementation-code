pip install -r requirements.txt
cd siamese_model
start /B python main.py
cd ../website
flask --app main.py run
