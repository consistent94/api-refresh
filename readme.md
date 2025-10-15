# Historical Figures Explorer

A Python Flask web application that demonstrates API data extraction and ETL (Extract, Transform, Load) processes by fetching biographical information about historical figures from Wikipedia's REST API.

## 🎯 Project Overview

This application showcases fundamental data engineering concepts:

- **Extract**: Fetches raw data from Wikipedia's REST API
- **Transform**: Cleans, parses, and structures biographical data using Python
- **Load**: Displays transformed data through a beautiful Flask web interface

Perfect for learning Python, API integration, and data engineering fundamentals!

## 🏗️ Architecture

```
Historical Figures Explorer
├── Extract (Wikipedia API)
│   ├── Search functionality
│   ├── Page content retrieval
│   └── Infobox data extraction
├── Transform (Python Data Processing)
│   ├── Text cleaning and normalization
│   ├── Date parsing and standardization
│   ├── Category extraction
│   └── Data validation
└── Load (Flask Web Interface)
    ├── Search interface
    ├── Figure detail pages
    └── Responsive design
```

## 🚀 Features

- **Smart Search**: Search for any historical figure by name
- **Rich Biographical Data**: Birth/death dates, locations, occupations, nationalities
- **Historical Context**: Automatic categorization and period classification
- **Data Quality Indicators**: Validation warnings and data completeness metrics
- **Responsive Design**: Beautiful, mobile-friendly interface
- **API Endpoints**: RESTful API for programmatic access

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **API Integration**: requests library for Wikipedia REST API
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Data Processing**: Custom ETL pipeline with regex parsing
- **Styling**: Modern CSS with gradients and animations

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🔧 Installation & Setup

1. **Clone or download this project**
   ```bash
   cd api-practice
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎮 Usage

### Web Interface
1. Enter a historical figure's name in the search box
2. Click "Search" or press Enter
3. View detailed biographical information
4. Explore suggested popular figures

### API Endpoints
- `GET /api/search/<name>` - Get figure data as JSON
- `GET /api/suggestions/<query>` - Get search suggestions

## 📊 Data Sources

- **Wikipedia REST API**: Primary data source for biographical information
- **Rate Limited**: Respectful API usage with built-in delays
- **Error Handling**: Graceful handling of missing or incomplete data

## 🔍 Sample Searches

Try these historical figures:
- Leonardo da Vinci
- Cleopatra
- Albert Einstein
- Marie Curie
- Napoleon Bonaparte
- William Shakespeare
- Joan of Arc
- Galileo Galilei

## 📁 Project Structure

```
api-practice/
├── app.py                 # Main Flask application
├── wikipedia_client.py    # Wikipedia API interaction
├── data_transformer.py    # ETL transformation logic
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Search page
│   └── figure.html       # Figure detail page
├── static/
│   └── style.css         # CSS styling
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── venv/               # Virtual environment (created during setup)
```

## 🔧 Configuration

### Environment Variables
- `FLASK_DEBUG`: Set to 'True' for development mode (default: True)
- `PORT`: Port number for the Flask server (default: 5000)
- `SECRET_KEY`: Secret key for Flask sessions (auto-generated for development)

### Wikipedia API
- No authentication required
- Rate limiting: Built-in delays to respect Wikipedia's servers
- User-Agent: Set to 'HistoricalFiguresExplorer/1.0 (Educational Project)'

## 🧪 Data Engineering Concepts Demonstrated

### Extract Layer
- HTTP API integration with error handling
- Rate limiting and respectful API usage
- Multiple data source coordination (search + content + infobox)

### Transform Layer
- Text cleaning and normalization
- Date parsing with multiple format support
- Category extraction using keyword matching
- Data validation and quality assessment

### Load Layer
- Structured data presentation
- Web interface with responsive design
- API endpoints for programmatic access

## 🚀 Future Enhancements (Phase 2)

- **Database Integration**: SQLite/PostgreSQL for data persistence
- **Caching**: Redis for improved performance
- **Advanced Analytics**: Timeline visualization and relationship mapping
- **Data Export**: CSV/JSON download functionality
- **Batch Processing**: Bulk historical figure import

## 🤝 Contributing

This is an educational project, but suggestions and improvements are welcome!

## 📝 License

This project is for educational purposes. Wikipedia data is available under Creative Commons licenses.

## 🙏 Acknowledgments

- Wikipedia and Wikimedia Foundation for providing free access to biographical data
- Flask community for the excellent web framework
- Python community for amazing data processing libraries

---

**Happy Learning!** 🎓

Explore the fascinating lives of historical figures while mastering Python and data engineering concepts.
