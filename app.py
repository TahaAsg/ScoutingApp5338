from flask import Flask, render_template, request, url_for, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import json
from multiprocessing import Value
import time
import pandas as pd

balls_shot = Value('i', 0)
accidents = Value('i', 0)
e1 = Value('i', 0)
e2 = Value('i', 0)

app = Flask(__name__)

def init_sheet():
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open("RoboLoco-Scouting-Test").sheet1

    return sheet

@app.route('/', methods=['GET', 'POST'])
def home():
    balls_shot = 0
    if request.method == 'POST':
        for key, val in request.form.items():
            if key == 'team_name':
                context = {
                    'team_name': val
                }

                with open('./team_name.txt', 'w') as f:
                    f.write(val)

        return redirect('/observing')
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/observing', methods=['GET', 'POST'])
def observation():
    with open('./team_name.txt', 'r') as f:
        name = f.read()

    context = {
        'team_name': name
    }

    if request.method == 'POST':
        for key, val in request.form.items():
            if key == "notes":
                notes = val
             
        # sheet = init_sheet()

        with open('./team_name.txt', 'r') as f:
            name = f.read()

        data = {
            'team_name': name,
            'boxes_carried': request.json['boxes_carried'],
            'boxes_controlled': request.json['boxes_controlled'],
            'accidents': request.json['accidents'],
            'e2': request.json['e2'],
            'notes': request.json['notes']
        }

        print(request.json)

        df = pd.read_csv('./observations/BunnyBots.csv')
        df = pd.read_csv('./observations/BunnyBots.csv')

        data = {
            'team_name': pd.Series([data['team_name']]),
            'boxes_carried': pd.Series([data['boxes_carried']]),
            'boxes_controlled': pd.Series([data['boxes_controlled']]),
            'accidents': pd.Series([data['accidents']]),
            'notes': pd.Series([data['notes']])
        }

        df = df.append(pd.DataFrame(data), ignore_index=True)

        df.to_csv('./observations/BunnyBots.csv', index=False) 

        '''
        team_name = list(df['Team_Name'])
        print(team_name)
        boxes_carried = list(df['Boxes_Carried'])
        boxes_controlled = list(df['Boxes_Controlled'])
        accidents = list(df['Accidents'])

        team_name.append(data['team_name'])
        boxes_carried.append(data['boxes_carried'])
        boxes_controlled.append(data['boxes_controlled'])
        accidents.append(data['accidents'])

        df['team_name'] = pd.Series(team_name)
        df['boxes_carried'] = pd.Series(boxes_carried)
        df['boxes_controlled'] = pd.Series(boxes_controlled)
        df['accidents'] = pd.Series(accidents)

        df.to_csv('./observations/BunnyBots.csv', ignore_index=True) 
        '''

        # df = pd.DataFrame(data)

        # df.to_csv(f'./observations/{name}')

        '''
        # sheets API update calls
        sheet = init_sheet()

        col1 = sheet.col_values(1)
        team_index = len(col1) + 1

        sheet.update_cell(team_index, 1, data['team_name'])
        sheet.update_cell(team_index, 2, data['balls_shot'])
        sheet.update_cell(team_index, 3, data['accidents'])
        sheet.update_cell(team_index, 4, data['e1'])
        sheet.update_cell(team_index, 5, data['e2'])
        sheet.update_cell(team_index, 6, data['notes'])
        '''
                
        # sheet.update_cell(2, 1, name)
        return render_template('home.html')

    if request.method == 'POST':
        if request.form.get('ball_shot'):
            '''
            cell = sheet.cell(2, 2).value
            sheet.update_cell(2, 2, str(int(cell) + 1))
            '''
            balls_shot.value += 1
            
            print(f'{int(balls_shot.value - 1)} -> {int(balls_shot.value)}')
        if request.form.get('accident'):
            accidents.value += 1
            
            print(f'{int(accidents.value - 1)} -> {int(accidents.value)}')
        if request.form.get('e1'):
            e1.value += 1
            
            print(f'{int(e1.value - 1)} -> {int(e1.value)}')
        if request.form.get('e2'):
            e2.value += 1

            print(f'{int(e1.value - 1)} -> {int(e2.value)}')

    return render_template('observing.html', **context) 

if __name__ == '__main__':
    app.run(debug=True)