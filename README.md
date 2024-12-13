# Infrascout
please note that this version might have limited functionality espicially when trying to download the report. This is because the tool is meant for internal use and while hosted on github, there is no option to add the executable files so you will need to do it yourselves via this link https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf.

 Detaillierte Schritt-für-Schritt-Anleitung zur Nutzung von Infrascout

Schritt 1: Anwendung starten
Öffnen Sie Infrascout über den folgenden Link:
Infrascout2.streamlit.app
Stellen Sie sicher, dass Sie eine stabile Internetverbindung haben, um die Funktionen optimal nutzen zu können.
Machen Sie sich mit der Benutzeroberfläche vertraut, die vier Hauptregisterkarten enthält:
Parameter festlegen
Daten hochladen
Analyse anzeigen
Bericht generieren
Hinweis: Diese Webversion von Infrascout dient als Proof of Concept.
Einige Funktionen (z. B. das Generieren und Herunterladen von PDF-Berichten) sind möglicherweise eingeschränkt.
Weitere Informationen oder Lösungsvorschläge finden Sie in der GitHub-README-Datei.

Schritt 2: Parameter festlegen
Wechseln Sie zur Registerkarte Parameter festlegen.
Geben Sie den Namen der Stadt ein, die Sie analysieren möchten (z. B. Bern, Schweiz).
Dies ist der geografische Bereich, für den die Infrastruktur analysiert wird.
Achten Sie darauf, dass der Stadtname korrekt geschrieben ist.
Passen Sie den Bevölkerungsdichte-Schwellenwert mit dem Schieberegler an:
Bestimmt die Mindestbevölkerungsdichte für Bereiche, die analysiert werden sollen.
Legen Sie den Proximity Threshold (in Metern) fest:
Definiert, wie weit die bestehende Infrastruktur entfernt sein darf, um einen Bereich als abgedeckt zu betrachten.
Wählen Sie die Infrastrukturtypen, die Sie analysieren möchten:
Beispiele sind Bänke, Toiletten, Abfallkörbe, Bushaltestellen, Trinkbrunnen usw.
Die Software konzentriert sich während der Analyse auf diese spezifischen Typen.

Schritt 3: Datenquelle wählen
Wechseln Sie zur Registerkarte Daten hochladen.
Wählen Sie aus, wie Sie Infrastrukturdaten eingeben möchten:
Option 1: Daten aus OpenStreetMap abrufen
Klicken Sie auf die Schaltfläche "Daten aus OpenStreetMap abrufen".
Die Software sammelt automatisch bestehende Infrastrukturdaten für die ausgewählte Stadt.
Stellen Sie sicher, dass die ausgewählten Infrastrukturtypen Ihren Präferenzen entsprechen.
Option 2: Eigene Daten hochladen
Laden Sie Ihre eigenen CSV- oder GPKG-Dateien mit Infrastrukturdaten hoch.
Beispiele für Infrastrukturen: Bushaltestellen, Parks, Spielplätze usw.
Stellen Sie sicher, dass Ihre Dateien die richtigen Spalten wie Längengrad, Breitengrad oder Geometrie enthalten.

Schritt 4: Bevölkerungs- und Verkehrsdatensätze hochladen
Bleiben Sie auf der Registerkarte Daten hochladen:
Laden Sie mindestens eine CSV-Datei mit Bevölkerungsdaten hoch, die die Bevölkerungsdichte enthält. *Das ist obligatorisch,Verkehrsdaten undLuftqualitätsdaten sind optional

Diese Datensätze sind entscheidend für die Analyse:
Bevölkerungsdichte: Identifiziert Bereiche mit hoher Bevölkerungsdichte, die Infrastruktur benötigen.
Verkehrsdaten: Priorisiert stark frequentierte Bereiche für die Analyse.
Wenn Sie keine Beispiel-Daten haben, laden Sie diese aus unserem GitHub-Repository herunter.

Schritt 5: Analyse ausführen
Wechseln Sie zur Registerkarte Analyse anzeigen.
Klicken Sie auf die Schaltfläche "Analyse ausführen".
Die Software bewertet Bereiche mit unzureichender Infrastruktur basierend auf:
Bevölkerungsdichte: Markiert unterversorgte Bereiche mit hoher Bevölkerung.
Nähe zu bestehender Infrastruktur: Identifiziert Lücken in der Abdeckung.
Verkehrsdaten: Priorisiert stark frequentierte Zonen.
Überprüfen Sie die vorgeschlagenen Infrastrukturlocations:
Eine Tabelle zeigt die vorgeschlagenen Standorte mit Typ, Koordinaten und Bevölkerungsdichte.
Visualisierte Punkte erscheinen auf einer interaktiven Karte.

Schritt 6: Ergebnisse anzeigen
Erkunden Sie die vorgeschlagenen Standorte auf der interaktiven Karte:
Zoomen Sie hinein, um eine detaillierte Ansicht der Standorte zu erhalten.
Bewegen Sie den Mauszeiger über Punkte, um weitere Informationen wie Infrastrukturtyp und Koordinaten anzuzeigen.
Überprüfen Sie die geschätzten Kosten für die Umsetzung der empfohlenen Infrastruktur:
Die Kosten basieren auf den in Schritt 2 ausgewählten Infrastrukturtypen.
Nutzen Sie diese Informationen zur Erstellung von Projektbudgets.

Schritt 7: Bericht erstellen
Wechseln Sie zur Registerkarte Bericht erstellen.
Geben Sie Feedback zu den vorgeschlagenen Standorten im entsprechenden Feld ein.
Ihr Feedback wird im finalen Bericht enthalten sein.
Klicken Sie auf "PDF-Bericht herunterladen", um einen detaillierten Bericht zu erstellen:
Der Bericht enthält die vorgeschlagenen Standorte, geschätzte Kosten und Ihr Feedback.
Hinweis:
Die Webversion kann Einschränkungen beim PDF-Generieren haben.
Weitere Informationen und einen Beispielbericht finden Sie in unserem GitHub-Profil.

Tipps für eine effektive Nutzung
Stellen Sie sicher, dass hochgeladene Dateien genaue und saubere Daten enthalten, um Fehler während der Analyse zu vermeiden.
Für manuelle Uploads bestätigen Sie, dass das Dateiformat den Anforderungen entspricht (z. B. CSV oder GPKG mit den richtigen Spalten).
Überprüfen Sie immer die Genauigkeit der aus OpenStreetMap abgerufenen Infrastrukturdaten.
Für eine bessere Verständnis schauen Sie sich unser Video-Tutorial auf Showroom an.
