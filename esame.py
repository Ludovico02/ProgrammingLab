class ExamException(Exception):
    pass # raise ExamException('Errore')

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
        self.can_read = True
        try:
            my_file = open(self.name, "r")
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print("Errore in apertura del file: {}".format(e))

    def get_data(self):
        if not self.can_read:
            print("Errore, file non aperto o illeggibile")
            return None
        data = []
        my_file = open(self.name, "r")
        for line in my_file:
            elements = line.split(",")

            # rimuovo eventuali spazi o "a capo" dagli elementi
            elements[-1] = elements[-1].strip()
            elements[0] = elements[0].strip()

            try:
                elements[-1] = int(elements[-1])
            except:
                print("Uso valore di default") # togliere?
                # dato che il numero non è convertibile in intero, il numero è una str
                elements[-1] = None # se non è un numero metto a none
            
            if elements[0] != "date": # aggiungere verifiche?
                data.append(elements)
            
        my_file.close()
        return data

# time series è la lista completa, years = [1948, 1949]
def detect_similar_monthly_variations(time_series, years):
    if len(years) > 2:
        raise ExamException("Non deve avere più di 2 valori")
    if years[0] != years[1] - 1:
        if years[0] - 1 == years[1]: # se il primo anno è maggiore del secondo
            years[0], years[1] = years[1], years[0]
        else:
            raise ExamException("Gli anni non sono consecutivi")
    
    first_year_i, first_found, second_year_i, second_found = 0, False, 0, False
    for i, list in enumerate(time_series):
        if str(years[0]) in list[0] and first_found == False:
            first_year_i = i
            first_found = True
        if str(years[1]) in list[0] and second_found == False:
            second_year_i = i
            second_found = True
        if first_found and second_found:
            break
    print(first_year_i, second_year_i)

    first, second = [], []
    for list in time_series:
        if str(years[0]) in list[0]:
            first.append(list[1])
        if str(years[1]) in list[0]:
            second.append(list[1])
    print(first)
    print(second)

    first = [abs(first[i] - first[i + 1]) for i in range(len(first) - 1)]
    second = [abs(second[i] - second[i + 1]) for i in range(len(second) - 1)]
    print(first, second)

    finale = []
    for x, y in zip(first, second):
        if abs(x - y) <= 2:
            finale.append(True)
        else:
            finale.append(False)
    print(finale)

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(time_series)

detect_similar_monthly_variations(time_series, [1949, 1950])