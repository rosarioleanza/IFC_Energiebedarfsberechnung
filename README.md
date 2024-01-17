# IFC_Energiebedarfsberechnung
Mit diesem Tool, ist es möglich einen IFC reinzuladen mit den gesetzten Raumkategorien und damit wird der Energiebedarf anhand von SIA2056 ermittelt. Dieses Tool dient als Hilfestellung bei einer frühen Phase des Projekts um den Energie- und Leistungsbedarf zu ermitteln und Stromleitungen etc. zu Dimensionieren.

IFC Energiebedarfsberechnung mit SIA 2056 - Rosario Leanza - HSLU HS23

1. Inhalt Abgabe 

Im ZIP Ordner „MEP Abgabe Rosario Leanza DC_SCRIPT“ sind verschiedene Ordner und Dateien vorhanden:
- dieses „readme“ file
- Modulabschluss Poster
- SIA 2056 (Grundlage des Programms)
- Dokumentation / Präsentation
- Ordner „Programm“ (Python Files, Excel Tabellen und Logo)
- Ordner „Beispieldateien“ Mit Beispielbilder und eines der exportierten PDFs vom Programm
- Ordner „Funktionsfähige IFC-Files“ (IFC-Files welche im Programm funktionieren)

Zunächst dieses ZIP Ordner an gewünschte Stelle entpacken.

Diese Programm wurde mit Python 3.11.5 auf MacOS Sonoma 14.2 entwickelt und getestet. Python 3.12 ist nicht kompatibel, da gewisse Module noch nicht unter 3.12 funktionieren.

Die zu installierenden und benutzten Module sind:

Customtkinter
Tkinter
Os
Numpy
Pandas
Matplotlib
fpdf
Ifcopenshell





2. Vorbereitung (einmalig bei Installation)

Bevor das Programm an einem neuen / anderen PC benutzt werden kann müssen zuerst gewissen Anpassungen in den Code gemacht werden (nur einmalig). Im Ordner „Programm befinden sich drei Python files,  main.py ; gui.py ; functions.py. Diese im Microsoft Visual Studio code öffnen (oder in ein beliebiges Programm). In diese Files befinden sich viele # Kommentare, welche genau beschreiben, was der Codes genau macht.
Main.py ist die Ausführung des Programms, immer diesen ausführen bei Benutzung.
Gui.py ist die grafische Darstellung und Benutzeroberfläche des Programms.
Functions.py ist der ganze Gehirn des Programms, hier sind alle Funktionen und mathematische Kalkulationen hinterlegt, die im Programm genutzt werden.

In Gui.py muss zunächst bei Zeile 29 der Dateipfad des logo_image aktualisiert werden, da auf einem neuen Computer der Dateipfad anders ist.

In functions.py muss hingegen bei Zeile 7 der Dateipfad für die Raumnutzungsdaten aktualisiert werden, da auf einem neuen Computer der Dateipfad anders ist.





3. Benutzung des Programms

Nun main.py ausführen und das Programm ist funktionstüchtig. Das IFC-File aus dem Ordner „funktionsfähige IFC-Files auswählen, eigenen Strompreis und PV-Konfigurationen eingeben und auf berechnen drücken. Das ist beliebig änderbar, einfach andere Datei auswählen und Zahlen und erneut auf Berechnen drücken. Das Programm wird automatisch aktualisiert, ohne dass es geschlossen werden muss um eine neue berechnung durchzuführen.

Zum Schluss PDF Exportieren und dieser wird auch im Ordner „Programm“ exportiert. Der Inhalt des PDFs ist das gleiche wie beim Programm. Also alle Berechnungen, Lösungen und Diagramme sind darin enthalten.


Rosario Leanza

