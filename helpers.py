from datetime import datetime
from dateutil.relativedelta import relativedelta

def isNew(release_date):
    # subtract a month off of today's time
    new_date = datetime.today() - relativedelta(months=1)
    # new_date.strftime('%Y-%M-%D')
    #print("Date to be older than: " + str(new_date))
    # format release date obj
    try:
        release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
    except:
        print("error for this album date.")
        return False

    # print("Release Date: " + str(release_date_obj))
    # perform comparison
    if new_date < release_date_obj:
        # print("Its New Music!")
        return True
    else:
        # print("Its Old News..")
        return False

