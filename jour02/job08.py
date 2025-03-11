import mysql.connector
import atexit

cnx = mysql.connector.connect(
    host="localhost",      # Adresse du serveur MySQL (localhost si en local)
    user="root",           # Ton nom d'utilisateur MySQL
    password="Adeletdehlia21!",  # Remplace par ton mot de passe MySQL
    database="employe"  # Nom de ta base de données
)

import mysql.connector

class Zoo:
    def __init__(self, host, user, password, database):
        self.cnx = mysql.connector.connect(
            host=host,      # Adresse du serveur MySQL (localhost si en local)
            user=user,      # Ton nom d'utilisateur MySQL
            password=password,  # Remplace par ton mot de passe MySQL
            database=database  # Nom de ta base de données
        )
        self.cursor = self.cnx.cursor()
        atexit.register(self.fermer_connexion)

    def ajouter_cage(self, superficie, capacite):
        query = "INSERT INTO cage (superficie, capacite) VALUES (%s, %s)"
        values = (superficie, capacite)
        self.cursor.execute(query, values)
        self.cnx.commit()

    def ajouter_animal(self, nom, race, id_cage, date_naissance, origine):
        query = "INSERT INTO animal (nom, race, id_cage, date_naissance, origine) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, race, id_cage, date_naissance, origine)
        self.cursor.execute(query, values)
        self.cnx.commit()

    def lister_animaux(self, id_cage=None):
       if id_cage:
        query = "SELECT * FROM animal WHERE id_cage = %s"
        self.cursor.execute(query, (id_cage,))
       else:
        query = "SELECT * FROM animal"
        self.cursor.execute(query)
        
       animaux = self.cursor.fetchall()
       return animaux if animaux else []

    def supprimer_animal(self, id_animal):
        query = "DELETE FROM animal WHERE id = %s"
        self.cursor.execute(query, (id_animal,))
        self.cnx.commit()

    def supprimer_cage(self, id_cage):
        query = "DELETE FROM cage WHERE id = %s"
        self.cursor.execute(query, (id_cage,))
        self.cnx.commit()

    def modifier_animal(self, id_animal, nom=None, race=None, id_cage=None, date_naissance=None, origine=None):
        query = "UPDATE animal SET "
        updates = []
        values = []

        if nom:
            updates.append("nom = %s")
            values.append(nom)
        if race:
            updates.append("race = %s")
            values.append(race)
        if id_cage:
            updates.append("id_cage = %s")
            values.append(id_cage)
        if date_naissance:
            updates.append("date_naissance = %s")
            values.append(date_naissance)
        if origine:
            updates.append("origine = %s")
            values.append(origine)

        if updates:
            query += ", ".join(updates) + " WHERE id = %s"
            values.append(id_animal)
            self.cursor.execute(query, tuple(values))
            self.cnx.commit()

    def superficie_totale(self):
        query = "SELECT SUM(superficie) FROM cage"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else 0

     
    def fermer_connexion(self):
      try:
          if hasattr(self, 'cursor') and self.cursor:
             self.cursor.close()
             self.cursor = None  # Évite de réutiliser une référence supprimée
          if hasattr(self, 'cnx') and self.cnx:
             self.cnx.close()
             self.cnx = None  # Même chose ici
      except Exception as e:
           print(f"erreur ors de la fermeture de la connexion : {e}")
   

def menu(zoo):
    while True:
              print("\nMenu de gestion du zoo")
              print("1. Ajouter une cage")
              print("2. Ajouter un animal")
              print("3. Lister tous les Animaux")
              print("4. Lister les animaux dans une cage")
              print("5. Modifier un animal")
              print("6. Supprimer un animal")
              print("7. Supprime une cage")
              print("8. Calculer la superficie totale des cages")
              print("9. Quitter")

              choix = input("choisissez une option : ")

              if choix == "1":
                      superficie = int(input("Entrez la superficie de la cage : "))
                      capacite = int(input("Entrez la capacité maximale de la cage : "))
                      zoo.ajouter_cage(superficie, capacite)
                      print("Cage ajoutée.")
        
              elif choix == "2":
                       nom = input("Entrez le nom de l'animal : ")
                       race = input("Entrez la race de l'animal : ")
                       id_cage = int(input("Entrez l'ID de la cage de l'animal : "))
                       date_naissance = input("Entrez la date de naissance de l'animal (YYYY-MM-DD) : ")
                       pays_origine = input("Entrez le pays d'origine de l'animal : ")
                       zoo.ajouter_animal(nom, race, id_cage, date_naissance, pays_origine)
                       print("Animal ajouté.")
        
              elif choix == "3":
                       animaux = zoo.lister_animaux()
                       print("Liste des animaux :")
                       for animal in animaux:
                        print(animal)
        
              elif choix == "4":
                       id_cage = int(input("Entrez l'ID de la cage : "))
                       animaux = zoo.lister_animaux(id_cage)
                       print(f"Animaux dans la cage {id_cage} :")
                       for animal in animaux:
                        print(animal)
        
              elif choix == "5":
                       id_animal = int(input("Entrez l'ID de l'animal à modifier : "))
                       nom = input("Entrez le nouveau nom de l'animal (laisser vide pour ne pas changer) : ")
                       race = input("Entrez la nouvelle race de l'animal (laisser vide pour ne pas changer) : ")
                       id_cage = input("Entrez le nouvel ID de la cage de l'animal (laisser vide pour ne pas changer) : ")
                       date_naissance = input("Entrez la nouvelle date de naissance de l'animal (laisser vide pour ne pas changer) : ")
                       pays_origine = input("Entrez le nouveau pays d'origine de l'animal (laisser vide pour ne pas changer) : ")
                       zoo.modifier_animal(id_animal, nom if nom else None, race if race else None,
                                int(id_cage) if id_cage else None, date_naissance if date_naissance else None,
                                pays_origine if pays_origine else None)
                       print("Animal modifié.")
        
              elif choix == "6":
                      id_animal = int(input("Entrez l'ID de l'animal à supprimer : "))
                      zoo.supprimer_animal(id_animal)
                      print("Animal supprimé.")
        
              elif choix == "7":
                     id_cage = int(input("Entrez l'ID de la cage à supprimer : "))
                     zoo.supprimer_cage(id_cage)
                     print("Cage supprimée.")
        
              elif choix == "8":
                     superficie_totale = zoo.superficie_totale()
                     print(f"La superficie totale de toutes les cages est de {superficie_totale} m².")
        
              elif choix == "9":
                   print("Au revoir !")
                   return
 
zoo = Zoo(host="localhost", user="root", password="Adeletdehlia21!", database="zoo")

menu(zoo)