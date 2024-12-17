from django.contrib.auth import get_user_model
from managefee.models import Subscription, Fee
from django.utils import timezone
import random
from datetime import datetime

CustomUser = get_user_model()

def create_test_data():
    # Créer les souscriptions pour chaque mois de l'année en cours
    year = timezone.now().year
    subscriptions = []
    
    MONTHS = [
        "JANVIER", "FEVRIER", "MARS", "AVRIL", "MAI", "JUIN",
        "JUILLET", "AOUT", "SEPTEMBRE", "OCTOBRE", "NOVEMBRE", "DECEMBRE"
    ]
    
    # Créer ou récupérer les souscriptions pour chaque mois
    for month in MONTHS:
        sub, created = Subscription.objects.get_or_create(
            plan=month,
            year=year
        )
        subscriptions.append(sub)

    # Créer 100 utilisateurs
    for i in range(100):
        # Générer un nom d'utilisateur unique
        username = f'user{i+1}'
        
        # Choisir un bloc aléatoire
        bloc = f'b{random.randint(1, 10)}'
        
        # Choisir une mensualité aléatoire (500, 1000, 1500 ou 2000)
        monthly_fee = random.choice([500, 1000, 1500, 2000])
        
        # Créer l'utilisateur
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password='admin',  # Mot de passe par défaut
                email=f'{username}@example.com',
                bloc=bloc,
                feecharge=monthly_fee,
                has_changed_password=False
            )
            
            # Générer des paiements aléatoires pour certains mois
            # Choisir aléatoirement combien de mois ont été payés (entre 0 et 12)
            months_paid = random.sample(subscriptions, random.randint(0, 12))
            
            for subscription in months_paid:
                # Créer un paiement pour ce mois
                payment_date = datetime(year, MONTHS.index(subscription.plan) + 1, 
                                     random.randint(1, 28))
                
                Fee.objects.create(
                    user=user,
                    subscription=subscription,
                    date=payment_date,
                    amount=monthly_fee
                )
            
            print(f"Utilisateur créé : {username} (Bloc: {bloc}, Mensualité: {monthly_fee}DA)")
            
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur {username}: {str(e)}")

    print("Création des données de test terminée!")

# Pour exécuter le script, utilisez cette fonction dans un shell Django :
# from managefee.test_data import create_test_data
# create_test_data()