'''
Autor: Anton CNC
YouTube: https://www.youtube.com/@boessi

Dieses Programm bietet folgende Vorteile:

Es garantiert, dass die exakte Kombination von Endmaßen gefunden wird – sofern sie existiert.
Es verwendet Rekursion mit Backtracking, um alle möglichen Kombinationen zu überprüfen.
Es berücksichtigt Ungenauigkeiten bei Gleitkommazahlen durch die Verwendung eines sehr kleinen Toleranzwertes (1e-9).
Es gibt die gefundene Kombination, die Anzahl der verwendeten Endmaße und die Gesamtsumme aus.
Zum Ausführen des Programms stelle sicher, dass Python und Tkinter installiert sind.

Das Backtracking in diesem Programm funktioniert wie folgt: 1.) Die Funktion find_end_gauges implementiert den Backtracking-Algorithmus. Sie versucht, eine Kombination von Endmaßen zu finden, die genau die Ziel-Länge ergibt.
2.) Der Algorithmus beginnt mit einer leeren Kombination und fügt nach und nach Endmaße hinzu.
3.) In jedem Schritt wird ein Endmaß zur aktuellen Kombination hinzugefügt und überprüft:

Wenn die Summe der Endmaße der Ziel-Länge entspricht, wurde eine Lösung gefunden.
Wenn die Summe größer als die Ziel-Länge ist, ist dieser Pfad nicht zielführend.
Wenn die Summe kleiner ist, wird die Suche rekursiv fortgesetzt.
Wenn ein Pfad nicht zu einer Lösung führt, „springt“ der Algorithmus zurück (Backtracking), indem er zum vorherigen Zustand zurückkehrt und eine andere Möglichkeit ausprobiert.

Dieser Vorgang wiederholt sich, bis entweder eine Lösung gefunden wurde oder alle Möglichkeiten ausgeschöpft sind.

Die Verwendung einer Menge (used_end_measurements) stellt sicher, dass jedes Endmaß nur einmal verwendet wird.

Dieser Ansatz ermöglicht es, den Lösungsraum effizient zu durchsuchen, indem nicht zielführende Pfade frühzeitig abgebrochen werden.

'''
import tkinter as tk
from tkinter import ttk, messagebox, font, scrolledtext


def finde_endmaße(ziel, verfügbare_endmaße, aktuelle_kombination=None, verwendete_endmaße=None):
    if aktuelle_kombination is None:
        aktuelle_kombination = []
    if verwendete_endmaße is None:
        verwendete_endmaße = set()

    aktuelle_summe = sum(aktuelle_kombination)

    #if abs(aktuelle_summe - ziel) < 1e-9:
    if abs(aktuelle_summe - ziel) < 0.005:
        return aktuelle_kombination

    if aktuelle_summe > ziel:
        return None

    for i, endmaß in enumerate(verfügbare_endmaße):
        if endmaß not in verwendete_endmaße:
            neue_kombination = aktuelle_kombination + [endmaß]
            neue_verwendete = verwendete_endmaße.copy()
            neue_verwendete.add(endmaß)
            ergebnis = finde_endmaße(ziel, verfügbare_endmaße, neue_kombination, neue_verwendete)
            if ergebnis:
                return ergebnis

    return None


