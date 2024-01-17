#functions.py
import ifcopenshell
import ifcopenshell.util.element
import pandas as pd

# Raumnutzungsdaten SIA Energiebedarf nach Raumnutzungen pro m2
raumnutzungsdaten = pd.read_excel(r"/Users/rosario.leanza/Library/CloudStorage/OneDrive-HochschuleLuzern/Module/3.HS23/DC_SCRIPT/EnergiebedarfnachFlächeTool/Raumnutzungsdaten.xlsx")

# Excel Pfad ^^^^^^^^^^^^ bei read_excel(r" X "), das X mit Pfad vom Raumnutzundsdaten.xlsx ändern







# Funktion öffnen der IFC-Datei
def ifc_file_reader(ifc_file_path):
    try:
        model = ifcopenshell.open(ifc_file_path)
        return model
    
    except Exception as e:
        print(f"Fehler beim Öffnen der IFC-Datei: {e}")
        return None

# Funktion Räume aus IFC
def get_spaces(model):
    spaces = model.by_type("IfcSpace")
    return spaces

# Funktion Namen der Räume
def get_room_names(room):
    attr = room.get_info()
    if attr.get("LongName") in room:
        return attr.get("LongName")
    else:
        return "Nicht definiert"
  
# Funktion Raumkategorien aus Räume (nicht nutzbar mit meiner tabelle aus SIA, da nur gewisse Kategorien möglich sind laut SIA2056 und in Revit nicht alle verfügbar sind
#def get_room_category(room):
#    all_psets = ifcopenshell.util.element.get_psets(room, psets_only=False)

#    if all_psets is not None:
#        pset_common = all_psets.get("ID-Daten")

#        if pset_common is not None:
#            prop_category = pset_common.get("Kategorie")

#            if prop_category is not None and prop_category != "":
#                return prop_category
    
# Funktion Fläche aus Räume lesen
def get_room_floor_area(room):
    all_psets = ifcopenshell.util.element.get_psets(room, psets_only=False)

    if all_psets is not None:
        pset_base = all_psets.get("BaseQuantities")

        if pset_base is not None:
            prop_area = pset_base.get("NetFloorArea")

            if prop_area is not None and prop_area != "":
                return round(prop_area, 2)

    return None

# Berechnung Energiebedarf auf Fläche
def calculate_room_energy(room_floor_area, room_name):
    index = raumnutzungsdaten[raumnutzungsdaten["Raumnutzung"] == room_name].index[0]
    category_energy = raumnutzungsdaten.iloc[index]["Energie"]
    room_energy = room_floor_area * category_energy
    return round(room_energy, 2)

# Berechnung Energiekosten im Raum
def calculate_energy_cost(room_energy, strompreis_label):
    strompreis_wert = float(strompreis_label.get())
    if room_energy is not None:
        room_energy_cost = room_energy * strompreis_wert
        return round(room_energy_cost,2)
    else:
        return 0.0

# Berechnung Stromkosten Total
def sum_total_cost(total_costs, energy_costs):
    total_energy_cost = sum(energy_costs)
    total_costs.configure(text=f"Stromkosten: {total_energy_cost:.2f} CHF/Jahr")
    print("Gesamtkosten: ", round(total_energy_cost, 2))

# Berechnung Leistung pro Raum
def power_consume_calculator(room_name, room_energy):
    index = raumnutzungsdaten[raumnutzungsdaten["Raumnutzung"] == room_name].index[0]
    category_hours = raumnutzungsdaten.iloc[index]["Nutzungsstunden"]
    room_power_consume = room_energy / category_hours
    return round(room_power_consume, 2)

# Summe aller Energien
def sum_total_energy(gesamtenergie, room_energies):
    total_energy = sum(room_energies)
    gesamtenergie.configure(text=f"Gesamter Energiebedarf: {total_energy:.2f} kWh/Jahr")
    print("Gesamte Energie: ", round(total_energy, 2))

# Summe aller Leistungen
def sum_total_power(gesamtleistung_text, room_powerdf):
    total_power = sum(room_powerdf)
    gesamtleistung_text.configure(text=f"Gesamter Leistungsbedarf: {total_power:.2f} kW")
    print("Gesamte Leistung: ", round(total_power, 2))

# Funktion Berechnung PV Fläche
def get_pv_area(pv_fläche_label, pv_berechnet_text, erzeugung_pv_label, strompreis_label, energy_costs):
    try:
        pv_fläche_wert = float(pv_fläche_label.get())
        strompreis_wert = float(strompreis_label.get())
        erzeugung_pv_wert = float(erzeugung_pv_label.get())
        pv_berechnet = pv_fläche_wert * erzeugung_pv_wert * strompreis_wert
        pv_berechnet_text.configure(text=f"Mögliche Stromersparnisse durch PV: {pv_berechnet:.2f} CHF/Jahr")
        energy_costs.append(-pv_berechnet)
        return pv_berechnet
    except ValueError:
        pv_berechnet_text.configure(text="Ungültige Eingabe")
