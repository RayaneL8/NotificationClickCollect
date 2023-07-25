from plyer import notification
import time
import requests
from datetime import datetime, timedelta
import os

#CLE SECRETE D'ADMIN
SHARED_SECRET = os.environ.get('SHARED_SECRET')

#CLE API
API_KEY = os.environ.get('API_KEY')

#[ADRESSE] : Contient l'adresse de l'api pour récupérer une liste de commandes
URL_ORDERS = "https://%s:%s@souk-dubai-1400.myshopify.com/admin/api/2023-07/orders.json?status=open" % (API_KEY, SHARED_SECRET)





def get_200_orders(heure):
    r = requests.get(URL_ORDERS+"&limit=200&created_at_min="+str(heure)).json()
    return r


def envoyer_notification(titre, message):
    notification.notify(
        title=titre,
        message=message,
        app_icon=None,  
        timeout=10000, 
    )


while(True):
  b = True
  # Obtenir l'heure actuelle
  time_now = datetime.now()

  # Formater l'heure actuelle au format "Date - Heure"
  time_now_formatted = time_now.strftime("%d-%m-%Y - %H:%M")

  # Définir un décalage d'une heure (timedelta de -2h , -5m)
  time_lag = timedelta(hours=-2,minutes=-5)

  # Calculer la nouvelle heure en ajoutant le décalage
  time_f = time_now + time_lag

  # Formater la nouvelle heure au format ISO 8601 avec heure et code horaire
  time_f_iso8601 = time_f.strftime("%Y-%m-%dT%H:%M:%S%z")


  orders = get_200_orders(time_f_iso8601)
  for p in orders["orders"]:
    for ps in p["shipping_lines"]:
      if (ps["code"] == "Villepinte"):
        b = False
        titre_notification = "Nouveau Click & Collect"
        message_notification = ("Commande n°"+str(p["name"]))
        envoyer_notification(titre_notification, message_notification)
  if b :
    print("Pas de nouveaux click & collect à : "+str(time_now_formatted))


  time.sleep(295)