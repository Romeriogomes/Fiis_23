from __future__ import print_function
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import date
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
options = Options()
options.add_argument('--headless=new')
navegador = webdriver.Remote('http://localhost:4444/wd/hub', options=options)
link = "https://www.fundsexplorer.com.br/ranking"
navegador.get(url=link)
sleep(5)
print(link)
data_Hoje = date.today()
data_Hotem = date.fromordinal(data_Hoje.toordinal())
dataHotenFormat = data_Hotem.strftime("%d/%m/%Y")

dic_Fundo = {'Fundo':[]}
dic_Setor = {'Setor':[]}
dic_Valor = {'Valor':[]}
dic_PvP = {'PvP':[]}
dic_Dividendo = {'Dividendo':[]}
dic_Rentabilidade = {'Rentabilidade':[]}
dic_Data = {'Data':[]}
#table = navegador.find_elements(By.ID, value="upTo--default-fiis-table")
Fundo = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-post_title"]')
Setor = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-setor"]')
Valor = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-valor"]')
PvP = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-pvp"]')
Dividendo = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-dividendo"]')
Rentabilidade = navegador.find_elements(By.XPATH, value='//*[@data-collum="collum-rentabilidade_mes"]')
Data = dataHotenFormat
print("Tabela Encontrada")
Fundos = Fundo[0]
Setors = Setor[0]
Valores = Valor[0]
PvPs = PvP[0]
Dividendos = Dividendo[0]
Rentabilidades =Rentabilidade[0]
Datas = Data[0]


#def Extract ():

for Fundos in Fundo :
    print("extraindo...")
    dic_Fundo['Fundo'].append(Fundos.text)
    global dfFiis1
    dfFiis1 = pd.DataFrame(dic_Fundo, columns=None)
    dic_Data['Data'].append(Data)
    global dfFiis7
    dfFiis7 = pd.DataFrame(dic_Data, columns=None)
for Setores in Setor :
    dic_Setor['Setor'].append(Setores.text)
    global dfFiis2
    dfFiis2= pd.DataFrame(dic_Setor, columns=None)
for Valores in Valor :
    dic_Valor['Valor'].append(Valores.text)
    global dfFiis3
    dfFiis3= pd.DataFrame(dic_Valor, columns=None)
for PvPs in PvP :
    dic_PvP['PvP'].append(PvPs.text)
    global dfFiis4
    dfFiis4 = pd.DataFrame(dic_PvP, columns=None)
for Dividendos in Dividendo :
    dic_Dividendo['Dividendo'].append(Dividendos.text)
    global dfFiis5
    dfFiis5 = pd.DataFrame(dic_Dividendo, columns=None)
for Rentabilidades in Rentabilidade :
    dic_Rentabilidade['Rentabilidade'].append(Rentabilidades.text)
    global dfFiis6
    dfFiis6 = pd.DataFrame(dic_Rentabilidade, columns=None)

    #return dfFiis1,dfFiis2,dfFiis3,dfFiis4,dfFiis5,dfFiis6,dfFiis7
#print(dfFiis1,dfFiis2)
# if __name__ == '__main__':
#     Extract()
dfb = pd.merge(dfFiis1 , dfFiis2, left_index=True, right_index= True)
dfb1 = pd.merge(dfFiis3, dfFiis4, left_index=True, right_index= True)
dfb3 = pd.merge(dfFiis5, dfFiis6, left_index=True, right_index= True)
dfb4 = pd.merge(dfb, dfb1, left_index=True, right_index= True)
dfb5 = pd.merge(dfb4, dfb3, left_index=True, right_index= True)
global dfFiis
dfFiis = pd.merge(dfb5, dfFiis7, left_index=True, right_index= True)

print("Finalizou")


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1CDh4Z2M8ccWe6Oj5pew1bBNIEuZ015OuwIz_MkXqSR8'
SAMPLE_RANGE_NAME = 'Página2!A1'


def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().append(spreadsheetId="1CDh4Z2M8ccWe6Oj5pew1bBNIEuZ015OuwIz_MkXqSR8",
                            range='Página2!A1' , valueInputOption="USER_ENTERED",
                                body = dict(
                                    majorDimension = 'ROWS',
                                    values=dfFiis.T.reset_index().T.values.tolist())).execute()
    print("entrou")
    return result

if __name__ == '__main__':
    main()



