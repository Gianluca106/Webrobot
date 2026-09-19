# Web Robot - HTTP Header Stats

A web app built with Python (Flask) that analyzes the HTTP headers of a list of URLs. The app displays aggregated statistics on:

- Servers used
- Content type returned
- Content encoding

Results are shown as dynamic charts powered by Chart.js, with a modern interface built with Bootstrap.

## Tech Stack

- Python 3
- Flask
- Chart.js
- Bootstrap (Bootswatch themes: Flatly & Darkly)
- Font Awesome

## Key Features

- Bulk URL input (one per line)
- HTTP header analysis with metadata collection
- Interactive charts (server, content type, encoding)
- Welcome modal on startup
- History of recent analyses
- Light/dark mode support
- Export results to CSV

## Project Structure

- `app.py`: main Flask application
- `templates/`: HTML templates (dynamic)
- `static/js/chart-render.js`: chart rendering script
- `requirements.txt`: required Python packages
- `history.csv`, `results.csv`: output/history files, generated at runtime

## Running Locally

**1. Clone or unzip the project**

**2. Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the app**
```bash
python3 app.py
```

The app will be available at `http://127.0.0.1:5000`

## Notes

- The project is designed to be extended in the future with filters, authentication, or more detailed analysis.
- Light/dark theme support is automatic via a toggle switch.
