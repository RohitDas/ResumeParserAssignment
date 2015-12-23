import nltk
def extract_entities(text):
     print "Probable Names:"
     for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            try:
                label = chunk.label()
                if label == "PERSON":
                    leaves =  chunk.leaves()
                    print ' '.join([i[0] for i in leaves])
            except Exception as e:
                pass
	
             		


