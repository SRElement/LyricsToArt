import spacy

class PromptGenerator():
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.excluded_tags = {"ADJ","NOUN","PROPN","VERB"}

    def generatePromtFromString(self, text):
        doc = self.nlp(text.lower())

        prompt = []
        for token in self.nlp(doc):
            if token.pos_ in self.excluded_tags:
                prompt.append(token.text)
        if prompt == []:
            prompt = [text]
        return ' '.join(prompt)
        


