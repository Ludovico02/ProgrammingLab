'''
- se il file è vuoto semplicemente non sono presenti gli anni in time_series quindi si alza un eccezzione
- timestamp duplicato 
- la data deve avere il - ?
'''
# import re

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
            
            elements = [element.replace(" ", "").strip() for element in elements]

            if len(elements) > 2:
                aux, num = "", ""
                data_found, num_found = False, False
                for element in elements:
                    if "-" in element and element.replace("-","").isnumeric() and not data_found:
                        data_found = True
                        aux = element
                    if element.isnumeric() and not num_found:
                        num_found = True
                        num = element
                elements = [aux, num]

            # rimuovo eventuali spazi o "a capo" dagli elementi
            # elements[-1] = elements[-1].strip()
            # elements[0] = elements[0].strip()

            try:
                elements[-1] = int(elements[-1])
            except:
                # dato che il numero non è convertibile in intero, il numero è una str
                elements[-1] = None

            if elements[-1] != None and elements[-1] <= 0: # se il valore è minore di 0 o nullo (= 0)
                elements[-1] = None

            if len(elements) < 2:
                elements.insert(0, "")
        
            # if re.match("[0-9\-]*$", elements[0]): # aggiungere verifiche?
            #     data.append(elements)
            if "-" in elements[0] and elements[0].replace("-", "").isnumeric():
                data.append(elements)
            
        my_file.close()
        return data

# time series è la lista completa, years = [1948, 1949]
def detect_similar_monthly_variations(time_series, years):
    if len(years) > 2:
        raise ExamException("Non deve avere più di 2 valori")

    try:
        years[0] = int(years[0])
        years[1] = int(years[1])
    except:
        raise ExamException("Gli anni devono essere numeri interi")

    if years[0] != years[1] - 1:
        if years[0] - 1 == years[1]: # se il primo anno è maggiore del secondo
            years[0], years[1] = years[1], years[0]
        else:
            raise ExamException("Gli anni non sono consecutivi")
    
    first_found, second_found = False, False
    for list in time_series:
        if str(years[0]) in list[0] and first_found == False:
            first_found = True
        if str(years[1]) in list[0] and second_found == False:
            second_found = True
        if first_found and second_found:
            break
    
    if not first_found or not second_found:
        raise ExamException("Uno dei due anni non è presente nella lista")

    first, second = [], []
    for list in time_series:
        if str(years[0]) in list[0]:
            first.append(list[1])
        if str(years[1]) in list[0]:
            second.append(list[1])
    print(first)
    print(second)

    first = [None if first[i] == None or first[i + 1] == None else abs(first[i] - first[i + 1]) for i in range(len(first) - 1)]
    # for i in range(len(first) - 1):
    #     if first[i] == None or first[i + 1] == None:
    #         first[i] = None
    #     else:
    #         first[i] = abs(first[i] - first[i + 1])
    # first.pop()
    second = [None if second[i] == None or second[i + 1] == None else abs(second[i] - second[i + 1]) for i in range(len(second) - 1)]
    # for i in range(len(second) - 1):
    #     if second[i] == None or second[i + 1] == None:
    #         second[i] = None
    #     else:
    #         second[i] = abs(second[i] - second[i + 1])
    # second.pop()
    print(first)
    print(second)

    finale = []
    for x, y in zip(first, second):
        if x == None or y == None:
            finale.append(False)
        elif abs(x - y) <= 2:
            finale.append(True)
        else:
            finale.append(False)
    for i in range(12 - len(finale)):
        finale.append(False)
    print(finale, len(finale)) # return

'''
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(time_series)

detect_similar_monthly_variations(time_series, [1949, 1950])
'''
time_series_file = CSVTimeSeriesFile(name='dati_sbagliati.csv')
time_series = time_series_file.get_data()
print(time_series, len(time_series))

detect_similar_monthly_variations(time_series, [1949, 1950])