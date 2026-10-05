# Projektplanung – Telefonbuch

## Ziel und Erfolgskriterien

Wir entwickeln zu zweit innerhalb von fünf Tagen eine Python-Konsolenapplikation für ein Telefonbuch. Beim Start erscheint ein Hauptmenü. Einträge können angezeigt, erfasst, gesucht, bearbeitet und gelöscht werden.

Das Projekt ist fertig, wenn:
- jeder Eintrag einen Vor- und Nachnamen sowie eine gültige Schweizer Telefonnummer enthält;
- die Einträge in einer `.txt`-Datei im Projektordner gespeichert und nach einem Neustart wieder geladen werden;
- ungültige Eingaben abgefangen werden, ohne dass das Programm abstürzt;
- beide den gesamten Code verstehen und erklären können.

Eine Funktion gilt als fertig, wenn wir sie mit normalen und fehlerhaften Eingaben getestet haben. Bei Änderungen an Einträgen prüfen wir zusätzlich, ob die Daten nach einem Neustart noch stimmen.

## Technische Entscheidungen

- Ein Eintrag wird im Programm als Dictionary mit `vorname`, `nachname` und `telefonnummer` dargestellt.
- Die Einträge werden in einer Liste verwaltet und als JSON-Text in `telefonbuch.txt` gespeichert.
- Vor- und Nachname dürfen nicht leer sein. Telefonnummern prüfen wir nach einem gemeinsam festgelegten Schweizer Format, z. B. `079 123 45 67` oder `+41 79 123 45 67`.
- Das Programm wird in kleine Funktionen für Menü, Eingabeprüfung, Suchen, Bearbeiten, Löschen sowie Speichern und Laden aufgeteilt.

## Aufgaben nach Priorität

**Must**
- [ ] Repository anlegen und diese Planung gemeinsam prüfen
- [ ] Kleines lauffähiges Programm mit Hauptmenü erstellen
- [ ] Einträge als `.txt`-Datei speichern und beim Start laden
- [ ] Einträge anzeigen und erfassen
- [ ] Einträge suchen, bearbeiten und löschen
- [ ] Leere und ungültige Eingaben abfangen
- [ ] Alle Funktionen und das erneute Laden der Daten testen

**Should**
- [ ] Code gegenseitig prüfen und verständliche Namen und Kommentare ergänzen
- [ ] Hilfreiche Meldungen für leeres Telefonbuch und erfolglose Suche ergänzen

**Could**
- [ ] Zusätzliche Angaben pro Eintrag ermöglichen

## Zusammenarbeit

- Person A: **[Name]** – zunächst Menü, Anzeige und Erfassung
- Person B: **[Name]** – zunächst Datei-Speicherung, Laden und Eingabeprüfung
- Suchen, Bearbeiten, Löschen und Tests teilen wir nach Fortschritt auf.
- Wir arbeiten in eigenen Git-Branches, prüfen die Änderungen gegenseitig und führen sie über Pull Requests zusammen.
- Wir stimmen uns täglich kurz zu Fortschritt, Problemen und den nächsten Aufgaben ab.
- Beide ändern einmal gleichzeitig `Projektplanung.md` in eigenen Branches. Danach führen wir die Änderungen zusammen und lösen einen möglichen Git-Konflikt gemeinsam.

## Zeitplan

- **Tag 1:** Planung, technische Entscheidungen, Repository und lauffähiges Hauptmenü
- **Tag 2:** Einträge erfassen, anzeigen, speichern und laden
- **Tag 3:** Suchen, Bearbeiten und Löschen
- **Tag 4:** Eingabefehler abfangen, Tests und Fehlerbehebung
- **Tag 5:** Code prüfen, letzte Tests, Dokumentation und Abgabe

Am Ende jedes Tages prüfen wir, was funktioniert, was noch offen ist und ob wir die Aufgabenliste anpassen müssen.

## Planung Jaël

Kommt hier hin
