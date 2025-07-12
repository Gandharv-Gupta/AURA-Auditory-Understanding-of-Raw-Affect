-Unique emotions: [48]
['Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement', 'Anger', 'Anxiety', 'Awe', 'Awkwardness', 'Boredom', 'Calmness', 'Concentration', 'Confusion', 'Contemplation', 'Contempt', 'Contentment', 'Craving', 'Desire', 'Determination', 'Disappointment', 'Disgust', 'Distress', 'Doubt', 'Ecstasy', 'Embarrassment', 'Empathic Pain', 'Entrancement', 'Envy', 'Excitement', 'Fear', 'Guilt', 'Horror', 'Interest', 'Joy', 'Love', 'Nostalgia', 'Pain', 'Pride', 'Realization', 'Relief', 'Romance', 'Sadness', 'Satisfaction', 'Shame', 'Surprise (negative)', 'Surprise (positive)', 'Sympathy', 'Tiredness', 'Triumph']

#Run commands:
(to run: cntrl+shift+v)

# Run command:
- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# create env:
- py -3.10 -m venv .venv

# Activate .venv:
- .venv/scripts/activate.ps1

# Run chroma:
-  chroma run --path ./chroma_store

# Uvicorn:
- uvicorn main:app --reload
