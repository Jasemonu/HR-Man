import os
from datetime import date
from models.payslip import Payslip
from models import storage
from models.user import User
from models.earnings import Earning
from models.deductions import Deduction
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont


storage.connect()
def check_earning(staff_number):
    earn = Earning.objects(staff_number=staff_number).first()
    if earn:
        return earn
    return None


def getperiod(data):
    period_list = data.get('period').split('-')
    year = int(period_list[0])
    month = int(period_list[1])
    day = int(period_list[1])
    return date(year, month, day).strftime("%B_%y")

company = 'Niche Cocoa Industry'
info = 'Salary for '
folder = 'static/assets/pdf'
def create_payslip(data, staff):
    earn = check_earning(data.get('staff_number'))
    if earn is None:
        return "Null"

    try:
        deduct = Deduction.objects(staff_number=staff.staff_number).first()
    except Exception as e:
        print(e)
        return None
    period = getperiod(data)

    name = f'{staff.staff_number}_{period}.pdf'

    payslip = Payslip.objects(name=name).first()
    if payslip:
        return 'exists'

    width, height = A4

    c = canvas.Canvas(f'{folder}/{name}', pagesize=A4)

    c.setFont('Times-Roman', 30)
    text_width = stringWidth(company, 'Times-Roman', 30)
    c.drawString((width - text_width) / 2, 790, company)

    c.setFont('Times-Roman', 25)
    text_width = stringWidth(info + period, 'Times-Roman', 25)
    c.drawString((width - text_width) / 2, 760, info + period)

    c.setLineWidth(1)
    c.line(10, 755, 585, 755)

    c.setFont('Times-Roman', 18)
    text_width = stringWidth('Earnings', 'Times-Roman', 18)
    c.drawString((width - text_width) / 2, 730, 'Earnings')

    c.setLineWidth(1)
    c.line(10, 725, 585, 725)

    c.setFont('Times-Roman', 15)
    c.drawString(100, 710, 'Staff Number:  ')
    c.drawString(300, 710, staff.staff_number)

    c.drawString(100, 685, 'Employee Name:  ')
    c.drawString(300, 685, f'{staff.first_name} {staff.last_name}')

    c.drawString(100, 660, 'Basic:  ')
    c.drawString(300, 660, str(earn.basic))

    c.drawString(100, 635, 'Overtime:  ')
    c.drawString(300, 635, str(earn.overtime))

    c.drawString(100, 610, 'Allawance:  ')
    c.drawString(300, 610, str(earn.allawance))

    c.drawString(100, 585, 'Bonuses:  ')
    c.drawString(300, 585, str(earn.bonus))

    c.drawString(100, 560, 'Gross:  ')
    c.drawString(300, 560, str(earn.gross))

    c.setLineWidth(1)
    c.line(10, 545, 585, 545)

    c.setFont('Times-Roman', 18)
    text_width = stringWidth('Deductions', 'Times-Roman', 18)
    c.drawString((width - text_width) / 2, 530, 'Deductions')

    c.setFont('Times-Roman', 15)
    c.drawString(100, 505, 'SSNIT:  ')
    c.drawString(300, 505, str(deduct.SSNIT))

    c.drawString(100, 480, 'Tax:  ')
    c.drawString(300, 480, str(deduct.tax))

    c.drawString(100, 455, 'Tax:  ')
    c.drawString(300, 455, str(deduct.tax))

    c.drawString(100, 430, 'Tier Two:  ')
    c.drawString(300, 430, str(deduct.tier_two))

    c.drawString(100, 405, 'Tier Three:  ')
    c.drawString(300, 405, str(deduct.tier_three))

    c.setLineWidth(1)
    c.line(10, 390, 585, 390)

    c.setFont('Times-Roman', 18)
    text_width = stringWidth('Take Home', 'Times-Roman', 18)
    c.drawString((width - text_width) / 2, 375, 'Take Home')

    c.setFont('Times-Roman', 15)
    c.drawString(100, 350, 'Net:  ')
    c.drawString(300, 350, str(earn.gross - deduct.total))

    c.setFont('Times-Roman', 10)
    c.drawString(250, 25, 'HR solutions powered by @HR-MAN')

    c.showPage()
    c.save()

    for path in os.listdir(folder):
        if path == name:
            payslip = Payslip(period=period, staff_number=staff.staff_number, name=name)
            payslip.save()
            return payslip
    return None
