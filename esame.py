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

        c = 1 # contatore
        data = [["1921-01", 5]]
        my_file = open(self.name, "r")
        for line in my_file:
            elements = line.split(",")
            
            elements = [element.replace(" ", "").strip() for element in elements]

            if len(elements) > 2 and elements[0].count("-") == 1 and elements[0].replace("-", "").isnumeric():
                aux, num = elements[0], ""
                num_found = False
                for element in elements:
                    if element.isnumeric() and not num_found:
                        num_found = True
                        num = element
                elements = [aux, num]
        
            # if re.match("[0-9\-]*$", elements[0]): # aggiungere verifiche?
            #     data.append(elements)

            if elements[0].count("-") == 1 and elements[0].replace("-", "").isnumeric() and len(elements) == 2:

                try:
                    elements[-1] = int(elements[-1])
                except:
                    # dato che il numero non è convertibile in intero, il numero è una str
                    elements[-1] = None

                if elements[-1] != None and elements[-1] <= 0:
                    elements[-1] = None
                
                verify_month, verify_year = True, True

                # verifica del mese
                try:
                    month = int(elements[0][elements[0].find("-") + 1:])
                except:
                    verify_month = False
                if  month > 12 or month < 1:
                    verify_month = False

                # verifica dell' anno
                try:
                    year = int(elements[0][:elements[0].find("-")])
                except:
                    verify_year = False
                if year <= 0:
                    verify_year = False


                    
                # verifico che non ci siano duplicati
                if verify_year and verify_month:
                    if len(data) > 1:
                        if int(data[len(data) - 1][0][:data[len(data) - 1][0].find("-")]) > year:
                            raise ExamException("Anno fuori ordine")

                    if len(data) > 1:
                        if int(data[len(data) - 1][0][data[len(data) - 1][0].find("-") + 1:]) > month and month != 1:
                            print(data)
                            raise ExamException("Mese fuori ordine")
                            
                    for el in data:
                        if elements[0] in el:
                            raise ExamException("Data duplicata")
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
    first_months, second_months = [], []
    for list in time_series:
        if str(years[0]) in list[0]:
            first.append(list[1])
            first_months.append(int(list[0][list[0].find("-") + 1:]))
        if str(years[1]) in list[0]:
            second_months.append(int(list[0][list[0].find("-") + 1:]))
            second.append(list[1])
    print(first)
    print(second)
    print(first_months)
    print(second_months)

    for i in range(len(first_months) - 1):
        if i == 0 and first_months[i] != 1:
            for j in range(first_months[i] - 1):
                first.insert(j, None)
        if first_months[i] != first_months[i + 1] - 1:
            first.insert(first_months[i], None)
    if first_months[-1] != 12:
        for i in range(12 - first_months[-1]):
            first.append(None)

    for i in range(len(second_months) - 1):
        if i == 0 and second_months[i] != 1:
            for j in range(second_months[i] - 1):
                second.insert(j, None)
        if second_months[i] != second_months[i + 1] - 1:
            second.insert(second_months[i], None)
    if second_months[-1] != 12:
        for i in range(12 - second_months[-1]):
            second.append(None)

    print("primo =", first, len(first))
    print("secondo =", second, len(second))

    first = [None if first[i] == None or first[i + 1] == None else abs(first[i] - first[i + 1]) for i in range(len(first) - 1)]

    second = [None if second[i] == None or second[i + 1] == None else abs(second[i] - second[i + 1]) for i in range(len(second) - 1)]

    print("p2 =", first, len(first))
    print("s2 =", second, len(second))

    finale = []
    for x, y in zip(first, second):
        if x == None or y == None:
            finale.append(False)
        elif abs(x - y) <= 2:
            finale.append(True)
        else:
            finale.append(False)
    for i in range(11 - len(finale)):
        finale.append(False)
    print(finale, len(finale)) # return

'''
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(time_series)

detect_similar_monthly_variations(time_series, [1949, 1950])
'''
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(time_series, len(time_series))

detect_similar_monthly_variations(time_series, [1949, 1950])