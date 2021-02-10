import pandas as pd
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
import qrcode
import jinja2
import requests
import os

tsn_name = "ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ \"ЯХРОМА РИВЕР\""
tsn_inn  = "7726405144"
tsn_rs   = "40703810438000009653"
tsn_bank = "ПАО «Сбербанк» г. Москва"
tsn_bik  = "044525225"
tsn_korsch="30101810400000000225"

class forming(object):
    summa=[0]*530
    def __init__(self):
        money = pd.read_excel("./meney.xlsx")
        for i in range(1,len(money)):
            try:
                self.summa[ int(money.iloc[i,0]) ] = int( money.iloc[i,13] * 100 )
            except:
                print( money.iloc[i,0] )

    def put_to_db(self,uch,fio,tel1,tel2,summ,ip):
        submission = {\
            "entry.640839015": str(uch),\
            "entry.1407090537": str(fio),\
            "entry.56622846": str(tel1),\
            "entry.869874719": str(tel2),\
            "entry.1267651923": str(summ),\
            "entry.892522649": str(ip),\
        }
        url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLScrjVFuTpA0YBtwcLUjg2GtMGhKqcS3qCqNyW5YrSd_XqrvLw/formResponse"
        requests.post(url, submission) 


    def form(self,uch,fio,tel1,tel2,summ,ip):
        summ = int( float(summ) * 100 )
        fio = fio.decode().replace('+',' ')    
        self.put_to_db(uch,fio,tel1,tel2,summ,ip)
        #Генерируем и сохраняем QR
        qr_data=f"ST00012|Name={tsn_name}|PersonalAcc={tsn_rs}|BankName={tsn_bank}|BIC={tsn_bik}|CorrespAcc={tsn_korsch}|Purpose=Членские и целевые взносы за 2021 год. уч. {str(uch)} телефон1: {str(tel1)} телефон2: {str(tel2)}|Sum={str(summ)}|PayeeINN={tsn_inn}|PayerAddress=Уч. {str(uch)}|FirstName={str(fio)}"
        qrimg = qrcode.make(qr_data)
        qrimg.save(f"./qrs/{str(ip)}.png")
        #Генерируем и сохраняем док файл
        doc = DocxTemplate("obrazec.docx")
        context = { 'nom0' : str(uch), 'tel1' : str(tel1), 'tel2' : str(tel2) , 'fio' : str(fio) , 'nom1' : str(uch) , 'sum_r': str( summ // 100 ) , 'sum_k': str( summ % 100 ) , 'QR' : InlineImage(doc,f"./qrs/{str(ip)}.png",width=Mm(30)) }
        doc.render(context)
        doc.save(f"./docs/{str(ip)}.docx")
        #Конвертирование в pdf
        os.system(f"libreoffice --convert-to pdf ./docs/{str(ip)}.docx")
        return str(ip)+".pdf"



