from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Hier wird festgelegt, dass die Kontakte in einer Datei namens telefonbuch.txt
# gespeichert werden. Sie liegt im gleichen Ordner wie das Programm.
DATEI = Path(__file__).resolve().parent / "telefonbuch.txt"


# Diese Ausnahme zeigt an, dass eine Aktion mit 7 abgebrochen wurde.
class AktionAbgebrochen(Exception):
    pass



# Diese Funktion wird für alle Eingaben während einer Aktion verwendet.
# Bei der Eingabe 7 wird die aktuelle Aktion abgebrochen.
def eingabeLesen(frage):
    antwort = input(frage).strip()

    if antwort == "7":
        raise AktionAbgebrochen

    return antwort



# Dieser Abschnitt liest die bereits gespeicherten Kontakte aus der Textdatei.
# Falls die Datei noch nicht existiert, wird sie zuerst erstellt.
def eintraegeLaden():
    eintraege = []

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



# Dieser Abschnitt schreibt alle Kontakte in die Textdatei.
# Auch nach dem Bearbeiten oder Löschen werden alle Einträge neu geschrieben.
def eintragSpeichern(eintraege):
    with open(DATEI, "w", encoding="utf-8") as datei:
        for eintrag in eintraege:
            datei.write(
                f'{eintrag["vorname"]};'
                f'{eintrag["nachname"]};'
                f'{eintrag["telefon"]}\n'
            )



# Dieser Abschnitt zeigt alle Kontakte mit einer Nummer an.
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



# Dieser Abschnitt prüft das grundlegende Format einer Schweizer Telefonnummer.
def telefonnummerPruefen(eingabe):
    nummer = eingabe.replace(" ", "").replace("-", "")

    if nummer.startswith("+41"):
        nummer = "0" + nummer[3:]
    elif nummer.startswith("0041"):
        nummer = "0" + nummer[4:]

    if len(nummer) == 10 and nummer.isdigit() and nummer.startswith("0"):
        return nummer

    return ""



# Dieser Abschnitt fragt nach Vor- und Nachnamen.
# Mit 7 kann die Eingabe jederzeit abgebrochen werden.
def namenEinlesen():
    while True:
        vorname = eingabeLesen("Vorname (7 = abbrechen): ")
        nachname = eingabeLesen("Nachname (7 = abbrechen): ")

        if vorname == "" or nachname == "":
            print("Vorname und Nachname dürfen nicht leer sein.")
        elif len(vorname) > 50 or len(nachname) > 50:
            print("Vorname und Nachname dürfen höchstens 50 Zeichen lang sein.")
        elif ";" in vorname or ";" in nachname:
            print("Ein Semikolon ist im Namen nicht erlaubt.")
        elif any(zeichen.isdigit() for zeichen in vorname + nachname):
            print("Namen dürfen keine Ziffern enthalten.")
        else:
            return vorname, nachname



# Dieser Abschnitt fragt nach einer Telefonnummer.
# Bei 7 wird abgebrochen, ohne den angefangenen Kontakt zu speichern.
def telefonnummerEinlesen():
    
    while True:
        eingabe = eingabeLesen("Telefonnummer (7 = abbrechen): ")
        telefon = telefonnummerPruefen(eingabe)

        if telefon != "":
            return telefon

        print("Ungültige Nummer. Beispiel: 079 123 45 67")



# Dieser Abschnitt erstellt einen neuen Kontakt.
# Gespeichert wird erst, wenn alle Angaben vollständig eingegeben wurden.
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

    

# Dieser Abschnitt sucht nach Namen oder nach dem Anfang einer Telefonnummer.
# Leerzeichen und Bindestriche in gespeicherten Nummern werden bei der Suche
# nicht berücksichtigt. Auch Nummern mit +41 oder 0041 können gefunden werden.
def eintragSuchen(eintraege):
    suchtext = eingabeLesen(
        "Name oder Anfang der Telefonnummer suchen (7 = abbrechen): "
    ).lower()

    if suchtext == "":
        print("Bitte einen Suchbegriff eingeben.")
        return

    # Leerzeichen und Bindestriche werden aus der Suche entfernt.
    nummernsuche = suchtext.replace(" ", "").replace("-", "")
    gefunden = False

    for eintrag in eintraege:
        if nummernsuche.isdigit():
            # Die gespeicherte Telefonnummer wird für den Vergleich vereinheitlicht.
            telefon = eintrag["telefon"].replace(" ", "").replace("-", "")

            if telefon.startswith("+41"):
                telefon = "0" + telefon[3:]
            elif telefon.startswith("0041"):
                telefon = "0" + telefon[4:]

            passt = telefon.startswith(nummernsuche)
        else:
            passt = (
                suchtext in eintrag["vorname"].lower()
                or suchtext in eintrag["nachname"].lower()
            )

        if passt:
            print(
                f'{eintrag["vorname"]} {eintrag["nachname"]}: '
                f'{eintrag["telefon"]}'
            )
            gefunden = True

    if not gefunden:
        print("Kein Eintrag gefunden.")



