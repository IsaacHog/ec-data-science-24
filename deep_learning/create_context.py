import srt
import pandas as pd
import re

with open("1.Philosophers stone.srt", "r", encoding="utf-8") as file:
    srt_data = file.read()

subtitles = list(srt.parse(srt_data))

def clean_text(text):
    text = re.sub(r"<.*?>", "", text)  # Tar bort HTML-taggar
    text = re.sub(r"{\\.*?}", "", text)  # Tar bort SRT-specifika koder
    text = text.strip()  # Tar bort onödiga mellanslag och radbrytningar
    return text

text_chunks = [clean_text(sub.content) for sub in subtitles]

df = pd.DataFrame({"text": text_chunks})
df.to_csv("context.csv", index=False)
