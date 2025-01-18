from datetime import datetime
def dateComparison(date):
    todays_date = datetime.now().date()         
    date_format = '%Y-%m-%d'
    date = datetime.strptime(date,date_format).date()
    difference = (todays_date - date).days
    if difference < 15:
        return ("checkbox-marked-circle",[39/256,174/256,96/256,1],"Safe")
    elif difference > 15 and difference < 30:
        return ("alert",[39/256,174/256,96/256,1],"Caution")
    else:
        return ("alert-circle",[39/256,174/256,96/256,1],"Danger")