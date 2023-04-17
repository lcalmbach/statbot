context = {
    "find_theme": """Was ist das Thema für die Frage "{}", antworte mit Thema aus Liste: [{}]. 
    Die Antwort hat folgendes Format: {{"thema": Thema}}
    Wenn keine eintrag in der Liste zugeordnet werden kann: {{"thema": "unbekannt"}} 
    Beispiele:\n 
    Frage: "wieviel Erdgas wurde in Basel in 2016 verbraucht?" {{"thema": "Energie"}}\n
    Frage: "Wieviele Personen leben in Riehen in 2022?" {{"thema": "Bevölkerung"}}
    Frage: "Wo lebt mein Vater" {{"thema": "unbekannt"}}
    Frage: "Mülde frdzi gugenbroll" {{"thema": "unbekannt"}}
    """,

    "find_product": """Welcher Eintrag  aus Liste "[{}]" passt am besten zur Antwort auf die Frage "{}"?. 
    Die Antwort hat folgendes Format: {{"product": Eintrag}}
    Wenn kein Eintrag in der Liste zugeordnet werden kann: {{"product": "unbekannt"}} 
    Beispiele:\n 
    Frage: "Wieviele Kinder hat es im Gundeli-Qurtier?" {{"product": "Wohnbevölkerung nach Wohnviertel"}}\n
    Frage: "Wieviele Personen leben in Riehen in 2022?" {{"product": "Bevölkerungsstand"}}
    Frage: "Wieviele Arbeitslose über sechzig Jahre gibt es in Basel" {{"product": "Arbeitslose nach Alter"}}\n
    Frage: "Wo lebt mein Vater" {{"product": "unbekannt"}}
    Frage: "Mülde frdzi gugenbroll" {{"product": "unbekannt"}}
    """,
}