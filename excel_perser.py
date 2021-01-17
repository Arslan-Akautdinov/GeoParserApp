# -*- coding: utf-8 -*-
# _*_ coding: utf-8
import xlsxwriter
from file_reader import FileReader


class ExcelParser:

    def __init__(self, data, out_path):
        self.data: FileReader = data
        self.out_path = out_path

    def export_document(self, document_name, titles):

        workbook = xlsxwriter.Workbook(f'{self.out_path}/{document_name}.xlsx')
        worksheet = workbook.add_worksheet()
        col_cell = 0
        row = 1
        last_cell = 0

        for title in titles:
            worksheet.write(0, col_cell, title)
            col_cell += 1

        for item in self.data.list:
            cell = 0
            for exp in item["middle"]:
                worksheet.write(row, cell, exp)
                cell += 1
                last_cell = cell
            row += 1

        worksheet.write(0, last_cell, "СУММА ВСЕХ ОСАДКОВ")

        row = 1
        for rain in self.data.rain_fall:
            worksheet.write(row, last_cell, rain)
            row += 1

        workbook.close()
