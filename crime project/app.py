from flask import Flask, render_template, request
import pickle
import numpy as np
from state_data import past_data
state_models = pickle.load(open('state_models.pkl', 'rb'))

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            year = int(int(request.form['year']) - 2022)
            state = request.form['state']
            if year < 0:
                return render_template('index.html', error='Year should be greater than 2022')
            y_pred = np.array(state_models[state].predict(year))
        except Exception as e:
            print('error',e)
            return render_template('index.html', error='Phasing error, please try again!')
        data = {2023+i:y_pred[i] for i in range(len(y_pred))}
        print(data)
        return render_template('index.html',state=state, year=year, data=data, past_data=past_data[state])
    return render_template('index.html')

    
if __name__ == '__main__':
    app.run(debug=True)


