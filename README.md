# WTTScraper

Ste že slišali za Wise Timetable? Tole https://wtimetable.com/?  
Se tudi vam zdi kot najslabši način organizacije urnika?  
Ste ga že poskusili uporabljati, upravljati z njim in spremljati predavanja, a ste ga na koncu vseeno za j****i?  
No, ne skrbi. Tukaj je WTTScraper.

En mali python class, ki ga lahko importate v vašo aplikacijo in ga uporabljate ali z discord bot-om ali z spletno stranjo.  
Skripta vrne dict ki se lahko pretvori v JSON.  

## Requirements
```txt
beautifulsoup4==4.12.3
Requests==2.32.3
```
Lahko jih tudi namestite s pomočjo ukaza pip `pip3 install -r requirements.txt`

## Uporaba
```python
from WTTScraper import WTTScrapper

filter_predmeti = {"razredi": ['RV1', 'RV2'], 'profesor': 'Prfoks', 'zacetek': '07:00'}

wtts = WTTScrapper("https://wise-tt.com/wtt_um_feri")

print("DANAŠNJI DATUM")
wtts.parse_calendar()
print(wtts.get_calendar())

print("Z DATUMOM")
wtts.parse_calendar(datum="07.10.2024")
print(wtts.get_calendar())

print("FILTRIRAN")
print(wtts.filter_calendar(filter_predmeti))
```
Output:
```json
{
    'Ponedeljek': [
        {'profesor': 'MARTINA ŠESTAK', 'razredi': ['MAG 1 IPT IIR RV 1'], 'predmet': 'PODATKOVNE TEHNOLOGIJE IN STORITVE', 'ucilnica': '(RU) G3-laboratorij Lumiere, klet', 'zacetek': '07:00', 'konec': '10:00'}
     ],
    'Torek': [],
    'Sreda': [],
    'Četrtek': [],
    'Petek': []
}
```
