import spacy

nlp = spacy.load('en_core_web_sm')
excluded_tags = {"ADJ","NOUN","PROPN","VERB"}
text = 'She said, shut up and dance with me'
doc = nlp(text.lower())

# phrases = set() 
# for nc in doc.noun_chunks:
#     phrases.add(nc.text)
#     phrases.add(doc[nc.root.left_edge.i:nc.root.right_edge.i+1].text)
# print(phrases)

new_sentence = []
for token in nlp(doc):
    print(token.pos_)
    if token.pos_ in excluded_tags:
        new_sentence.append(token.text)
print(text)
print(new_sentence)


