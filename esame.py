'''
- se il file è vuoto semplicemente non sono presenti gli anni in time_series quindi si alza un eccezzione
- la data deve avere il -
'''

class ExamException(Exception):
    pass # raise ExamException('Errore')

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name

    def get_data(self):
        try:
            my_file = open(self.name, "r")
            my_file.readline()
        except Exception as e:
            raise ExamException("Errore in apertura del file: {}".format(e))

        data = []
        my_file = open(self.name, "r")
        for line in my_file:
            elements = line.split(",")

            # tolgo tutti gli spazi dagli elementi
            elements = [element.replace(" ", "").strip() for element in elements]

            # in caso ci siano più di 2 elementi separati dalla virgola
            # il primo elemento deve comunque essere una data
            if len(elements) > 2 and elements[0].count("-") == 1 and elements[0].replace("-", "").isnumeric():
                aux, num = elements[0], ""
                num_found = False
                for element in elements:
                    if element.isnumeric() and not num_found:
                        num_found = True
                        num = element
                elements = [aux, num]

            # se il primo elemento è una data, deve avere solo 1 - e senza di quello dev'essere un numero
            if elements[0].count("-") == 1 and elements[0].replace("-", "").isnumeric() and len(elements) == 2:

                try:
                    elements[-1] = int(elements[-1])
                except:
                    elements[-1] = None

                # accetto solo i valori maggiori di 0
                if elements[-1] != None and elements[-1] <= 0:
                    elements[-1] = None

                verify_month, verify_year = True, True
                # verifica del mese
                # il mese non è convertibile in intero se non è presente, es. 1918-
                try:
                    month = int(elements[0][elements[0].find("-") + 1:])
                except:
                    verify_month = False
                # il mese deve essere un numero compreso fra 1 e 12
                if  month > 12 or month < 1:
                    verify_month = False

                # verifica dell' anno
                # l'anno non è convertibile in intero se non è presente, es. -02
                try:
                    year = int(elements[0][:elements[0].find("-")])
                except:
                    verify_year = False
                # considero che l'anno possa essere un valore qualsiasi purchè non negativo
                if year <= 0:
                    verify_year = False
                    
                # se sia l'anno che il mese sono validi
                if verify_year and verify_month:
                    if len(data) >= 1:
                        # salvo l'anno e il mese dell'elemento precedente, questo esiste solo se è già presente un elemento
                        data_year = int(data[len(data) - 1][0][:data[len(data) - 1][0].find("-")])
                        data_month = int(data[len(data) - 1][0][data[len(data) - 1][0].find("-") + 1:])

                    # considero gli anni e i mesi in ordine crescente
                    if len(data) >= 1:
                        if data_year > year:
                            raise ExamException("Anno fuori ordine")
                        if data_month > month and year == data_year:
                            raise ExamException("Mese fuori ordine")
                    
                    # verifico di non aver mai caricato quell'elemento
                    for el in data:
                        if elements[0] in el:
                            raise ExamException("Data duplicata")

                    # se non ho alzato eccezioni aggiungo gli elementi
                    data.append(elements)
            
        my_file.close()
        return data

# time series è la lista completa, years = [1948, 1949]
def detect_similar_monthly_variations(time_series, years):
    if len(years) > 2:
        raise ExamException("Il vettore non deve avere più di 2 valori")
    if len(years) < 2:
        raise ExamException("Il vettore deve avere 2 valori")

    try:
        years[0] = int(years[0])
        years[1] = int(years[1])
    except:
        raise ExamException("nni devono essere numeri interi")

    # in caso gli anni vengano inseriti al contrario li scambio altrimenti alzo un'eccezione
    if years[0] != years[1] - 1:
        if years[0] - 1 == years[1]: # se il primo anno è maggiore del secondo
            years[0], years[1] = years[1], years[0]
        else:
            raise ExamException("Anni non consecutivi")

    # verifico che gli anni inseriti siano presenti all'interno di time_series
    first_found, second_found = False, False
    for list in time_series:
        if str(years[0]) in list[0]:
            first_found = True
        if str(years[1]) in list[0]:
            second_found = True
        if first_found and second_found:
            break

    # se gli anni non sono presneti alzo un'eccezzione
    if not first_found or not second_found:
        raise ExamException("Uno dei due anni non è presente nella lista")

    # aggiungo a delle liste i valori corrispondenti alle date
    first, second = [None] * 12, [None] * 12
    for list in time_series:
        if str(years[0]) in list[0]:
            first[int(list[0][list[0].find("-") + 1:]) - 1] = list[1]
        if str(years[1]) in list[0]:
            second[int(list[0][list[0].find("-") + 1:]) - 1] = list[1]

    # faccio le sottrazioni fra gli elementi del vettore stesso, se sottraggo un valore con None, inserisco None
    first = [None if first[i] == None or first[i + 1] == None else first[i + 1] - first[i] for i in range(len(first) - 1)]
    second = [None if second[i] == None or second[i + 1] == None else second[i + 1] - second[i] for i in range(len(second) - 1)]

    finale = []
    for x, y in zip(first, second):
        if x == None or y == None:
            finale.append(False)
        elif abs(x - y) <= 2:
            finale.append(True)
        else:
            finale.append(False)
    return finale

# time_series_file = CSVTimeSeriesFile(name='data.csv')
# time_series = time_series_file.get_data()

# print(detect_similar_monthly_variations(time_series, [1949, 1950]))
