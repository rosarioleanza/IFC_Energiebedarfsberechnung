IFC Energiebedarfsberechnung mit SIA 2056 - Rosario Leanza - HSLU HS23

1. Inhalt Abgabe 

Im ZIP Ordner �MEP Abgabe Rosario Leanza DC_SCRIPT� sind verschiedene Ordner und Dateien vorhanden:
- dieses �readme� file
- Modulabschluss Poster
- SIA 2056 (Grundlage des Programms)
- Dokumentation / Pr�sentation
- Ordner �Programm� (Python Files, Excel Tabellen und Logo)
- Ordner �Beispieldateien� Mit Beispielbilder und eines der exportierten PDFs vom Programm
- Ordner �Funktionsf�hige IFC-Files� (IFC-Files welche im Programm funktionieren)

Zun�chst dieses ZIP Ordner an gew�nschte Stelle entpacken.

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

Bevor das Programm an einem neuen / anderen PC benutzt werden kann m�ssen zuerst gewissen Anpassungen in den Code gemacht werden (nur einmalig). Im Ordner �Programm befinden sich drei Python files,  main.py ; gui.py ; functions.py. Diese im Microsoft Visual Studio code �ffnen (oder in ein beliebiges Programm). In diese Files befinden sich viele # Kommentare, welche genau beschreiben, was der Codes genau macht.
Main.py ist die Ausf�hrung des Programms, immer diesen ausf�hren bei Benutzung.
Gui.py ist die grafische Darstellung und Benutzeroberfl�che des Programms.
Functions.py ist der ganze Gehirn des Programms, hier sind alle Funktionen und mathematische Kalkulationen hinterlegt, die im Programm genutzt werden.

In Gui.py muss zun�chst bei Zeile 29 der Dateipfad des logo_image aktualisiert werden, da auf einem neuen Computer der Dateipfad anders ist.

In functions.py muss hingegen bei Zeile 7 der Dateipfad f�r die Raumnutzungsdaten aktualisiert werden, da auf einem neuen Computer der Dateipfad anders ist.





3. Benutzung des Programms

Nun main.py ausf�hren und das Programm ist funktionst�chtig. Das IFC-File aus dem Ordner �funktionsf�hige IFC-Files ausw�hlen, eigenen Strompreis und PV-Konfigurationen eingeben und auf berechnen dr�cken. Das ist beliebig �nderbar, einfach andere Datei ausw�hlen und Zahlen und erneut auf Berechnen dr�cken. Das Programm wird automatisch aktualisiert, ohne dass es geschlossen werden muss um eine neue berechnung durchzuf�hren.

Zum Schluss PDF Exportieren und dieser wird auch im Ordner �Programm� exportiert. Der Inhalt des PDFs ist das gleiche wie beim Programm. Also alle Berechnungen, L�sungen und Diagramme sind darin enthalten.


Rosario Leanza
