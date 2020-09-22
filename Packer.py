from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, flash

from werkzeug.utils import secure_filename
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload


app = Flask(__name__)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

#Setting
app.secret_key = 'mysecretkey'

#Send function
def uploadFile(filename, filepath, mimetype):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)

    #Group all data, send and execute to dirve
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print('File ID: %s' % file.get('id'))

#Routes
@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/data', methods = ['POST'])
def Data():
    start_time = time.time()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        for x in range(0,len(files)):
            filename = files[x].filename
            filepath = secure_filename(files[x].filename)
            #filepath2 = './Envios/'+filepath
            mimetype = files[x].mimetype
            uploadFile(filename,filepath,mimetype)
    print(time.time() - start_time)
    return render_template('index.html')

@app.route('/analizar',methods = ['POST'])
def actualizar():

    if request.method == 'POST':
        opc = request.form['sec']
        str(opc)
        if opc == '1':
            os.system('Media_de_colores_por_imagen.py')
            os.system('Reporte.py')
        if opc == '32':
            os.system('Media_de_colores_por_imagen32.py')
            os.system('Reporte.py')
        if opc == '64':
            os.system('Media_de_colores_por_imagen64.py')
            os.system('Reporte.py')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
