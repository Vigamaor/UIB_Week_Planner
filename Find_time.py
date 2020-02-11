import json


class Gruppe:
    def __init__(self, navn, dag, start_tid, stopp_tid, fag):
        self.navn = navn
        self.dag = dag
        self.start_tid = float(start_tid)
        self.stopp_tid = float(stopp_tid)
        self.forelesning = navn == "forelesning"
        self.fag = fag

    def __repr__(self):
        return self.navn


def hent_data():
    with open("tider.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    global info104
    global info110
    global info135
    global forelesninger

    for gruppe_data in data["INFO104"].items():
        objekt = Gruppe(gruppe_data[0], gruppe_data[1]["dag"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"], "info104")
        if objekt.forelesning:
            forelesninger.append(objekt)
        else:
            info104.append(objekt)
    for gruppe_data in data["INFO110"].items():
        objekt = Gruppe(gruppe_data[0], gruppe_data[1]["dag"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"], "info110")
        if objekt.forelesning:
            forelesninger.append(objekt)
        else:
            info110.append(objekt)
    for gruppe_data in data["INFO135"].items():
        objekt = Gruppe(gruppe_data[0], gruppe_data[1]["dag"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"], "info135")
        if objekt.forelesning:
            forelesninger.append(objekt)
        else:
            info135.append(objekt)


def sorter():
    liste_tider = []
    for fag in info104:
        for fag2 in info110:
            for fag3 in info135:
                if not (fag.dag == "torsdag" or fag2.dag == "torsdag" or fag3.dag == "torsdag" or fag.dag == "fredag" or fag2.dag == "fredag" or fag3.dag =="fredag" or fag.dag == "mandag" or fag2.dag == "mandag" or fag3.dag == "mandag"):
                    if fag.dag == "onsdag" or fag2.dag == "onsdag" or fag3.dag == "onsdag":
                        for forelesning in forelesninger:
                            if fag.dag == forelesning.dag or fag2.dag == forelesning.dag or fag3.dag == forelesning.dag:
                                if (fag.start_tid == forelesning.start_tid or (forelesning.start_tid < fag.stopp_tid and forelesning.stopp_tid > fag.start_tid)) or (forelesning.start_tid == fag2.start_tid or (fag2.start_tid < forelesning.stopp_tid and fag2.stopp_tid > forelesning.start_tid)) or (forelesning.start_tid == fag3.start_tid or (fag3.start_tid < forelesning.stopp_tid and fag3.stopp_tid > forelesning.start_tid)):
                                    #TODO her skjærer det seg
                                    continue
                        if fag.dag == fag2.dag:
                            if fag.start_tid == fag2.start_tid or (fag2.start_tid < fag.stopp_tid and fag2.stopp_tid > fag.start_tid):
                                # TODO her skjærer det seg
                                continue
                        if fag.dag == fag3.dag:
                            if fag.start_tid == fag3.start_tid or (fag3.start_tid < fag.stopp_tid and fag3.stopp_tid > fag.start_tid):
                                # TODO her skjærer det seg
                                continue
                        if fag2.dag == fag3.dag:
                            if fag2.start_tid == fag3.start_tid or (fag3.start_tid < fag2.stopp_tid and fag3.stopp_tid > fag2.start_tid):
                                # TODO her skjærer det seg
                                continue
                        liste_tider.append([fag, fag2, fag3])

    return liste_tider


info104 = []
info110 = []
info135 = []
forelesninger = []

#hent_data()
#liste_tider = sorter()
#print("hei")
