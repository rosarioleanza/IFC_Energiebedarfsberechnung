# gui.py
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import PhotoImage
import os
from functions import ifc_file_reader, get_spaces, get_room_floor_area, get_room_names, sum_total_energy, sum_total_power
from functions import calculate_room_energy, calculate_energy_cost, get_pv_area, sum_total_cost, power_consume_calculator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF

# Schriftart erstellung für Titel
titel_schrift = ("Helvetica", 20, "bold")

# Klasse Hauptfenster und seine Unterfunktionen
class MainWindow:

    # Erstellung Hauptfenster der Anwendung und Konfiguration
    def __init__(self, root):
        self.root = root
        self.root.title("IFC Energiebedarf basierend auf Nutzungsfläche - DC_Script - HSLU - HS23 - Entwickelt mit Python von Rosario Leanza")
        self.root.resizable(width=True, height=True)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Logo für Anwendung (sichtbar auf Taskbar unten)
        logo_image = PhotoImage(file=r"/Users/rosario.leanza/Library/CloudStorage/OneDrive-HochschuleLuzern/Module/3.HS23/DC_SCRIPT/EnergiebedarfnachFlächeTool/logo.png")

        # Logo Pfad ^^^^^^^^^^^^ bei file=r" X ", das X mit Pfad vom logo.png ändern (im Ordner "Programm" enthalten)






        self.root.iconphoto(True, logo_image)

        # Aufrufung ui mit Benutzerlayout und GUI-Elemente
        self.create_ui()

    # Definiert create_ui mit linkem und rechtem Frame
    def create_ui(self):
        self.create_left_frame()
        self.create_right_frame()
        self.create_under_frame()

    # GUI Frame Links
    def create_left_frame(self):

        # Erstellung User Interface links
        left_frame = ctk.CTkFrame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        # Titel Frame links
        room_info_label = ctk.CTkLabel(left_frame, text="Optionen und Bedienung", font=titel_schrift)
        room_info_label.grid(row=0, column=0, padx=150, pady=10, columnspan=2)

        # Button Datei auswählen
        choose_file_button = ctk.CTkButton(left_frame, text="IFC-Datei auswählen", command=self.choose_file)
        choose_file_button.grid(row=1, column=0, padx=10, pady=0, sticky="w")

        # Speicherung Dateiname und wiederverwendung als Überblick
        self.ifc_file_name = ctk.StringVar()
        ifc_file_label = ctk.CTkLabel(left_frame, textvariable=self.ifc_file_name)
        ifc_file_label.grid(row=1, column=1, padx=10, pady=25, sticky="w")

        # Beschreibung Eingabefeld für die PV Fläche
        pv_fläche_text = ctk.CTkLabel(left_frame, text="PV Fläche (m²):")
        pv_fläche_text.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Eingabefeld und Speicherung PV Fläche für die Berechnung
        self.pv_fläche_label = ctk.StringVar()
        self.pv_fläche_label.set("100")
        pv_fläche_entry = ctk.CTkEntry(left_frame, textvariable=self.pv_fläche_label)
        pv_fläche_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Beschreibung Eingabefeld für Strompreis
        strompreis_text = ctk.CTkLabel(left_frame, text="Strompreis in CHF/kWh:")
        strompreis_text.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        # Eingabefeld und Speicherung Strompreis für die Berechnung
        self.strompreis_label = ctk.StringVar()
        self.strompreis_label.set("0.23")
        strompreis_entry = ctk.CTkEntry(left_frame, textvariable=self.strompreis_label)
        strompreis_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Button zum erneuten Berechnen
        calculate_button = ctk.CTkButton(left_frame, text="Berechnen", command=self.calculate)
        calculate_button.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        # Beschreibung Eingabefeld für Erzeugung PV
        erzeugung_pv_text = ctk.CTkLabel(left_frame, text="Erzeugung PV in kWh/m2 pro Jahr:")
        erzeugung_pv_text.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Eingabefeld und Speicherung Erzeugung PV
        self.erzeugung_pv_label = ctk.StringVar()
        self.erzeugung_pv_label.set("150")
        erzeugung_pv_entry = ctk.CTkEntry(left_frame, textvariable=self.erzeugung_pv_label)
        erzeugung_pv_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Beschreibung Export button
        export_text = ctk.CTkLabel(left_frame, text="Berechnungen als PDF exportieren:", font=('Helvetica', 14, 'bold'))
        export_text.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        # Button zum exportieren als PDF
        export_button = ctk.CTkButton(left_frame, text="PDF exportieren", font=('Helvetica', 14, 'bold'), command=self.export_pdf)
        export_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Bestätigung Export Label
        self.exported_label = ctk.CTkLabel(left_frame, text=" ")
        self.exported_label.grid(row=5, column=2, padx=10, pady=15, sticky="w")

    # GUI Frame rechts
    def create_right_frame(self):

        # Erstellung User Interface rechts
        right_frame = ctk.CTkFrame(self.root)
        right_frame.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=0)

        # Titel Frame rechts
        room_info_label = ctk.CTkLabel(right_frame, text="Informationen und Ausgabe", font=titel_schrift)
        room_info_label.grid(row=0, column=0, padx=200, pady=10)

        # Erstellt Frame mit Scroll-Funktion
        room_info_frame = ctk.CTkScrollableFrame(right_frame)
        room_info_frame.grid(row=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="nswe")
        room_info_frame.grid_columnconfigure(0, weight=1)

        # Erstellt ein leeres und aktualisierbares Label im obigen Frame
        self.room_info_label = ctk.CTkLabel(room_info_frame, text=" "*30)
        self.room_info_label.grid(column=0, row = 0)
        self.room_info_label.configure(anchor="nw")

        # Erstellt ein leeres und aktualisierbares Label für Kalkulationen im obigen Frame
        self.room_info_calculations = ctk.CTkLabel(room_info_frame, text=" "*30)
        self.room_info_calculations.grid(column=1, row = 0, padx = 10)
        self.room_info_calculations.configure(anchor="nw")

        # Stromkosten Label mit Text
        self.total_costs = ctk.CTkLabel(right_frame, text=f"Stromkosten: ----.--- CHF/Jahr")
        self.total_costs.grid(row=6, column=0, padx=10, pady=1, sticky="w")

        # Gesamter Energiebedarf Label
        self.gesamtenergie = ctk.CTkLabel(right_frame, text=f"Gesamter Energiebedarf: ----.--- kWh/Jahr")
        self.gesamtenergie.grid(row=6, column=0, padx=10, pady=1, sticky="e")

        # Label berechnete PV
        self.pv_berechnet_text = ctk.CTkLabel(right_frame, text=f"Mögliche Stromersparnisse durch PV: ----.--- CHF/Jahr")
        self.pv_berechnet_text.grid(row=7, column=0, padx=10, pady=1, sticky="w")

        # Label zum anzeigen der Gesamte Leistung
        self.gesamtleistung_text = ctk.CTkLabel(right_frame, text=f"Gesamter Leistungsbedarf: ----.--- kW", fg_color="transparent")
        self.gesamtleistung_text.grid(row=7, column=0, padx=10, pady=10, sticky="e")

    # GUI Frame unten
    def create_under_frame(self):

        # Erstellung User Interface unten
        under_frame = ctk.CTkFrame(self.root)
        under_frame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Titel Frame unten
        room_info_label = ctk.CTkLabel(under_frame, text="Diagramme", font=titel_schrift)
        room_info_label.grid(row=0, columnspan=2, padx=25, pady=10)

        # Platzhalter für Diagramm Energiekosten
        self.diagram_canvas = ctk.CTkCanvas(under_frame, width = 800, height = 395)
        self.diagram_canvas.configure(background="darkgray",highlightbackground="darkgray")
        self.diagram_canvas.grid(row=1, column=0, padx=10, pady=10, sticky="ew", ipadx=10, ipady=50)

        # Platzhalter für Diagramm Leistung
        self.diagram2_canvas = ctk.CTkCanvas(under_frame, width = 650, height = 395)
        self.diagram2_canvas.configure(background="darkgray",highlightbackground="darkgray")
        self.diagram2_canvas.grid(row=1, column=1, pady=10, sticky="ew", ipadx=10, ipady=50)




        # Bis hier alle angezeigte Sachen im Benutzerfenster

        # Ab hier weitere Funktionen die beim Benutzerfenster gebraucht werden (zum beispiel für Buttons)


    # Dateiauswähldialog
    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("IFC-Dateien", "*.ifc")])

        # Speicherung Dateipfad
        self.ifc_file_path = ctk.StringVar()

        # Kontrolle ob Dateipfad korrekt
        if self.file_path:

            # Aktualisierung Dateipfad
            self.ifc_file_path.set(self.file_path)
            print("Dateipfad ausgewählt:", self.file_path)

            # Aktualisierung Dateiname zur Wiederverwendung
            self.ifc_file_name.set(os.path.basename(self.file_path))

    # Befehl Kalkulationen ausführen    
    def calculate(self):    

        if self.file_path:

            # Leert die Diagramme in der unteren Leiste
            self.diagram_canvas.delete("all")
            self.diagram2_canvas.delete("all")

            # Leert die Rauminformationen Label
            self.room_info_label.configure(text="")
            self.room_info_calculations.configure(text="")

            # Leert die Gesamtkosten, Gesamtenergie und Gesamtleistung Label
            self.total_costs.configure(text="Stromkosten: ----.--- CHF/Jahr")
            self.gesamtenergie.configure(text="Gesamter Energiebedarf: ----.--- kWh/Jahr")
            self.pv_berechnet_text.configure(text="Mögliche Stromersparnisse: ----.--- CHF/Jahr")
            self.gesamtleistung_text.configure(text="Gesamter Leistungsbedarf: ----.--- kW", fg_color="transparent")

            # Ausführung Rauminformationsleser und alle Kalkulationen
            self.display_room_info()

            # Ausführung Kalkulation PV
            self.calculate_pv_fläche()

        else:

            # Erste Zeile im Rauminformationstext
            self.room_info_label.configure(text="Kein IFC-Ausgewählt")  
            print("Kein IFC-Ausgewählt")

    # Rauminformationen aus IFC lesen
    def display_room_info(self):
        model = ifc_file_reader(self.ifc_file_path.get())
        spaces = get_spaces(model)
        self.room_info_label.configure(text="")  # Leert vorherigen Label mit PLatzhalter

        # Initiert leere Listen für den weitergebrauch später
        self.room_powerdf = []
        self.energy_costs = []
        self.room_energies = []
        self.room_names = []

        # Kontrolle ob Räume vorhanden sind
        if spaces:

            # Erste Zeile im Rauminformationstext
            self.room_info_label.configure(text="Räume im IFC-Modell:")
            nr = 1

            # Pro Raum soll es diese Informationen lesen und berechnen
            for room in spaces:
                room_name = get_room_names(room)
                room_floor_area = get_room_floor_area(room)
                room_energy = calculate_room_energy(room_floor_area,room_name)
                energy_cost = calculate_energy_cost(room_energy, self.strompreis_label)
                room_power = power_consume_calculator(room_name, room_energy)

                # Speicherung der Werte in der erstellten Liste
                self.room_energies.append(room_energy)
                self.room_powerdf.append(room_power)
                self.energy_costs.append(energy_cost)
                self.room_names.append(room_name)

                # Rauminformations Text erstellung
                if room_floor_area is not None:
                    room_text = f"{nr}. Raum: {room_name}, Fläche: {room_floor_area} m²     "
                    room_calculations = f"Energiebedarf: {room_energy} kWh/a, Energiekosten: {energy_cost} CHF/a"
                else:
                    room_text = f"{nr}. Raum: {room_name}, Fläche: Nicht definiert"
                    room_calculations = " "

                # Ergänzt leeres Label mit Rauminformationen ab zweite Zeile/ Eine Zeile pro Raum
                self.room_info_label.configure(text=self.room_info_label.cget("text") + "\n" + room_text, justify = "left")
                self.room_info_calculations.configure(text=self.room_info_calculations.cget("text") + "\n" + room_calculations, justify = "left")
                nr = nr + 1
        else:
            self.room_info_label.configure(text=("Keine Räume erkannt!"))

        # Kontrolle ob berechnete Energiekosten vorhanden sind.
        if self.energy_costs:

            # Ausführung Diagramme
            self.diagramm_kosten()
            self.diagramm_kosten2()

        # Ausführung Kalkulation Stromkosten, Energie, Leistung
        sum_total_cost(self.total_costs, self.energy_costs)
        sum_total_energy(self.gesamtenergie, self.room_energies)
        sum_total_power(self.gesamtleistung_text, self.room_powerdf)

    # Kalkulation Stromeinsparungen dank PV Fläche
    def calculate_pv_fläche(self):
        get_pv_area(self.pv_fläche_label, self.pv_berechnet_text, self.erzeugung_pv_label, self.strompreis_label, self.energy_costs)
        
    # Diagrammerstellung für Kosten
    def diagramm_kosten(self):
        IFC_rooms = ['IFC-Modell']

        # Dataframe mit Energiekosten
        energy_costs_df = pd.DataFrame(self.energy_costs, columns=['Energiekosten_CHF'])

        # Balkendiagramm erstellen
        bar_width = 0.8 / len(IFC_rooms)
        bar_positions = np.arange(len(IFC_rooms))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
                'indigo', 'teal', 'magenta', 'lime', 'salmon', 'turquoise', 'gold', 'orchid', 'slateblue', 'darkgreen']

        # Diagrammgrösse einstellen
        fig, ax = plt.subplots(figsize=(9,5))

        # Für jeden Raum "Wert im Dataframe" soll es einen Balken erstellen
        for i, room_cost in enumerate(energy_costs_df["Energiekosten_CHF"]):
            color_index = i % len(colors)
            x_position = i * bar_width
            if room_cost >= 0:
                ax.bar(x_position, [room_cost], width=bar_width, label=self.room_names[i], color=colors[color_index], alpha=0.7)
                ax.text(x_position, room_cost, f'{room_cost:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
            else:
                ax.bar(x_position, [room_cost], width=bar_width, label=self.room_names[i], color=colors[color_index], alpha=0.7)
                ax.text(x_position, room_cost, f'{room_cost:.2f}', ha='center', va='bottom', color='black', fontweight='bold')

        # Diagramm-Titel und Achsenbeschriftungen hinzufügen
        plt.title('Energiekosten')
        plt.ylabel('Energiekosten (CHF/a)')
        np_IFC_rooms = np.array(IFC_rooms)
        plt.xticks(bar_positions, np_IFC_rooms)

         # Legende hinzufügen und positionieren
        legend = plt.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
        plt.subplots_adjust(right=0.70)

        plt.savefig("Diagramm1.png", bbox_inches="tight")

        # Diagramm anzeigen
        self.diagram_canvas.delete("all")
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.diagram_canvas)
        figure_canvas_widget = self.figure_canvas.get_tk_widget()
        figure_canvas_widget.place(relx=0, rely=0)


    # Diagrammerstellung für Leistung  
    def diagramm_kosten2(self):
        IFC_rooms = ['IFC-Modell']

        # Dataframe für Leistung
        power_consume_df = pd.DataFrame(self.room_powerdf, columns=["Leistung_kW"])

        # Balkendiagramm erstellen
        bar_width = 0.8 / len(IFC_rooms)
        bar_positions = np.arange(len(IFC_rooms))
        colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
                'indigo', 'teal', 'magenta', 'lime', 'salmon', 'turquoise', 'gold', 'orchid', 'slateblue', 'darkgreen']

        # Diagrammgrösse einstellen
        fig, ax = plt.subplots(figsize=(7,5))

        # Für jeden Raum "Wert im Dataframe" soll es einen Balken erstellen
        for i, room_consume in enumerate(power_consume_df["Leistung_kW"]):
            color_index = i % len(colors)
            x_position = i * bar_width
            if room_consume >= 0:
                ax.bar(x_position, [room_consume], width=bar_width, label=self.room_names[i], color=colors[color_index], alpha=0.7)
                ax.text(x_position, room_consume, f'{room_consume:.2f}', ha='center', va='bottom', color='black', fontweight='bold')
            else:
                ax.bar(x_position, [room_consume], width=bar_width, label=self.room_names[i], color=colors[color_index], alpha=0.7)
                ax.text(x_position, room_consume, f'{room_consume:.2f}', ha='center', va='bottom', color='black', fontweight='bold')

        # Diagramm-Titel und Achsenbeschriftungen hinzufügen
        plt.title("Leistung")
        plt.ylabel("Leistung (kW)")
        np_IFC_rooms = np.array(IFC_rooms)
        plt.xticks(bar_positions, np_IFC_rooms)

        plt.savefig("Diagramm2.png")

        # Diagramm anzeigen
        self.diagram2_canvas.delete("all")
        self.figure_canvas2 = FigureCanvasTkAgg(fig, master=self.diagram2_canvas)
        figure_canvas2_widget = self.figure_canvas2.get_tk_widget()
        figure_canvas2_widget.place(relx=0, rely=0)

    # Exportieren als PDF
    def export_pdf(self):

        title = "Energiebedarfsberechnung"

        #Bestandteile des PDFs
        class PDF(FPDF):

            # Kopfzeile
            def header(self):
                # Titelschriftart
                self.set_font('Arial', 'B', 18)
                # Mittige positionierung des Titels
                w = self.get_string_width(title) + 6
                self.set_x((210 - w) / 2)
                # Farbige Darstellung des Frames
                self.set_draw_color(255, 255, 255)
                self.set_fill_color(255, 255, 255)
                self.set_text_color(0, 80, 180)
                self.set_line_width(1)
                # Tiitel
                self.cell(w, 9, title, 1, 1, 'C')
                # Absatz
                self.ln(10)

            # Fusszeile
            def footer(self):
                # Position 1.5 cm vom Boden
                self.set_y(-15)
                # Schriftart
                self.set_font('Arial', 'I', 8)
                self.set_text_color(128)
                # Seitenzahl und Fusszeilentext
                self.cell(0, 10, 'IFC Energiebedarf basierend auf Nutzungsfläche - DC_Script - HSLU - HS23 - Entwickelt mit Python von Rosario Leanza   |   Seite ' + str(self.page_no()), 0, 0, 'C')

            # Kapitel 1 Titel für Rauminformationen und Berechnungen
            def chapter_title(self, num, label):
                self.set_font('Arial', '', 14)
                title_width = self.get_string_width(label) + 6
                left_margin = 10
                x_position = left_margin
                self.set_fill_color(200, 220, 255)
                self.rect(x_position, self.get_y(), title_width, 6, 'F')
                self.set_text_color(0, 80, 180)
                self.cell(title_width, 6, '%d. %s' % (num, label), 0, 1, 'C')
                self.ln(4)

            # Kapitel 1 Inhalt für Rauminformationen und Berechnungen
            def chapter_body(self, 
                             name, 
                             calc, 
                             total_costs, 
                             gesamtenergie, 
                             pv_berechnet_text, 
                             gesamtleistung_text,
                             pv_fläche_label,
                             erzeugung_pv_label):
                
                # Textblock 1 Rauminformationen
                self.set_font('Arial', '', 12)
                self.set_text_color(0, 0, 0)
                text = name.cget("text")
                self.multi_cell(0, 5, text)

                # Textblock 2 Berechnungen
                text2 = calc.cget("text")                
                self.multi_cell(0, 5, text2)
                self.ln()

                # Textblock 3 Gesamtenergie
                text3 = gesamtenergie.cget("text")
                self.multi_cell(0, 5, text3)
                self.ln()

                # Textblock 4 Gesamteleistung
                text4 = gesamtleistung_text.cget("text")
                self.multi_cell(0, 5, text4)
                self.ln()    

                # Textblock 5 PV Generiert kWh
                pv_fläche_wert = float(pv_fläche_label.get())
                erzeugung_pv_wert = float(erzeugung_pv_label.get())
                text5 = str(pv_fläche_wert * erzeugung_pv_wert)
                self.multi_cell(0, 5, "Energieerzeugung durch PV: " + text5 + " kWh/Jahr")
                self.ln()               

                # Textblock 6 Gesamtkosten
                text6 = total_costs.cget("text")
                self.multi_cell(0, 5, text6)
                self.ln()

                # Textblock 7 PV einsparungen
                text7 = pv_berechnet_text.cget("text")
                self.multi_cell(0, 5, text7)

            # Kapitel 2 Titel für Diagramme
            def chapter_title2(self, num, label):
                self.set_font('Arial', '', 14)
                title_width = self.get_string_width(label) + 6
                left_margin = 10
                x_position = left_margin
                self.set_fill_color(200, 220, 255)
                self.rect(x_position, self.get_y(), title_width, 6, 'F')
                self.set_text_color(0, 80, 180)
                self.cell(title_width, 6, '%d. %s' % (num, label), 0, 1, 'C')
                self.ln(4)

            # Kapitel 2 Inhalt für Diagramme
            def chapter_body2(self):
                self.image("Diagramm1.png", x=0, y = 35, w = 160, h = 100, type = "PNG", link = " ")
                self.image("Diagramm2.png", x=0, y = 140, w = 140, h = 100, type = "PNG", link = " ")

            def print_chapter(self, num, title, name, calc, total_costs, gesamtenergie, pv_berechnet_text, gesamtleistung_text, pv_fläche_label, erzeugung_pv_label, num2, title2):
                self.add_page()
                self.chapter_title(num, title)
                self.chapter_body(name, calc, total_costs, gesamtenergie, pv_berechnet_text, gesamtleistung_text, pv_fläche_label, erzeugung_pv_label)
                self.add_page()
                self.chapter_title2(num2, title2)
                self.chapter_body2()

        # Ausführung PDF Datei export
        pdf = PDF()
        pdf.set_title(title)
        pdf.set_author('Rosario Leanza')
        pdf.print_chapter(1, 
                            'Rauminformationen und Ausgabe', 
                            self.room_info_label, 
                            self.room_info_calculations,
                            self.total_costs,
                            self.gesamtenergie,
                            self.pv_berechnet_text,
                            self.gesamtleistung_text,
                            self.pv_fläche_label, 
                            self.erzeugung_pv_label,
                            2,
                            "Diagramme")

        try:
            self.exported_label.configure(text=" ")
            pdf.output('Energiebedarfsberechnung.pdf', 'F')
            print("PDF exportiert")
            self.exported_label.configure(text="PDF erfolgreich exportiert!")
        except Exception as e:
                print(f"Error exporting PDF: {e}")
                self.exported_label.configure(text="Fehler beim Exportieren des PDFs!") 