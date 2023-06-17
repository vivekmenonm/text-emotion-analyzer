
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')


def get_emotion(text):
    emotion_labels = emotion(text)
    emotion_detail = [item['label'] for item in emotion_labels]
    print("The detected emotion is:", emotion_detail)
    confidence_score = str(round([item['score'] for item in emotion_labels][0]*100, 2)) + "%"
    print("The confidence score is:", confidence_score)
    return emotion_detail[0], confidence_score