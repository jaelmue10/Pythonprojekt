# Funktionen

def menuSelektion(x):
    match x:
        case 1:
         eintraegeAnzeigen()
        case 2:
         eintragErfassen()
        case 3:
         eintragSpeichern()
        case 4:
         eintragEditieren()
        case 5:
         eintragLöschen
        case 6:
         beenden()
        case _:
            print("ungültige Menüwahl")


def eintraegeAnzeigen():
   print("Einträge anzeigen")
   # TODO: Fertigstellen

def eintragErfassen():
   print("Eintrag erfassen")
   # TODO: Fertigstellen

def eintragSpeichern():
   print("Eintrag speichern")

def eintragEditieren():
   print("Eintrag editieren")

def eintragLöschen():
   print("Eintrag löschen")

def beenden():
   print("fertig")

# Telefonbuch Programm

menuEingabe = 0

while menuEingabe != 6:
   print("1) Alle Einträge des Telefonbuches anzeigen.")
   print("2) Einen neuen Eintrag im Telefonbuch erfassen.")
   print("3) Nach eine Eintrag suchen.")
   print("4) Einen bestehenden Eintrag im Telefonbuch editieren.")
   print("5) Einen bestehenden Eintrag löschen.")
   print("6) beenden")

   menuEingabe = int(input("Gib eine Zahl zwiscchen 1 und 6 ein:"))

   menuSelektion(menuEingabe)
