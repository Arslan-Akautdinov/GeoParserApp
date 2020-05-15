import json


class FileReader:

    def __init__(self, text, col_path):

        self.text = text
        file = open(col_path, "w").readlines()
        self.columns = json.loads(file)
        self.list = self.calculating()
        self.rain_fall = self.get_rainfall(self.list)

    @staticmethod
    def get_average(data):

        clean_list = []

        for item in data:

            row = 0
            col = 0
            values = []
            current_sum = 0
            current_date = item["date"]

            while row < len(item["values"]):
                is_float = False
                value = item["values"][row][col]

                try:
                    current_sum += float(value.replace(",", "."))
                    is_float = True
                    row += 1
                except Exception as ex:
                    print(ex)

                if is_float is not False:
                    if row == len(item["values"]) - 1:
                        values.append(current_sum/row)
                        current_sum = 0
                        row = 0
                        col += 1
                else:
                    col += 1
                    current_sum = 0
                    row = 0
                    values.append(value)

                if col == len(item["values"][0]) - 1:
                    clean_list.append({"date": current_date, "middle": values.copy()})
                    break

        return clean_list

    @staticmethod
    def get_data(groups, dates):

        temp_collection = []
        date_count = 0
        iterator = 0
        data = []

        while iterator < len(groups):

            # Выбор текущей группы.
            group = groups[iterator]

            # Выбор текущей даты.
            current_date = group[0]

            # Выбор текущего времени.
            current_time = group[1]

            # Пердыдущая дата в списке.
            prev_date = dates[date_count]

            # Врменное хранилище информации.
            temp_collection.append(group)

            # Условие для записи последнего дня.
            last_day_record = current_time == "00:00" and date_count == len(dates) - 2

            # Если текущая дата не равна следующей и имеет время 0:30 или дата последняя.
            if current_date != prev_date and current_time == "0:30" or last_day_record:

                # Добавляем дату.
                data.append({"date": prev_date, "values": temp_collection.copy()})

                # Очищаем список.
                temp_collection.clear()

                # Переходим к следующей дате.
                date_count += 1

                # Забираем значение из предыдущнго дня.
                if date_count <= len(dates):

                    # На элемент назад.
                    iterator -= 1

            # Переходим к следующему элементу.
            iterator += 1

        return data

    @staticmethod
    def get_dates(groups):
        dates = []
        for group in groups:
            if group[0] not in dates:
                dates.append(group[0])
        return dates

    @staticmethod
    def get_groups(text):
        result = []

        # Получение элементов.
        for line in text:
            result.append(line.replace("\t", " ")
                              .replace("\n", "")
                              .split(" "))

        # Удаление лишних столбцов.
        if "Date" in result[1]:
            result.remove(result[0])
            result.remove(result[0])

        return result

    @staticmethod
    def get_rainfall(data):
        sum_rain = 0
        for rain_fall in data:
            sum_rain += rain_fall["middle"][17]
        return sum_rain

    def calculating(self):

        groups = self.get_groups(self.text)

        dates = self.get_dates(groups)

        data = self.get_data(groups, dates)

        return self.get_average(data)