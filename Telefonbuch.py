"""Telefonbuch - Konsolenapplikation."""

from pathlib import Path

DATEI = Path(__file__).resolve().parent / "telefonbuch.txt"
TRENNZEICHEN = ";"

START_EINTRAEGE = """\
Anna;Muster;+41791234567
Luca;Meier;+41449876543
Sofia;Keller;+41785551234
Arja;Hajdari;+41765394255
Jaël;Müller;+41767322515
Denis;Dübendorfer;+41799299277
Joel;Früh;+41792635710
Michael;Fuchs;+41768906743
Reto;Tobler;+41798973673
David;Rechsteiner;+41795693250
Celine;Weil;+41781853079
Noelle;Tanner;+41793675412
Amira;Bachmann;+41793471286
Ben;Widmer;+41786295641
Clara;Suter;+41764182793
Dario;Graf;+41795316842
Elina;Frei;+41782745916
Fabio;Bühler;+41768423175
Giulia;Hofmann;+41794168523
Henrik;Berger;+41787639214
Ida;Wenger;+41762957481
Jan;Kunz;+41795831627
Kim;Arnold;+41784372965
Luis;Marti;+41767184539
Malin;Egli;+41792568147
Nico;Zürcher;+41785719263
Olivia;Stutz;+41763482751
Pascal;Hess;+41796854312
Ria;Ammann;+41781947365
Silas;Frick;+41765291847
Tessa;Blum;+41793726481
Yann;Kaufmann;+41788461529
Alina;Schneider;+41762193754
Basil;Hartmann;+41794856231
Chiara;Vogel;+41785627194
Elias;Schärer;+41763158427
Flavia;Bieri;+41797241683
Gian;Krähenbühl;+41784529371
Jana;Portmann;+41766813725
Levin;Nussbaumer;+41795174286
Mara;Imhof;+41782936514
Sandro;Aebischer;+41767485193
"""


# ---------------------------------------------------------------------------
# Telefonnummern prüfen
# ---------------------------------------------------------------------------

def pruefe_telefonnummer(eingabe):
    """Gibt eine gültige Schweizer Nummer formatiert zurück, sonst ''."""
    nummer = eingabe.replace("(0)", "")

    for zeichen in [" ", "-", "/", ".", "(", ")"]:
        nummer = nummer.replace(zeichen, "")

    if nummer.startswith("+41"):
        nummer = nummer[3:]
    elif nummer.startswith("0041"):
        nummer = nummer[4:]
    elif nummer.startswith("0"):
        nummer = nummer[1:]
    else:
        return ""

    if len(nummer) != 9 or not nummer.isdigit() or nummer.startswith("0"):
        return ""

    return (
        "+41 " + nummer[0:2] + " " + nummer[2:5]
        + " " + nummer[5:7] + " " + nummer[7:9]
    )


# ---------------------------------------------------------------------------
# Datei laden und speichern
# ---------------------------------------------------------------------------

def speichere_eintraege(eintraege):
    """Speichert alle Einträge in telefonbuch.txt."""
    with open(DATEI, "w", encoding="utf-8") as datei:
        for eintrag in eintraege:
            zeile = TRENNZEICHEN.join([
                eintrag["vorname"],
                eintrag["nachname"],
                eintrag["telefon"]
            ])
            datei.write(zeile + "\n")


