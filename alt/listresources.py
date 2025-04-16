import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import os



parser = argparse.ArgumentParser(description='Bodeplot-Messprogramm für DSO-X 3012A')

parser.add_argument('--startfrequenzy', type=int, default=10, help='Startfrequenz in Hz (Default: 10Hz)')
parser.add_argument('--stopfrequenzy', type=int, default=1000000, help='Stopfrequenz in Hz (Default: 1MHz)')
parser.add_argument('--amplitude', type=float, default=2, help='Amplitude in Vpp (Default: 2Vpp)')
parser.add_argument('--sweeptyp', type=str, default='log', help='Typ der Frequenzentwicklung (Default: log) (Optionen: lin, log, exp, oct)')
parser.add_argument('--num_samples', type=int, default=1000, help='Anzahl der Messlpunkte (Samples) (Default: 1000)')
parser.add_argument('--hold', type=float, default=0.5, help='Wartezeit zwischen den Messungen in Sekunden (Default: 0.5 s)')

args = parser.parse_args()


startfrequenzy = args.startfrequenzy
if startfrequenzy < 0:
    print("Startfrequenzy muss größer als 0 sein")
    print("Using default value: 10Hz")


stopfrequenzy = args.stopfrequenzy


amplitude = args.amplitude
if amplitude < 0.02:
    print("Amplitude muss größer als 20mVpp sein")
    print("Using default value: 2Vpp")
if amplitude > 20:
    print("Warnung: Amplitude größer als 20Vpp. Bitte überprüfen Sie die Eingabe.")
    change_inputs = input("Evtl. die Amplitude reduzieren:[n/y]")
    if change_inputs == 'y':
        user_amplitude = input("Amplitude in Vpp (Default: 2Vpp): ")
        if user_amplitude == '':
            amplitude = 2
            print("Standardwert 2Vpp wird verwendet.")
        else:
            try:
                amplitude = float(user_amplitude)
            except ValueError:
                print("Ungültige Eingabe. Standardwert 2Vpp wird verwendet.")
                amplitude = 2
        print("Neue Amplitude:", amplitude, "Vpp")
    else:
        print("Keine Änderungen vorgenommen.")


sweeptyp = args.sweeptyp
if sweeptyp not in ['lin', 'log', 'exp', 'oct']:
    print("Unbekannter Sweep-Typ:", sweeptyp)
    print("Using default value: log")


num_samples = args.num_samples
if num_samples < 1:
    print("Anzahl der Messpunkte muss größer als 0 sein")
    print("Using default value: 1000")


hold = args.hold
if hold < 0:
    print("Halt-Zeit muss größer als 0 sein")
    print("Using default value: 0.5s")


measurement_time = num_samples * hold
if measurement_time > 300:
    print("Warnung: Gesamte Messzeit ist größer als 5 Minuten:", measurement_time, "s")
    change_inputs = input("Evtl. die Anzahl der Messpunkte reduzieren oder die Halt-Zeit verringern:[n/y]")
    if change_inputs == 'y':
        user_samples = input("Anzahl der Messpunkte (Samples) (Default: 50): ")
        if user_samples == '':
            samples = 50
            print("Standardwert 50 wird verwendet.")
        else:
            try:
                samples = int(user_samples)
            except ValueError:
                print("Ungültige Eingabe. Standardwert 50 wird verwendet.")
                samples = 50
        user_hold = input("Halt-Zeit (Default: 0.5s): ")
        if user_hold == '':
            hold = 0.5
            print("Standardwert 0.5s wird verwendet.")
        else:
            try:
                hold = float(user_hold)
            except ValueError:
                print("Ungültige Eingabe. Standardwert 0.5s wird verwendet.")
                hold = 0.5
        measurement_time = samples * hold
        print("Neue Halt-Zeit:", hold, "s")
        print("Neue Anzahl der Messpunkte:", samples)
        print("Neue Gesamte Messzeit:", measurement_time, "s")
    else:
        print("Keine Änderungen vorgenommen.")
    
else:
    print("Gesamte Messzeit:", measurement_time, "s")


print("Startfrequenzy:", startfrequenzy, "Hz")
print("Stopfrequenzy:", stopfrequenzy, "Hz")
print("Sweep-Typ:", sweeptyp)
print("Halt-Zeit:", hold, "s")
print("Anzahl der Messpunkte:", num_samples)





#verfügbare Geräte ausgeben

#file lesen falls vorhanden
    #scopeid = ... signalgeneratorid = ...
    #vergleiche mit den IDs der angeschlossenen Geräte, falls sie übereinstimmen sie als default verwenden
    #abfrage ob es so übernommen werden soll
#sonst user eingabe und abspeichern

rm = pyvisa.ResourceManager('@py')
connected_devices = rm.list_resources()
print("Verfügbare Geräte:")
for device in connected_devices:
    print(device)

# filename = "known_devices.txt"
# if os.path.exists(filename):
#     with open(filename, "r", encoding="utf-8") as datei:
#         known_devices = datei.readlines()
#         known_devices = [line.strip() for line in known_devices if line.strip()]
#         scope_id = None
#         functiongenerator_id = None

#         for device in connected_devices:
#             for known_device in known_devices:
#                 if known_device in device:
#                     print(f"Bekanntes Gerät gefunden: {device}")
#                     if "SCOPE" in known_device.upper():
#                         scope_id = device
#                     elif "FUNCTIONGENERATOR" in known_device.upper():
#                         functiongenerator_id = device

