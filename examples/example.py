from api_extractor import RevisionExtractor

extractor = RevisionExtractor(payload={'titles': "Malazan Book of the Fallen"})
content = extractor.get_all()

