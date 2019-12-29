# -*- coding: UTF-8 -*-
import csv
from datetime import datetime, timezone
from io import BytesIO

import xlwt
import arrow
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from tasks.models import Task
from users.models import User


class File_Exporter():
    def __init__(self, columns, filename, file_type):
        self.columns = columns
        self.file_type = file_type
        self.f_name = filename + " " + datetime.now().strftime('%Y-%m-%d') + "." + file_type

    def generate_excel(self, data, sheet_name):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=' + self.f_name

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheet_name)  # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(self.columns)):
            ws.write(row_num, col_num, self.columns[col_num], font_style)  # at 0 row 0 column

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in data:
            row_num += 1
            for col_num in range(len(row)):
                if col_num == 0:
                    ws.write(row_num, col_num, Task.objects.get(id=row[col_num]).title, font_style)
                elif col_num == 1:
                    ws.write(row_num, col_num, arrow.get(row[col_num]).format('YYYY-MM-DD HH:mm:ss'), font_style)
                elif col_num == 2:
                    ws.write(row_num, col_num, User.objects.get(id=row[col_num]).username, font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    def generate_csv(self, data):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + self.f_name

        writer = csv.writer(response)
        writer.writerow(self.columns)

        for task_flow in data:
            writer.writerow(
                [task_flow.task, task_flow.created_on, task_flow.transferred_by, task_flow.description])
        return response

    def generate_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None
