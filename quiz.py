#1e vragen gaan over niveau
quiz_questions = [
        {
        "question": "Welke stelling past het beste bij jou?",
        "answers": [
            {"text": "Je weet wat AI is, maar gebruikt het niet of nauwelijks bwust", "score": 1},
            {"text": "Je gebruikt AI oppervlakkig en soms in je werk, voornamelijk generatieve AI ter ondersteuning van je werkzaamheden", "score": 2},
            {"text": "Je gebruikt AI regelmatig in projecten en je werkzaamheden en hebt mogelijk al geëxperimenteerd met het bouwen van modellen met een ICT-er", "score": 3},
            {"text": "Je hebt veel kennis en kan zelf AI Modellen bouwen", "score": 4}
        ]
    },
    {
        "question": "Hoe vaak gebruik je in jouw werkzaamheden technologieën als kunstmatige intelligentie? ",
        "answers": [
            {"text": "Zelden tot nooit", "score": 1},
            {"text": "Af en toe", "score": 3},
            {"text": "Periodiek", "score": 6},
            {"text": "Dagelijks", "score": 10}
        ]
    },
    {
        "question": "Hoe schat je jouw eigen kennis en vaardigheid in rond inzet van kunstmatige intelligentie? ",
        "answers": [
            {"text": "Ik ben er niet of nauwelijks mee bekend", "score": 1},
            {"text": "Ik ben bekend met de belangrijke concepten en termen van kunstmatige intelligentie", "score": 3},
            {"text": "Ik weet wat generatieve AI is en welke generatieve AI-systemen in zou kunnen gebruiken in mijn werk", "score": 5},
            {"text": "Ik heb generatieve AI-tekstsystemen, beelgeneratiesystemen of andere generatieve AI-systemen ingezet", "score": 7}, 
            {"text": "Ik heb enige ervaring met het gebruiken van AI in projecten", "score": 10},
            {"text": "Ik heb ervaring met het bouwen van AI-modellen (alleen of samen met een ICT’er", "score": 20}
            
        ]
    },
    # vragen hier over topci
       # Assume more questions similar to the above
    {
        "question": "Kies het onderwerp dat je het meest interesseert:",
        "answers": [
            {"text": "Machinelearning en AI", "topic": "MLAI"},
            {"text": "Data analysis and cleaning", "topic": "DACL"},
            {"text": "AI, ethiek en maatschappelijke gevolgen", "topic": "AIETHIC"},
            {"text": "Generatieve AI & Prompting", "topic": "GENAI"},
        ]
    },

]

def get_question(question_id):
    """Fetch a single quiz question by its ID."""
    if 0 <= question_id < len(quiz_questions):
        return quiz_questions[question_id]
    else:
        return {"error": "Question not found"}

