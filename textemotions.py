from transformers import pipeline

class TextToEmotion():
    
    def __init__(self):
        self.emotionModel = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
        self.emotionLabel = ''

    def emotion(self, prompt):
        self.emotionLabel = self.emotionModel(prompt)
        return self.emotionLabel
    
    def labelEmotionsFromList(self, list):
        emotionList = []
        for i in range(0,len(list)):
            emotionList.append(self.emotionModel(list[i])[0]['label'])
        print(emotionList)
        return emotionList