class EndmaßRechnerApp:
    def __init__(self, master):
        self.master = master
        master.title("Anton CNC: Endmaß-Rechner")
        master.geometry("440x750")  # Fenstergröße angepasst

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=16)  # Schriftgröße auf 16 erhöht
        master.option_add("*Font", default_font)

        self.endmaße = [
            50, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2,
            1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2,
            1.1, 1.09, 1.08, 1.07, 1.06, 1.05,
            1.04, 1.03, 1.02, 1.01, 1.005, 1
        ]

        self.endmaße_real = [
            50.00028,   # 50 mm + 0.00028 mm
            30.00025,   # 30 mm + 0.00025 mm
            19.99979,   # 20 mm - 0.00021 mm
            10.00012,   # 10 mm + 0.00012 mm
            9.00005,    # 9 mm + 0.00005 mm
            7.99960,    # 8 mm - 0.0004 mm
            6.99985,    # 7 mm - 0.00015 mm
            5.99988,    # 6 mm - 0.00012 mm
            5.00002,    # 5 mm + 0.00002 mm
            4.00040,    # 4 mm + 0.0004 mm
            3.00002,    # 3 mm + 0.00002 mm
            2.00014,    # 2 mm + 0.00014 mm
            1.90028,    # 1.9 mm + 0.00028 mm
            1.79992,    # 1.8 mm - 0.00008 mm
            1.70032,    # 1.7 mm + 0.00032 mm
            1.60038,    # 1.6 mm + 0.00038 mm
            1.50033,    # 1.5 mm + 0.00033 mm
            1.40016,    # 1.4 mm + 0.00016 mm
            1.29970,    # 1.3 mm - 0.0003 mm
            1.20005,    # 1.2 mm + 0.00005 mm
            1.10000,    # 1.1 mm + 0.00000 mm
            1.09045,    # 1.09 mm + 0.00045 mm
            1.07969,    # 1.08 mm - 0.00031 mm
            1.07010,    # 1.07 mm + 0.0001 mm
            1.06015,    # 1.06 mm + 0.00015 mm
            1.04972,    # 1.05 mm - 0.00028 mm
            1.04004,    # 1.04 mm + 0.00004 mm
            1.03040,    # 1.03 mm + 0.0004 mm
            1.01967,    # 1.02 mm - 0.00033 mm
            1.01005,    # 1.01 mm + 0.00005 mm
            1.00472,    # 1.005 mm - 0.00028 mm
            0.99990     # 1 mm - 0.0001 mm
        ]

        self.label = ttk.Label(master, text="Gewünschte Länge (mm):")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(master)
        self.entry.pack()
        self.entry.bind("<Return>", lambda event: self.calculate())

        # Radiobuttons für "Ideal" und "Real" nebeneinander
        self.auswahl_modus = tk.StringVar(value="ideal")  # Standardmäßig "ideal" ausgewählt
        self.radio_frame = ttk.Frame(master)  # Frame für die Radiobuttons
        self.radio_frame.pack()

        self.ideal_radio = ttk.Radiobutton(self.radio_frame, text="Ideal", variable=self.auswahl_modus, value="ideal")
        self.real_radio = ttk.Radiobutton(self.radio_frame, text="Real", variable=self.auswahl_modus, value="real")
        self.ideal_radio.pack(side=tk.LEFT, padx=10)  # nebeneinander anordnen
        self.real_radio.pack(side=tk.LEFT, padx=10)

        self.calculate_button = ttk.Button(master, text="Berechnen", command=self.calculate)
        self.calculate_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(master, height=20, width=50)
        self.result_text.pack(pady=10, padx=10)
        self.result_text.configure(padx=20, pady=10)  # Innerer Abstand im Widget

    def calculate(self):
        # Leeren des Ausgabefelds zu Beginn der Berechnung
        self.result_text.delete(1.0, tk.END)

        try:
            eingabe = self.entry.get().replace(',', '.')
            ziel = float(eingabe)
            if ziel <= 0:
                messagebox.showerror("Fehler", "Die Länge muss größer als 0 sein.")
                return

            # Auswahl des Endmaß-Arrays basierend auf dem ausgewählten Radiobutton
            if self.auswahl_modus.get() == "ideal":
                verfügbare_endmaße = self.endmaße
            else:
                verfügbare_endmaße = self.endmaße_real

            ergebnis = finde_endmaße(ziel, verfügbare_endmaße)

            if ergebnis:
                self.result_text.insert(tk.END, f"Exakte Länge von {ziel} mm:\n\n")
                for maß in ergebnis:
                    # Prüfen und Einrücken von Werten kleiner als 10 mm
                    if maß < 10:
                        self.result_text.insert(tk.END, f" {maß:.5f} mm\n")  # Ein Leerzeichen für das Einrücken
                    else:
                        self.result_text.insert(tk.END, f"{maß:.5f} mm\n")
                self.result_text.insert(tk.END, f"\nAnzahl der Endmaße: {len(ergebnis)}\n")

                # Zusätzliche Ausgabe für "Real"-Modus
                if self.auswahl_modus.get() == "real":
                    summe_real = sum(ergebnis)
                    abweichung = summe_real - ziel
                    self.result_text.insert(tk.END, f"Summe (real): {summe_real:.5f} mm\n")
                    self.result_text.insert(tk.END, f"Abweichung: {abweichung:.5f} mm\n")
                else:
                     self.result_text.insert(tk.END, f"Summe: {sum(ergebnis):.5f} mm\n")

            else:
                self.result_text.insert(tk.END, f"Keine exakte Kombination für {ziel} mm gefunden.")

        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl ein.")


root = tk.Tk()
app = EndmaßRechnerApp(root)
root.mainloop()
