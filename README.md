# Designing Journalism

repo containing (for now) an rss file containing info about AI courses fit for journalists. 

# RPO Elearning selector prototype

Deze applicatie is een prototype van een Quickscan tool die gebruikers helpt om een passende selectie van e-learnings te vinden, gebaseerd op hun AI-niveau en interesses. Momenteel is er één ontwikkelde quizlijn rondom kunstmatige intelligentie (AI). Toekomstige uitbreidingen zullen lijnen voor Innovatie en Cybersecurity omvatten.

## Installatie

1. Clone de repository.
2. Zorg dat python geinstalleerd is
3. Create a virtual environment in dir .venv :  https://docs.python.org/3/library/venv.html
4. Activate the .venv
5. pip install -r requirements.txt       (installas requirements)
6. Start the web app :  python app.py
7. open browser op (by default)  http://localhost:5000


## Functies

- **Quiz**: Gebruikers kunnen een quiz invullen om hun AI-kennisniveau te bepalen.
- **E-learnings Aanbevelingen**: Op basis van de quizresultaten worden gepersonaliseerde e-learning aanbevelingen gedaan.
- **Filteren**: Gebruikers kunnen de aanbevolen e-learnings filteren op basis van beschikbare tijd, type en onderwerpen.

## Installatie en Gebruik

### Vereisten

- Python 3.x
- Flask
- jQuery

### Starten van de Applicatie

1. Start de Flask server:
    ```sh
    python app.py
    ```

2. Open een webbrowser en ga naar `http://localhost:5000`.

## Architectuur

De applicatie bestaat uit de volgende onderdelen:

### Frontend

- **quiz.html**: De hoofdquizpagina waar gebruikers vragen beantwoorden. Deze pagina laadt dynamisch quizvragen en toont ze aan de gebruiker.
- **elearnings.html**: De pagina waar gefilterde e-learning resultaten worden weergegeven op basis van de quizresultaten en gebruikersfilters.
- **quiz.js**: Dit script bevat de logica voor het laden van quizvragen en het verwerken van antwoorden. Het communiceert met de server om nieuwe vragen op te halen en verwerkt gebruikersantwoorden om de quiz voort te zetten of te voltooien.
- **script.js**: Dit script bevat de logica voor het filteren en weergeven van e-learning resultaten. Het haalt resultaten op van de server en toont deze aan de gebruiker, terwijl het ook dynamisch filters toepast op basis van gebruikersinvoer.

### Backend

- **app.py**: Dit is het hoofdbestand van de applicatie dat de Flask server opzet en de verschillende routes definieert. Het behandelt aanvragen voor quizvragen, quizresultaten en gefilterde e-learning aanbevelingen.
- **quiz.py**: Dit bestand bevat de logica voor het genereren en beheren van quizvragen. Het zorgt ervoor dat elke gebruiker relevante en willekeurige vragen krijgt op basis van de geselecteerde quizlijn.
- **scoring.py**: Dit bestand bevat de logica voor het berekenen van de scores op basis van de antwoorden van de gebruiker. Het helpt bij het bepalen van het AI-niveau van de gebruiker.
- **filtering.py**: Dit bestand bevat de logica voor het filteren van de e-learning resultaten op basis van de invoer van de gebruiker, zoals beschikbare tijd, type e-learning en geselecteerde onderwerpen.

### Data

- **Elearnings.xlsx**: Dit Excel-bestand bevat details van de beschikbare e-learning cursussen, zoals titel, tijdsinvestering, onderwerp en aanbieders. De gegevens uit dit bestand worden gebruikt om gebruikers aanbevelingen te doen op basis van hun quizresultaten en geselecteerde filters.

## Gebruik

- **Quiz**: Gebruikers starten de quiz op de quizpagina. De quizvragen worden dynamisch geladen en gebruikers kunnen antwoorden door op de juiste knoppen te klikken. Aan het einde van de quiz worden de resultaten doorgestuurd naar de volgende pagina voor e-learning aanbevelingen.
- **E-learning Aanbevelingen**: Na het voltooien van de quiz worden gebruikers doorgestuurd naar de e-learning aanbevelingen pagina. Hier zien ze een lijst van aanbevolen cursussen gebaseerd op hun quizresultaten.
- **Filteren**: Op de e-learning aanbevelingen pagina kunnen gebruikers filters instellen om de resultaten verder aan te passen aan hun voorkeuren. Filters omvatten beschikbare tijd, type e-learning en specifieke onderwerpen.

## Logica

- **Quiz Logica**: De quizvragen en antwoorden worden geladen via AJAX-aanvragen naar de server. Elke vraag kan punten opleveren of een specifiek onderwerp selecteren. Gebruikers klikken op antwoorden en de logica in `quiz.js` verwerkt deze antwoorden, houdt de score bij en bepaalt het geselecteerde onderwerp. Zodra de quiz is voltooid, worden de resultaten doorgestuurd naar de server voor verdere verwerking.
- **E-learning Filter Logica**: De filters op de e-learning aanbevelingen pagina maken gebruik van jQuery om dynamisch de lijst van aanbevolen cursussen bij te werken. Gebruikers kunnen schuifregelaars en selectievakjes gebruiken om hun voorkeuren aan te geven, en de logica in `script.js` haalt de gefilterde resultaten op van de server en toont deze aan de gebruiker.

## Toekomstige Uitbreidingen

- Toevoegen van nieuwe quizlijnen voor Innovatie en Cybersecurity.
- Verbeteren van de gebruikersinterface en de gebruiksvriendelijkheid.
- Integreren van meer geavanceerde filteropties en e-learning aanbevelingen.

## Bijdragen

Bijdragen aan dit project zijn welkom. Voel je vrij om pull requests te openen of issues te melden.

## Licentie

Dit project is gelicentieerd onder de MIT-licentie. Zie de `LICENSE` file voor meer informatie.

