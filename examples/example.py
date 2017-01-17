from api_extractor import RevisionExtractor

extractor = RevisionExtractor(payload={'titles': "Malazan Book of the Fallen"})
#extractor.remove_all()
content = extractor.get_all()


