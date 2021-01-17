# -*- coding: utf-8 -*-
# _*_ coding: utf-8
import json


class FileReader:

    def __init__(self, text, col_path):
        self.text = text
        with open(col_path, encoding="UTF-8") as json_file:
            self.columns = json.loads(json_file.read())
        self.list = self.calculating()
        self.rain_fall = self.get_rainfall(self.list)



    @staticmethod
    def get_average(data):

        clean_list = []

        for date in data:
            values = []
            col_count = len(date["values"][0])
            cur_date = date["date"]
            values.append(cur_date)
            values.append("с 00:30 до 00:00")
            second_col = []

            for col in range(2, col_count):

                row_count = len(date["values"])
                values_counter = 0
                current_sum = 0
                is_added = False

                for row in range(0, row_count):

                    # Get value
                    value = date["values"][row][col]

                    # Set value type
                    try:
                        if value == "---":
                            value = 0
                        else:
                            value = float(value.replace(",", "."))
                        current_sum += value
                        values_counter += 1
                    except ValueError:
                        values.append(value)
                        is_added = True
                        break

                    if col == 2:
                        second_col.append(value)

                if current_sum != 0 and is_added is False:
                    values.append(current_sum/row_count)
                elif current_sum == 0 and is_added is False:
                    values.append("---")

            clean_list.append({"date": cur_date, "middle": values.copy()})

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

            # Если текущая дата не равна следующей и имеет время 0:30 или дата последняя.
            if current_date != prev_date:

                result = {"date": prev_date, "values": temp_collection.copy()}

                if result["values"][0][1] == "00:00":
                    result["values"].remove(result["values"][0])

                # Добавляем дату.
                data.append(result)

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
        result = []
        for rain_fall in data:
            try:
                value = float(rain_fall["middle"][17])
                result.append(value * 48)
            except Exception as ex:
                result.append(rain_fall["middle"][17])
        return result

    def calculating(self):
        groups = self.get_groups(self.text)
        dates = self.get_dates(groups)
        data = self.get_data(groups, dates)
        return self.get_average(data)
