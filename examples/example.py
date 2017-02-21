from api_extractor import RevisionExtractor
from query_handler import QueryHandler

#extractor = RevisionExtractor(payload={'titles': "Malazan Book of the Fallen"})
#extractor.remove_all()
handler= QueryHandler()
user='marvin'
date1='2015-01-01'
date2='2015-06-05'
#content = extractor.get_all()
count= handler.get_count(1001,[user,date1,date2])
print count
count= handler.get_avg(1,[user,date1,date2])
print count
#count= handler.get_mode(1)
#for c in count:
    #revid=rev['revid']
#    print c['user']

#a=handler.insert_dates()
#a=handler.get_dates()

