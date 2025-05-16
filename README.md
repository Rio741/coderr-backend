# Coderr Backend

Dieses Repository enthält das Backend des **Coderr Project** – eine Plattform zur Zusammenarbeit von Freelancern, entwickelt mit Django und dem Django REST Framework (DRF).

## 🚀 Features

- **Benutzerverwaltung**: Registrierung, Login und Authentifizierung von Freelancern und Auftraggebern
(z. B. über Token-basierte Authentifizierung mit DRF)
- **Anzeigen-/Projektverwaltung**: Benutzer können Projekte/Jobanzeigen erstellen, bearbeiten, löschen und durchsuchen
(z. B. mit Titel, Beschreibung, Vergütung, Kategorie etc.)
- **Kontaktverwaltung**: Verwaltung von Kontakten oder Kommunikationsdaten zwischen Benutzern
-**Adminbereich**: Voll funktionsfähige Django-Adminoberfläche zur Verwaltung aller Datenmodelle

## 🛠 Technologien

- Python
- Django
- Django REST Framework
- SQLite (als Entwicklungsdatenbank)

## 📦 Voraussetzungen

- Python 3.8+
- `pip` (meist mit Python vorinstalliert)
- `git`
- Optional: `venv` oder `pipenv` für virtuelle Umgebungen

## ⚙️ Installation (lokale Umgebung)
1. Repository klonen:
   ```bash
   git clone https://github.com/Rio741/coderr-backend.git
   cd join-backend
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python -m venv venv
   venv\Scripts\activate 
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
4. Datenbankmigrationen anwenden:
   ```bash
   python manage.py migrate
5. Entwicklungsserver starten:
   ```bash
   python manage.py runserver

## 🔐 Umgebungsvariablen

Dieses Projekt verwendet eine .env-Datei, um sensible Konfigurationen wie den SECRET_KEY sicher und flexibel zu verwalten. Diese Datei wird nicht mit dem Repository geteilt (siehe .gitignore), sondern muss lokal erstellt werden.

## 📄 Beispiel für eine .env-Datei
Erstelle im Hauptverzeichnis des Projekts (dort, wo auch manage.py liegt) eine Datei mit dem Namen .env und folgendem Inhalt:

```bash
DJANGO_SECRET_KEY=dein-geheimer-key
```
🔒 Achte darauf, dass der `DJANGO_SECRET_KEY` lang, zufällig und sicher ist. Du kannst z. B. [diesen Generator](https://djecrety.ir/) nutzen.