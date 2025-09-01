# Multi Energy System Explorer

Gerade Version 0 zum Vergleich der Programmstruktur mit Matlab Modell aus SENSE Lehre.

Nutzen durch Anpassen der Parameter (Capex noch nicht genutzt) in main.py und erstellen anderer Modellstruktur in MES.py.

### Python Dateien
#### main.py
- Anpassen der Paramter
- Einlesen der Verbrauchs- und Erzeugungsprofile
- Aufrufen der MES Erstellung
- Aufrufen der OPtimierung
- Abspeichern der Ergebnisse in Excel-Datei

#### technologies.py
- Speichert Standardwerte für Paramter
- Langfristig Technologie Modelle

#### classes.py
- 3 Elternklassen mit allen Kindern
- MES Klasse zur Speicherung des MES
- langfristig erstellen der dicts für Optimierung (gerade in Optimierungsdatei)

#### MES.py
- Struktur des MES erstellen

#### functions.py
- Hilfsfunktionen für alles nicht eindeutig zuordnbare
- 
#### optimize.py
- Erstellung eines MILP Problems zur Optimierung des MES mit pyomo

#### result_visualisation.py
- Hardgecodeter Vergleich mit Matlab Modell
- Langfristig Erstellung der klassischen Grafiken

### sonst. Dateien
#### Results.xlsx
- Ergebnis Excel aus dem Matlab Model

#### pv_daten_Berlin.csv
- normierte PV Einspeisung von Renewables.ninja

#### Heatload
- Aus SENSE Lehre
  
#### ElectricityLoad
- Aus SENSE Lehre
  
#### Dependencies:
- gurobi (oder anderer Solver, dann anderen Solver in optimize.py auswählen)
- pyomo
- pandas
- matplotlib
- numpy
- networkx