def lade_eintraege():
    """Lädt vorhandene Einträge oder erstellt die Datei beim ersten Start."""
    if not DATEI.exists():
        eintraege = []

        for zeile in START_EINTRAEGE.splitlines():
            vorname, nachname, telefon = zeile.split(TRENNZEICHEN)
            eintraege.append({
                "vorname": vorname,
                "nachname": nachname,
                "telefon": pruefe_telefonnummer(telefon)
            })

        speichere_eintraege(eintraege)
        return eintraege

    eintraege = []

    with open(DATEI, "r", encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()

            if zeile == "":
                continue

            teile = zeile.split(TRENNZEICHEN)

            if len(teile) != 3:
                print("Warnung: Fehlerhafte Zeile übersprungen:", zeile)
                continue

            eintraege.append({
                "vorname": teile[0],
                "nachname": teile[1],
                "telefon": teile[2]
            })

    return eintraege


# ---------------------------------------------------------------------------
# Eingaben
# ---------------------------------------------------------------------------

def frage_name(bezeichnung, alter_wert=""):
    """Fragt einen gültigen Namen ab. Enter behält beim Bearbeiten den Wert."""
    while True:
        if alter_wert:
            text = input(f"{bezeichnung} [{alter_wert}]: ").strip()
        else:
            text = input(f"{bezeichnung}: ").strip()

        if text == "" and alter_wert:
            return alter_wert

        if text == "":
            print("Fehler: Die Eingabe darf nicht leer sein.")
        elif TRENNZEICHEN in text:
            print("Fehler: Ein Semikolon ist nicht erlaubt.")
        elif any(zeichen.isdigit() for zeichen in text):
            print("Fehler: Ein Name darf keine Ziffern enthalten.")
        else:
            return text


def frage_telefonnummer(alter_wert=""):
    """Fragt eine gültige Schweizer Telefonnummer ab."""
    while True:
        if alter_wert:
            text = input(f"Telefonnummer [{alter_wert}]: ").strip()
        else:
            text = input("Telefonnummer: ").strip()

        if text == "" and alter_wert:
            return alter_wert

        nummer = pruefe_telefonnummer(text)

        if nummer:
            return nummer

        print(
            "Fehler: Keine gültige Schweizer Nummer "
            "(z. B. 079 123 45 67 oder +41 44 123 45 67)."
        )


def frage_eintrag(alter_eintrag=None):
    """Erfragt einen neuen Eintrag oder bearbeitet einen bestehenden."""
    if alter_eintrag is None:
        alter_eintrag = {
            "vorname": "",
            "nachname": "",
            "telefon": ""
        }

    return {
        "vorname": frage_name("Vorname", alter_eintrag["vorname"]),
        "nachname": frage_name("Nachname", alter_eintrag["nachname"]),
        "telefon": frage_telefonnummer(alter_eintrag["telefon"])
    }


# ---------------------------------------------------------------------------
# Anzeigen, Suchen und Auswählen
# ---------------------------------------------------------------------------

def sortier_schluessel(eintrag):
    """Sortiert nach Nachname und dann Vorname."""
    return (
        eintrag["nachname"].casefold(),
        eintrag["vorname"].casefold()
    )


def zeige_eintraege(eintraege):
    """Zeigt die Einträge nummeriert und sortiert an."""
    if not eintraege:
        print("Keine Einträge vorhanden.")
        return

    sortierte_eintraege = sorted(eintraege, key=sortier_schluessel)

    for nummer, eintrag in enumerate(sortierte_eintraege, start=1):
        print(
            f'{nummer}. {eintrag["nachname"]} '
            f'{eintrag["vorname"]}, {eintrag["telefon"]}'
        )


def finde_treffer(eintraege, suchtext):
    """Sucht nach Vorname, Nachname oder Telefonnummer."""
    suchtext_name = suchtext.casefold()
    suchtext_nummer = suchtext.replace(" ", "").replace("-", "")

    treffer = []

    for eintrag in eintraege:
        telefon = eintrag["telefon"].replace(" ", "")
        telefon_national = "0" + telefon[3:]

        if (
            suchtext_name in eintrag["vorname"].casefold()
            or suchtext_name in eintrag["nachname"].casefold()
            or suchtext_nummer in telefon
            or suchtext_nummer in telefon_national
        ):
            treffer.append(eintrag)

    return sorted(treffer, key=sortier_schluessel)


def waehle_eintrag(eintraege, aktion):
    """Sucht einen Eintrag für das Bearbeiten oder Löschen."""
    if not eintraege:
        print("Das Telefonbuch ist leer.")
        return None

    suchtext = input(
        f"Welchen Eintrag möchtest du {aktion}? Suchbegriff: "
    ).strip()

    if suchtext == "":
        print("Abgebrochen.")
        return None

    treffer = finde_treffer(eintraege, suchtext)

    if not treffer:
        print("Kein Eintrag gefunden.")
        return None

    if len(treffer) == 1:
        return treffer[0]

    zeige_eintraege(treffer)

    while True:
        auswahl = input(
            "Nummer des Eintrags (Enter = abbrechen): "
        ).strip()

        if auswahl == "":
            return None

        if auswahl.isdigit() and 1 <= int(auswahl) <= len(treffer):
            return treffer[int(auswahl) - 1]

        print(
            f"Fehler: Bitte eine Zahl zwischen 1 und "
            f"{len(treffer)} eingeben."
        )


# ---------------------------------------------------------------------------
# Menüfunktionen
# ---------------------------------------------------------------------------

def zeige_alle_eintraege(eintraege):
    print("\n--- Alle Einträge ---")
    zeige_eintraege(eintraege)


def erfasse_eintrag(eintraege):
    print("\n--- Neuen Eintrag erfassen ---")
    neuer_eintrag = frage_eintrag()

    if neuer_eintrag in eintraege:
        print("Dieser Eintrag existiert schon.")
        return

    eintraege.append(neuer_eintrag)
    speichere_eintraege(eintraege)
    print("Eintrag gespeichert.")


def suche_eintrag(eintraege):
    print("\n--- Eintrag suchen ---")
    suchtext = input("Suchbegriff (Name oder Nummer): ").strip()

    if suchtext == "":
        print("Fehler: Bitte einen Suchbegriff eingeben.")
        return

    zeige_eintraege(finde_treffer(eintraege, suchtext))


def bearbeite_eintrag(eintraege):
    print("\n--- Eintrag bearbeiten ---")
    eintrag = waehle_eintrag(eintraege, "bearbeiten")

    if eintrag is None:
        return

    print("Enter drücken, um den alten Wert zu behalten.")
    geaenderter_eintrag = frage_eintrag(eintrag)

    if (
        geaenderter_eintrag != eintrag
        and geaenderter_eintrag in eintraege
    ):
        print("Diesen Eintrag gibt es schon. Es wurde nichts geändert.")
        return

    eintrag.update(geaenderter_eintrag)
    speichere_eintraege(eintraege)
    print("Eintrag geändert.")


def loesche_eintrag(eintraege):
    print("\n--- Eintrag löschen ---")
    eintrag = waehle_eintrag(eintraege, "löschen")

    if eintrag is None:
        return

    print(
        "Gewählt:",
        eintrag["vorname"],
        eintrag["nachname"],
        eintrag["telefon"]
    )

    antwort = input("Wirklich löschen? (j/n): ").strip().lower()

    if antwort == "j":
        eintraege.remove(eintrag)
        speichere_eintraege(eintraege)
        print("Eintrag gelöscht.")
    else:
        print("Nicht gelöscht.")


# ---------------------------------------------------------------------------
# Hauptprogramm
# ---------------------------------------------------------------------------

def zeige_menue():
    print("\n===== Telefonbuch =====")
    print("1 - Alle Einträge anzeigen")
    print("2 - Neuen Eintrag erfassen")
    print("3 - Eintrag suchen")
    print("4 - Eintrag bearbeiten")
    print("5 - Eintrag löschen")
    print("0 - Beenden")


def main():
    eintraege = lade_eintraege()

    while True:
        zeige_menue()
        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            zeige_alle_eintraege(eintraege)
        elif wahl == "2":
            erfasse_eintrag(eintraege)
        elif wahl == "3":
            suche_eintrag(eintraege)
        elif wahl == "4":
            bearbeite_eintrag(eintraege)
        elif wahl == "5":
            loesche_eintrag(eintraege)
        elif wahl == "0":
            print("Auf Wiedersehen!")
            break
        else:
            print("Fehler: Bitte eine Zahl von 0 bis 5 eingeben.")


if __name__ == "__main__":
    main()
