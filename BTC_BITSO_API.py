
##### Precio de Bitcoin en BITSO usando la Bitso API
# se define una funcion que busca el precio de BTC mediante el PPP esto es el volumen * precio de las 50 ultimas posturas de compra y venta entre el total de postura para venta y compra
# Usando las ultimas 50 posturas que nos da el JSON de la API
## el PPP se basa en Precio Promedio Ponderado (PPP) de la BMV
   # Factor calculado por la BMV para cada una de las acciones listadas, mediante la ponderación por volumen de los precios a los que se realizan las operaciones con cada valor durante los últimos 20 minutos de cada jornada bursátil.
   # https://www.bmv.com.mx/es/Grupo_BMV/Glosario
# PPP_Compra = (Precio_compra * Volumen_Compra)/ Sum(Volumen_Compra) de manera analoga se obtiene el PPP de venta y se usa el promedio de ambos.

def btc_value_mxn():
    import time
    import requests
    import numpy as np
    response = requests.get('https://api.bitso.com/v3/order_book/?book=btc_mxn')
    json_response = response.json()
    price_asks=[]
    volume_asks=[]
    price_bids=[]
    volume_bids=[]

    for i in range(0,50):

        price_asks.append(float(json_response['payload']['asks'][i]['price']))
        price_bids.append(float(json_response['payload']['bids'][i]['price']))

        volume_asks.append(float(json_response['payload']['asks'][i]['amount']))
        volume_bids.append(float(json_response['payload']['bids'][i]['amount']))


    ppp_asks= np.sum((np.array(price_asks)*np.array(volume_asks)))/np.sum(volume_asks)

    ppp_bids= np.sum((np.array(price_bids)*np.array(volume_bids)))/np.sum(volume_bids)



    ppp_btc = (ppp_bids + ppp_asks )/ 2

    print('El precio de BTC al', json_response['payload']['updated_at'],'es de  ${:15,.2f} MXN'.format(ppp_btc)  )
    time.sleep(60)


while True:
    btc_value_mxn()