import pandas as pd


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

