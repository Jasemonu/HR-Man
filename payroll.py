from models import storage
from datetime import date
from models.deductions import Deduction
from mongoengine.errors import NotUniqueError
from models.earnings import Earning
from models.payroll import Payroll
from models.user import User



storage.connect()
#Deduction.drop_collection()
#Earning.drop_collection()

def earning(data, user, period):
    obj = {
            'staff': user,
            'period': period,
            'basic': data.get('basic'),
            'overtime': data.get('overtime'),
            'allawance': data.get('allawance'),
            'bonus': data.get('bonus'),
            'gross': data.get('gross')
            }

    earn = Earning(**obj)
    try:
        earn.save()
    except Exception as e:
        return None
    return earn

def deduction(earn):
    #earn = Earning.objects(staff_number=staff_number).first()
    if not earn:
        return None
    SSNIT = earn.basic * (13 / 100)
    tax = earn.gross * (15 / 100)
    tier_two = earn.basic * (5 / 100)
    tier_three = earn.basic * (5 / 100)
    obj = {
            'staff': earn.staff,
            'period': earn.period,
            'SSNIT': SSNIT,
            'tax': tax,
            'tier_two': tier_two,
            'tier_three': tier_three,
            'total': SSNIT + tax + tier_two + tier_three
            }
    deduct = Deduction(**obj)
    try:
        deduct.save()
    except Exception:
        return None
    return deduct

def create_payroll(salary, user):
    period = date.today().strftime('%B_%Y')
    earn = earning(salary, user, period)
    if earn is None:
        return None
    deduct = deduction(earn)
    if deduct is None:
        return None
    obj = {
            'staff_number': user.staff_number,
            'full_name': user.first_name + ' ' + user.last_name,
            'gross': earn.gross,
            'deductions': deduct.total,
            'net': earn.gross - deduct.total
            }
    payroll = Payroll.objects(name=period).first()
    if payroll:
        items = payroll.items
        for item in items:
            if user.staff_number in item.values():
                return 'exists'
        items.append(obj)
        try:
            payroll.update(items=items)
            payroll.save()
        except NotUniqueError:
            return 'exists'
    else:
        payroll = Payroll(name=period, items=[obj])
        payroll.save()
    return payroll.id


