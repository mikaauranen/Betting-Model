# 1. Haetaan virallinen, kevyt Python-ympäristö
FROM python:3.11-slim

# 2. Luodaan konttiin työskentelykansio nimeltä /app
WORKDIR /app

# 3. Kopioidaan ensin riippuvuudet ja asennetaan ne
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Kopioidaan loputkin koodit (main.py, database.py jne.) konttiin
COPY . .

# 5. Määritetään komento, joka ajetaan kun kontti käynnistyy
CMD ["python", "main.py"]