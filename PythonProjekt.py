#  Hier wird festgelegt, dass die Kontakte in einer Datei namens telefonbuch.txtgespeichert werden. Sie liegt im gleichen Ordner wie das Programm.
from pathlib import Path
DATEI = Path(__file__).resolve().parent / "telefonbuch.txt"



# Dieser Abschnitt liest die bereits gespeicherten Kontakte aus der Textdatei. Falls die Datei noch nicht existiert, wird sie zuerst erstellt.
def eintraegeLaden():
    eintraege = []

    # "a" erstellt die Datei, falls sie noch nicht existiert.
    with open(DATEI, "a", encoding="utf-8"):
        pass

    with open(DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            teile = zeile.strip().split(";")

            if len(teile) == 3:
                eintrag = {
                    "vorname": teile[0],
                    "nachname": teile[1],
                    "telefon": teile[2]
                }
                eintraege.append(eintrag)

    return eintraege



# Dieser Abschnitt schreibt alle Kontakte in die Textdatei. Änderungen bleiben also auch erhalten, wenn das Programm beendet wird.
def eintragSpeichern(eintraege):
    # "w" schreibt alle Einträge neu. Das ist auch nach
    # dem Bearbeiten oder Löschen eines Eintrags nötig.
    with open(DATEI, "w", encoding="utf-8") as datei:
        for eintrag in eintraege:
            datei.write(
                f'{eintrag["vorname"]};'
                f'{eintrag["nachname"]};'
                f'{eintrag["telefon"]}\n'
            )



# Dieser Abschnitt zeigt alle Kontakte mit einer Nummer an. Wenn keine Kontakte vorhanden sind, erscheint stattdessen eine Meldung.
def eintraegeAnzeigen(eintraege):
    if len(eintraege) == 0:
        print("Das Telefonbuch ist leer.")
        return

    for nummer in range(len(eintraege)):
        eintrag = eintraege[nummer]
        print(
            f'{nummer + 1}) {eintrag["vorname"]} '
            f'{eintrag["nachname"]}: {eintrag["telefon"]}'
        )



# Dieser Abschnitt prüft, ob eine Telefonnummer dem erwarteten Format entspricht. Schweizer Vorwahlen werden dabei berücksichtigt.
def telefonnummerPruefen(eingabe):
    # Einfache Prüfung für Schweizer Nummern, z. B. 079 123 45 67
    # oder +41 79 123 45 67.
    nummer = eingabe.replace(" ", "").replace("-", "")

    if nummer.startswith("+41"):
        nummer = "0" + nummer[3:]
    elif nummer.startswith("0041"):
        nummer = "0" + nummer[4:]

    if len(nummer) == 10 and nummer.isdigit() and nummer.startswith("0"):
        return nummer

    return ""



# Dieser Abschnitt fragt nach Vor- und Nachnamen. Er wiederholt die Frage, wenn die Eingabe nicht erlaubt ist.
def namenEinlesen():
    while True:
        vorname = input("Vorname: ").strip()
        nachname = input("Nachname: ").strip()

        if vorname == "" or nachname == "":
            print("Vorname und Nachname dürfen nicht leer sein.")
        elif ";" in vorname or ";" in nachname:
            print("Ein Semikolon ist im Namen nicht erlaubt.")
        elif any(zeichen.isdigit() for zeichen in vorname + nachname):
            print("Namen dürfen keine Ziffern enthalten.")
        else:
            return vorname, nachname



# Dieser Abschnitt fragt nach einer Telefonnummer. Wenn sie ungültig ist, muss eine neue Eingabe erfolgen.
def telefonnummerEinlesen():
    while True:
        eingabe = input("Telefonnummer: ").strip()
        telefon = telefonnummerPruefen(eingabe)

        if telefon != "":
            return telefon

        print("Ungültige Nummer. Beispiel: 079 123 45 67")



# Dieser Abschnitt erstellt einen neuen Kontakt. Wenn genau dieser Kontakt noch nicht vorhanden ist, wird er hinzugefügt und gespeichert.
def eintragErfassen(eintraege):
    vorname, nachname = namenEinlesen()
    telefon = telefonnummerEinlesen()

    eintrag = {
        "vorname": vorname,
        "nachname": nachname,
        "telefon": telefon
    }

    if eintrag in eintraege:
        print("Dieser Eintrag ist bereits vorhanden.")
        return

    eintraege.append(eintrag)
    eintragSpeichern(eintraege)
    print("Eintrag gespeichert.")



# Dieser Abschnitt sucht nach Kontakten. Man kann dafür einen Namen oder eine Telefonnummer bzw. einen Teil davon eingeben.
def eintragSuchen(eintraege):
    suchtext = input("Name oder Telefonnummer suchen: ").strip().lower()

    if suchtext == "":
        print("Bitte einen Suchbegriff eingeben.")
        return

    gefunden = False

    for eintrag in eintraege:
        if (
            suchtext in eintrag["vorname"].lower()
            or suchtext in eintrag["nachname"].lower()
            or suchtext.replace(" ", "") in eintrag["telefon"]
        ):
            print(
                f'{eintrag["vorname"]} {eintrag["nachname"]}: '
                f'{eintrag["telefon"]}'
            )
            gefunden = True

    if not gefunden:
        print("Kein Eintrag gefunden.")



# In diesem Abschnitt können Sie einen Kontakt anhand seiner angezeigten Nummer auswählen. Das braucht das Programm beim Ändern und Löschen.
def nummerAuswaehlen(eintraege):
    eintraegeAnzeigen(eintraege)

    if len(eintraege) == 0:
        return -1

    eingabe = input("Nummer des Eintrags (Enter = abbrechen): ").strip()

    if eingabe.isdigit():
        nummer = int(eingabe)

        if 1 <= nummer <= len(eintraege):
            return nummer - 1  # Listen beginnen beim Index 0.

    print("Keine gültige Nummer gewählt.")
    return -1



# Dieser Abschnitt ist zum Ändern eines vorhandenen Kontakts da. Du wählst einen Kontakt aus, gibst die neuen Angaben ein und speichert die Änderung.
def eintragEditieren(eintraege):
    nummer = nummerAuswaehlen(eintraege)

    if nummer == -1:
        return

    print("Neue Angaben eingeben:")
    vorname, nachname = namenEinlesen()
    telefon = telefonnummerEinlesen()

    neuer_eintrag = {
        "vorname": vorname,
        "nachname": nachname,
        "telefon": telefon
    }

    if neuer_eintrag in eintraege and neuer_eintrag != eintraege[nummer]:
        print("Dieser Eintrag ist bereits vorhanden.")
        return

    eintraege[nummer] = neuer_eintrag
    eintragSpeichern(eintraege)
    print("Eintrag geändert.")



# Dieser Abschnitt löscht einen ausgewählten Kontakt. Zuerst fragt das Programm zur Sicherheit, ob du ihn wirklich löschen möchtest.
def eintragLoeschen(eintraege):
    nummer = nummerAuswaehlen(eintraege)

    if nummer == -1:
        return

    antwort = input("Eintrag wirklich löschen? (j/n): ").strip().lower()

    if antwort == "j":
        eintraege.pop(nummer)
        eintragSpeichern(eintraege)
        print("Eintrag gelöscht.")
    else:
        print("Nicht gelöscht.")



# Dieser Abschnitt ordnet jeder Zahl im Menü die passende Aktion zu. Bei einer anderen Eingabe meldet er, dass die Auswahl ungültig ist.
def menuSelektion(wahl, eintraege):
    match wahl:
        case "1":
            eintraegeAnzeigen(eintraege)
        case "2":
            eintragErfassen(eintraege)
        case "3":
            eintragSuchen(eintraege)
        case "4":
            eintragEditieren(eintraege)
        case "5":
            eintragLoeschen(eintraege)
        case "6":
            print("Auf Wiedersehen!")
        case _:
            print("Ungültige Menüwahl.")



# Das ist der Hauptablauf des Programms. Die Kontakte werden geladen und das Menü wird immer wieder angezeigt, bis Sie 6zum Beenden wählen.
def main():
    eintraege = eintraegeLaden()
    wahl = ""

    while wahl != "6":
        print("\n--- Telefonbuch ---")
        print("1) Alle Einträge anzeigen")
        print("2) Neuen Eintrag erfassen")
        print("3) Eintrag suchen")
        print("4) Eintrag editieren")
        print("5) Eintrag löschen")
        print("6) Beenden")

        wahl = input("Wähle eine Zahl von 1 bis 6: ").strip()
        menuSelektion(wahl, eintraege)



# Dieser letzte Abschnitt beginnt den Hauptablauf, wenn du die Python-Datei ausführst.
if __name__ == "__main__":
    main()


    