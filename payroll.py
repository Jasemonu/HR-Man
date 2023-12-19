from models import storage
from datetime import date
from models.deductions import Deduction
from models.earnings import Earning
from models.payroll import Payroll
from models.user import User



storage.connect()
#Deduction.drop_collection()
#Earning.drop_collection()

def earning(data):
    earn = Earning(**data)
    try:
        earn.save()
    except Exception as e:
        print(e)
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
            'staff_number': earn.staff_number,
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
    period = date.today().strftime('%B_%y')
    name = salary.get('staff_number') + '_' + period
    earn = earning(salary)
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
    payroll = Payroll.objects(name=name).first()
    if payroll:
        items = payroll.items
        items.append(obj)
        payroll.update(items=items)
        payroll.save()
    else:
        payroll = Payroll(name=name, items=[obj])
        payroll.save()
    return payroll.id