#         if scope_id and functiongenerator_id:
#             print(f"Standardgeräte erkannt: Oszilloskop = {scope_id}, Funktionsgenerator = {functiongenerator_id}")
#             use_defaults = input("Möchten Sie diese Geräte verwenden? [y/n]: ").strip().lower()
#             if use_defaults != 'y':
#                 scope_id = None
#                 functiongenerator_id = None






if len(devices) == 0:
    print("Keine Geräte gefunden. Bitte überprüfen Sie die Verbindung.")
    exit()


# Ressourcenmanager initialisieren und Gerät öffnen
rm = pyvisa.ResourceManager()
scope = rm.open_resource(scope_id)
functiongenerator = rm.open_resource(functiongenerator_id)
print("Verfügbare Geräte:")
print("Verbunden mit:", scope.query("*IDN?").strip(), "und", signal_generator.query("*IDN?").strip())

# Gerät zurücksetzen und Kanäle aktivieren
scope.write("*RST")
time.sleep(1)
scope.write("CHANnel1:DISPlay ON")
scope.write("CHANnel2:DISPlay ON")







# Listen zur Speicherung der Messdaten: Frequenz, Gain (dB) und Phase (Grad)
measured_freq = []
gain_db = []
phase_deg = []

print("Starte Datensammlung... (Externer Sweep: Oszi misst Frequenz)")

for i in range(num_samples):

    #frequenz im Signalgenerator einstellen
    #skalierung am oszi einstellen
    #messung von frequenz, amplituden und phase

    try:
        functiongenerator.write("SINusoid <{freq}> ,<{amplitude}>")
    except Exception as e:
        print("Fehler bei Frequenzeinstellung:", e)
        



    try:
        # Frequenz wird von Kanal 1 gemessen (Sweep erfolgt extern)
        freq_response = scope.query("MEASure:FREQuency? CHANnel1")
        freq = float(freq_response)
        print(f"Frequenz gemessen: {freq:.2f} Hz")
    except Exception as e:
        print("Fehler bei Frequenzmessung:", e)
        freq = 0

    try:
        # Spitzenspannung an Kanal 1 (Eingang) abfragen
        ch1_response = scope.query("MEASure:VMAX? CHANnel1")
        ch1_amp = float(ch1_response)
        print(f"Spitzenspannung Kanal 1 gemessen: {ch1_amp:.2f} V")
    except Exception as e:
        print("Fehler bei Kanal 1 Messung:", e)
        ch1_amp = 0

    try:
        # Spitzenspannung an Kanal 2 (Ausgang) abfragen
        ch2_response = scope.query("MEASure:VMAX? CHANnel2")
        ch2_amp = float(ch2_response)
        print(f"Spitzenspannung Kanal 2 gemessen: {ch2_amp:.2f} V")
    except Exception as e:
        print("Fehler bei Kanal 2 Messung:", e)
        ch2_amp = 0

    try:
        # Zeitdifferenz (TDIF) zwischen Kanal 1 und Kanal 2 zur Phasenbestimmung abfragen
        tdif_response = scope.query("MEASure:TDIF? CHANnel1,CHANnel2")
        time_delay = float(tdif_response)
        print(f"Zeitdifferenz gemessen: {time_delay:.6f} s")
    except Exception as e:
        print("Fehler bei TDIF-Messung:", e)
        time_delay = 0



    # Berechne den Gain in dB (Schutz vor Division durch 0)
    if ch1_amp > 0:
        gain = 20 * np.log10(ch2_amp / ch1_amp)
    else:
        gain = -999  # Kennzeichnung für fehlerhafte Messung
    # Berechne die Phasenverschiebung in Grad: (Zeitdifferenz * Frequenz * 360°)
    phase = (time_delay * freq) * 360




    measured_freq.append(freq)
    gain_db.append(gain)
    phase_deg.append(phase)

    print(f"Messung {i+1}/{num_samples}: Frequenz = {freq:.2f} Hz, Gain = {gain:.2f} dB, Phase = {phase:.2f}°")
    time.sleep(0.5)  # Wartezeit, um ausreichend stabilisierte Messwerte zu erhalten

# Um eventuell nicht monotone Messreihenfolge (abhängig vom Sweep) zu berücksichtigen, sortiere die Daten nach Frequenz
measured_freq = np.array(measured_freq)
gain_db = np.array(gain_db)
phase_deg = np.array(phase_deg)
sort_index = np.argsort(measured_freq)
measured_freq = measured_freq[sort_index]
gain_db = gain_db[sort_index]
phase_deg = phase_deg[sort_index]

# Erstelle den Bodeplot: Amplitude und Phase als Funktion der gemessenen Frequenz
fig, ax1 = plt.subplots()
ax1.set_xlabel('Frequenz (Hz)')
ax1.set_ylabel('Gain (dB)', color='tab:blue')
ax1.semilogx(measured_freq, gain_db, 'o-', color='tab:blue', label="Gain")
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True, which='both', linestyle='--')

ax2 = ax1.twinx()
ax2.set_ylabel('Phase (Grad)', color='tab:red')
ax2.semilogx(measured_freq, phase_deg, 'x-', color='tab:red', label="Phase")
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Bodeplot (Externer Sweep, Frequenzmessung am Oszilloskop)')
fig.tight_layout()
plt.show()

# Schließe die Verbindung zum Gerät
scope.close()
rm.close()
