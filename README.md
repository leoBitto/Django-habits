# Habits App

Questo progetto Django è progettato per aiutarti a gestire e monitorare le tue abitudini quotidiane. Le principali entità del sistema sono rappresentate dai seguenti modelli:

## Category
Il modello `Category` rappresenta una categoria a cui un'abitudine può essere associata. Ogni categoria ha un nome, un colore predefinito e un'icona opzionale.

## Habit
Il modello `Habit` rappresenta un'abitudine e può essere associato a una categoria specifica tramite una relazione ForeignKey. Ogni abitudine ha un nome unico, una categoria e un campo booleano `is_positive` che indica se l'abitudine è considerata positiva o negativa. Se un'abitudine è positiva, il goal può essere considerato raggiunto se il numero di eventi completati è superiore al target. Se un'abitudine è negativa, il goal può essere considerato raggiunto se il numero di eventi completati è inferiore al target.

## HabitEvent
Il modello `HabitEvent` tiene traccia degli eventi specifici legati all'abitudine. Ogni evento ha un riferimento all'abitudine associata, una data, un'ora opzionale, una posizione opzionale e uno stato booleano `completed` che indica se l'abitudine è stata completata durante quell'evento.