# In diesem Abschnitt wird ein Kontakt anhand seiner Nummer ausgewählt.
# Mit Enter oder 7 kommt man zum Menü zurück.
def nummerAuswaehlen(eintraege):
    eintraegeAnzeigen(eintraege)

    if len(eintraege) == 0:
        return -1

    eingabe = eingabeLesen(
        "Nummer des Eintrags (Enter oder 7 = abbrechen): "
    )

    if eingabe == "":
        return -1

    if eingabe.isdigit():
        nummer = int(eingabe)

        if 1 <= nummer <= len(eintraege):
            return nummer - 1  # Listen beginnen beim Index 0.

    print("Keine gültige Nummer gewählt.")
    return -1



# Dieser Abschnitt ändert einen vorhandenen Kontakt.
# Der alte Eintrag bleibt erhalten, wenn bei einer Eingabe 7 gedrückt wird.
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



# Dieser Abschnitt löscht einen Kontakt erst nach einer Bestätigung.
# Mit 7 kann auch die Bestätigung abgebrochen werden.
def eintragLoeschen(eintraege):
    nummer = nummerAuswaehlen(eintraege)

    if nummer == -1:
        return

    while True:
        antwort = eingabeLesen(
            "Eintrag wirklich löschen? (j/n, 7 = abbrechen): "
        ).lower()

        if antwort == "j":
            eintraege.pop(nummer)
            eintragSpeichern(eintraege)
            print("Eintrag gelöscht.")
            return

        if antwort == "n":
            print("Nicht gelöscht.")
            return

        print("Bitte j, n oder 7 eingeben.")



# Dieser Abschnitt ordnet jeder Zahl im Menü die passende Aktion zu.
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
        case "7":
            print("Du bist bereits im Hauptmenü.")


def menueAnzeigen():
    console.clear()

    # Kopfzeile
    kopf = Text()
    kopf.append("  T E L E F O N B U C H  ", style="bold bright_white")
    kopf.append(" /  KONTAKTE", style="bold bright_cyan")

    console.print()
    console.print(
        Panel(
            kopf,
            border_style="bright_cyan",
            width=54,
            padding=(1, 1),
        )
    )

    # Menü
    menue = Text()
    menue.append("  HAUPTMENÜ\n", style="bold bright_cyan")
    menue.append("  ─────────────────────────────────────────\n\n", style="dim cyan")

    punkte = [
        ("1", "ANZEIGEN",   "Alle Kontakte ansehen"),
        ("2", "ERFASSEN",   "Neuen Kontakt speichern"),
        ("3", "SUCHEN",     "Kontakt schnell finden"),
        ("4", "BEARBEITEN", "Kontakt ändern"),
        ("5", "LÖSCHEN",    "Kontakt entfernen"),
    ]

    for nummer, titel, beschreibung in punkte:
        menue.append("  [ ", style="dim cyan")
        menue.append(nummer, style="bold bright_yellow")
        menue.append(" ]  ", style="dim cyan")
        menue.append(f"{titel:<12}", style="bold white")
        menue.append(f" {beschreibung}\n", style="dim")

    menue.append("\n  ─────────────────────────────────────────\n", style="dim cyan")
    menue.append("  [ ", style="dim cyan")
    menue.append("6", style="bold bright_yellow")
    menue.append(" ]  ", style="dim cyan")
    menue.append("BEENDEN", style="bold bright_red")
    menue.append("      Programm verlassen\n", style="dim")

    console.print(
        Panel(
            menue,
            border_style="cyan",
            width=54,
            padding=(1, 1),
        )
    )

    # Kurzer Hinweis statt zusätzlicher Menü-Kachel
    hinweis = Text()
    hinweis.append("  STATUS  ", style="bold bright_green")
    hinweis.append("Bereit", style="green")
    hinweis.append("     |     ", style="dim")
    hinweis.append("7", style="bold yellow")
    hinweis.append(" = Aktion abbrechen", style="dim")

    console.print(hinweis)
    console.print()


