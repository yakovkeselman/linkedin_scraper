from datetime import date
import re


def time_divide(s1: str):
    """Extracts start and end dates from LI string"""

    d = date.today()
    moy = d.strftime('%b %Y')
    if s1.endswith('Present'):
        s1 = s1.replace('Present', moy)

    arr = s1.split(' ')
    time_from, time_to = None, None
    if len(arr) >= 4:
        arr = arr[-4:]
        if re.match(r'\d+', arr[-2]):
            time_from = arr[-2]
            time_to = arr[-1]
        else:
            time_from = ' '.join(arr[:2])
            time_to = ' '.join(arr[2:])

    return time_from, time_to


if __name__ == '__main__':
    input1 = 'Dates Employed Jan 2014 May 2014'
    assert time_divide(input1) == ('Jan 2014', 'May 2014')
    input2 = 'Dates attended or expected graduation 2008 2012'
    assert time_divide(input2) == ('2008', '2012')
