import requests
from datetime import datetime

import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

from bs4 import BeautifulSoup

class WTTScrapper:
    """
    form:j_idt411:0:j_idt417:2:j_idt418:1:j_idt427
    form:j_idt411:27:j_idt417:0:j_idt418:0:calendarHour
    form:j_idt411:0:j_idt417:1:j_idt418:0:calendarHour
    j_idt411 -> vrstica tako da ura
    j_idt417 -> dan (ponedeljek = 0, torek = 1)
    j_idt418 -> ko imas splitane ure na en dan 0 je leva 1 je desna in karkol več je +1
    j_idt427 -> specificna ura 3 kolumni so znotraj npr od 7:00 do 7:30 in mas potem 422 427 in 433
    """
    def __init__(self, url, filter=None):
        self.url = url
        self.dnevi = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek"]
        self.ure = [
            '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', 
            '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', 
            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', 
            '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', "21:00"
        ]
        self.calendar = None
    def process_class_data(self, string, zacetek):
        array = string[2:-3].split("\n")
        data = {}
        data_names = ["profesor", "razredi", "predmet", "ucilnica"]
        if len(array) == 4:
            for i in range(0, 4):
                if i == 1:
                    array_split = array[i].split(",")
                    data[data_names[i]] = array_split
                else:
                    data[data_names[i]] = array[i]
            data["zacetek"] = zacetek
            data["konec"] = ""
            return data
        else:
            print(array)
            print(string)
            input("Error array not len() of 4. Press enter to exit")
            exit(0)
    
    def parse_calendar(self, datum=None):
        request_timeout = 50

        if datum is not None:
            try:
                datetime.strptime(datum, '%d.%m.%Y')
            except ValueError:
                print("Datum mora biti v formatu dd.mm.llll Ex: 29.12.2024, 04.11.2024")
        else: 
            datum = datetime.today().strftime('%d.%m.%Y')
        
        print(datum)
        
        self.calendar = {
            "Ponedeljek": [], 
            "Torek": [], 
            "Sreda": [], 
            "Četrtek": [], 
            "Petek": []
        }

        session = requests.Session()

        response = session.get(self.url, allow_redirects=True, timeout=request_timeout)
        print(response.status_code)
        cookie = response.cookies.get('JSESSIONID')
        soup = BeautifulSoup(response.text, 'lxml')
        javax = soup.find('input', {'name': 'javax.faces.ViewState'})['value']



        
        url = f"{self.url}/pages/home.jsf;jsessionid={cookie}"

        headers = {
            "Host": "wise-tt.com",
            "Cookie": f"JSESSIONID={cookie}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
            "Accept": "application/xml, text/xml, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Faces-Request": "partial/ajax",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://wise-tt.com",
            "Dnt": "1",
            "Referer": f"{self.url}/pages/home.jsf",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=0",
            "Te": "trailers",
            "Connection": "keep-alive"
        }

        payload1 = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:newDate",
            "javax.faces.partial.execute": "form:newDate",
            "javax.faces.partial.render": "form",
            "javax.faces.behavior.event": "dateSelect",
            "javax.faces.partial.event": "dateSelect",
            "form": "form",
            "form:j_idt142": "",
            "form:newDate_input": f"{datum}",
            "form:j_idt147_focus": "",
            "form:j_idt147_input": "1",
            "form:j_idt151_focus": "",
            "form:j_idt151_input": "4",
            "form:j_idt175_focus": "",
            "form:j_idt175_input": "0",
            "form:j_idt179_focus": "",
            "form:j_idt179_input": "0",
            "form:j_idt183_focus": "",
            "form:j_idt183_input": "0",
            "form:j_idt187_focus": "",
            "form:j_idt187_input": "4",
            "form:groupVar_selection": "",
            "form:groupVar_scrollState": "0,0",
            "form:tutorVar_selection": "",
            "form:tutorVar_scrollState": "0,0",
            "form:roomVar_selection": "",
            "form:roomVar_scrollState": "0,0",
            "form:courseVar_selection": "",
            "form:courseVar_scrollState": "0,0",
            "form:j_idt267_focus": "",
            "form:j_idt267_input": "0",
            "form:j_idt271_focus": "",
            "form:j_idt271_input": "0",
            "form:j_idt275_focus": "",
            "form:j_idt275_input": "0",
            "form:j_idt279_focus": "",
            "form:j_idt279_input": "4",
            "javax.faces.ViewState": f"{javax}"
        }

        payload2 = {
            "javax.faces.partial.ajax": "true",
            "javax.faces.source": "form:j_idt175",
            "javax.faces.partial.execute": "form:j_idt175",
            "javax.faces.partial.render": "form",
            "javax.faces.behavior.event": "change",
            "javax.faces.partial.event": "change",
            "form": "form",
            "form:j_idt142": "",
            "form:newDate_input": f"{datum}",
            "form:j_idt147_focus": "",
            "form:j_idt147_input": "1",
            "form:j_idt151_focus": "",
            "form:j_idt151_input": "4",
            "form:j_idt175_focus": "",
            "form:j_idt175_input": "30",
            "form:j_idt179_focus": "",
            "form:j_idt179_input": "0",
            "form:j_idt183_focus": "",
            "form:j_idt183_input": "0",
            "form:j_idt187_focus": "",
            "form:j_idt187_input": "4",
            "form:groupVar_selection": "",
            "form:groupVar_scrollState": "0,0",
            "form:tutorVar_selection": "",
            "form:tutorVar_scrollState": "0,0",
            "form:roomVar_selection": "",
            "form:roomVar_scrollState": "0,0",
            "form:courseVar_selection": "",
            "form:courseVar_scrollState": "0,0",
            "form:j_idt267_focus": "",
            "form:j_idt267_input": "0",
            "form:j_idt271_focus": "",
            "form:j_idt271_input": "0",
            "form:j_idt275_focus": "",
            "form:j_idt275_input": "0",
            "form:j_idt279_focus": "",
            "form:j_idt279_input": "4",
            "form:j_idt390": "Izberite udeležence pouka zgoraj (+). Za več informacij je gumb 'Pomoč'.",
            "javax.faces.ViewState": f"{javax}"
        }

        response = session.post(url, headers=headers, data=payload1, timeout=request_timeout)
        print(response.status_code)
        response = session.post(url, headers=headers, data=payload2, timeout=request_timeout)
        print(response.status_code)

        response_raw = response.text

        soup = BeautifulSoup(response_raw, "lxml")
        main_calendar = soup.find(id="mainCalendar")

        for dan in range(0, 5):
            previous = []
            for ura in range(0, 28):
                split = 0
                subject = []
                while True:
                    row = main_calendar.find("input", id=f"form:j_idt411:{ura}:j_idt417:{dan}:j_idt418:{split}:calendarHour")
                    if row == None:
                        break
                    title_value = row.get('title')
                    style = row.get("style")
                    #print(style)
                    #print(title_value)
                    if style.strip() == "cursor: zoom-in;}":
                        if len(title_value) > 2:
                            data = self.process_class_data(title_value, self.ure[ura])
                            self.calendar[self.dnevi[dan]].append(data)
                            try:
                                previous[split] = data
                            except:
                                previous.append(None)
                                previous[split] = data
                        elif len(title_value) > 1:
                            pass
                        else:
                            try:
                                if previous[split]:
                                    previous[split]["konec"] = self.ure[ura+1]
                            except:
                                pass
                    else:
                        try:
                            del previous[split]
                        except:
                            pass
                    split += 1
                    # print("Day:", dnevi[dan])
                    # print("Ura:", ure[ura])
                    # print("Split:", split)
                    # print("Previous:", previous)
                    # print(calendar)
                    # input()
                    # os.system("clear")
        return self.calendar
    
    def filter_calendar(self, filter):
        """
        filter: dict
        Ex: {"razredi": ["predmet1", "predmet2"], 'profesor': 'prof', 'zacetek': '07:00'}
        """
        output = self.calendar
        for dnevi in output.keys():
            for ura in range(0, len(output[dnevi]), 1):
                for filter_key, filter_value in filter.items():
                    if isinstance(filter_value, list):
                        if not any(fv in output[dnevi][ura][filter_key] for fv in filter_value):
                            output[dnevi][ura] = {}
                    else:
                        if len(output[dnevi][ura]) != 0 and filter_value != output[dnevi][ura][filter_key]:
                            output[dnevi][ura] = {}
        for i in self.dnevi:
            output[i] = [entry for entry in output[i] if entry]
        return output

    def get_calendar(self):
        return self.calendar