# Das ist der Hauptablauf. Ein Abbruch mit 7 wird hier aufgefangen,
# damit das Hauptmenü wieder angezeigt wird.
def main():
    eintraege = eintraegeLaden()
    wahl = ""

    while wahl != "6":
        menueAnzeigen()
        wahl = input("Deine Wahl (1–7): ").strip()

        if wahl not in {"1", "2", "3", "4", "5", "6", "7"}:
            print("Bitte gib eine Zahl von 1 bis 7 ein.")
            continue

        try:
            menuSelektion(wahl, eintraege)
        except AktionAbgebrochen:
            print("Aktion abgebrochen. Es wurde nichts geändert.")



# Dieser Abschnitt fragt nach einer freiwilligen Adresse.
# Mit Enter bleibt die Adresse leer. Mit 7 wird die Aktion abgebrochen.
def adresseEinlesen():
    while True:
        adresse = eingabeLesen(
            "Adresse (optional, Enter = leer, 7 = abbrechen): "
        )

        # Das Semikolon trennt die Angaben in der Textdatei.
        # Deshalb darf es nicht in der Adresse vorkommen.
        if ";" in adresse:
            print("Ein Semikolon ist in der Adresse nicht erlaubt.")
        elif len(adresse) > 200:
            print("Die Adresse darf höchstens 200 Zeichen lang sein.")
        else:
            return adresse



# Dieser Abschnitt liest Kontakte mit und ohne Adresse aus der Textdatei.
# Bereits gespeicherte Kontakte ohne Adresse bleiben dadurch erhalten.
def eintraegeLaden():
    eintraege = []

    with open(DATEI, "a", encoding="utf-8"):
        pass

    with open(DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            teile = zeile.rstrip("\n").split(";")

            # Alte Einträge haben drei Angaben, neue Einträge vier.
            if len(teile) in (3, 4):
                eintrag = {
                    "vorname": teile[0],
                    "nachname": teile[1],
                    "telefon": teile[2],
                    "adresse": teile[3] if len(teile) == 4 else ""
                }
                eintraege.append(eintrag)

    return eintraege



# Dieser Abschnitt speichert alle Kontakte mit einem zusätzlichen
# Feld für die Adresse. Das Feld darf auch leer sein.
def eintragSpeichern(eintraege):
    with open(DATEI, "w", encoding="utf-8") as datei:
        for eintrag in eintraege:
            datei.write(
                f'{eintrag["vorname"]};'
                f'{eintrag["nachname"]};'
                f'{eintrag["telefon"]};'
                f'{eintrag["adresse"]}\n'
            )



# Dieser Abschnitt zeigt die Adresse nur an, wenn eine eingetragen wurde.
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

        if eintrag["adresse"]:
            print(f'   Adresse: {eintrag["adresse"]}')



# Dieser Abschnitt erstellt einen Kontakt mit einer freiwilligen Adresse.
# Gespeichert wird erst, wenn alle Eingaben abgeschlossen sind.
def eintragErfassen(eintraege):
    vorname, nachname = namenEinlesen()
    telefon = telefonnummerEinlesen()
    adresse = adresseEinlesen()

    eintrag = {
        "vorname": vorname,
        "nachname": nachname,
        "telefon": telefon,
        "adresse": adresse
    }

    if eintrag in eintraege:
        print("Dieser Eintrag ist bereits vorhanden.")
        return

    eintraege.append(eintrag)
    eintragSpeichern(eintraege)
    print("Eintrag gespeichert.")



# Dieser Abschnitt ändert einen Kontakt und fragt auch nach der Adresse.
# Bei 7 bleibt der bisherige Kontakt unverändert.
# Mit Enter wird eine bisherige Adresse entfernt.
def eintragEditieren(eintraege):
    nummer = nummerAuswaehlen(eintraege)

    if nummer == -1:
        return

    print("Neue Angaben eingeben:")
    vorname, nachname = namenEinlesen()
    telefon = telefonnummerEinlesen()
    adresse = adresseEinlesen()

    neuer_eintrag = {
        "vorname": vorname,
        "nachname": nachname,
        "telefon": telefon,
        "adresse": adresse
    }

    if neuer_eintrag in eintraege and neuer_eintrag != eintraege[nummer]:
        print("Dieser Eintrag ist bereits vorhanden.")
        return

    eintraege[nummer] = neuer_eintrag
    eintragSpeichern(eintraege)
    print("Eintrag geändert.")

# Dieser letzte Abschnitt startet das Programm.
if __name__ == "__main__":
    main()

