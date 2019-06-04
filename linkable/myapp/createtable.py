import csv
from .models import Book
path='/Users/emsud/Documents/Linkable/datafile/'


def createTable():
    with open(path+"data.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p=Book(title=row['Title'],node=row['Node'],sellnum=row['Sellnum'],autor=row['Autor'],description=row['Description'],location=row['Location'], imagesource=row['ImageUrl'])
            p.save()