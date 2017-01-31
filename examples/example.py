from api_extractor import RevisionExtractor
from query_handler import QueryHandler

#extractor = RevisionExtractor(payload={'titles': "Malazan Book of the Fallen"})
#extractor.remove_all()
handler= QueryHandler()
#content = extractor.get_all()
count= handler.get_count(4,['2015-06-06',-1])
print count
#a=handler.insert_dates()
#a=handler.get_dates()

