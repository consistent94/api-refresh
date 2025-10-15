"""
Historical Figures Explorer - Flask Web Application

Main Flask application that provides a web interface for searching
and displaying biographical information about historical figures
extracted from Wikipedia.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from urllib.parse import quote

from wikipedia_client import WikipediaClient
from data_transformer import DataTransformer


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize components
wikipedia_client = WikipediaClient()
data_transformer = DataTransformer()


@app.route('/')
def index():
    """
    Home page with search form.
    
    Returns:
        Rendered template with search form
    """
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """
    Handle search form submission.
    
    Returns:
        Redirect to figure detail page or back to search with error
    """
    name = request.form.get('name', '').strip()
    
    if not name:
        flash('Please enter a name to search for.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get raw data from Wikipedia
        raw_data = wikipedia_client.get_figure_data(name)
        
        if not raw_data:
            flash(f'No information found for "{name}". Try a different spelling or search term.', 'error')
            return redirect(url_for('index'))
        
        # Transform the data
        transformed_data = data_transformer.transform_figure_data(raw_data)
        
        # Validate the data
        validated_data = data_transformer.validate_data(transformed_data)
        
        # Redirect to figure page
        figure_name = quote(transformed_data['name'])
        return redirect(url_for('figure', name=figure_name))
        
    except Exception as e:
        app.logger.error(f"Error searching for {name}: {str(e)}")
        flash('An error occurred while searching. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/figure/<name>')
def figure(name):
    """
    Display detailed information about a historical figure.
    
    Args:
        name (str): URL-encoded name of the historical figure
        
    Returns:
        Rendered template with figure details or 404
    """
    try:
        # Decode the name
        decoded_name = name.replace('_', ' ')
        
        # Get data from Wikipedia (in case user accessed URL directly)
        raw_data = wikipedia_client.get_figure_data(decoded_name)
        
        if not raw_data:
            flash(f'No information found for "{decoded_name}".', 'error')
            return redirect(url_for('index'))
        
        # Transform and validate the data
        transformed_data = data_transformer.transform_figure_data(raw_data)
        validated_data = data_transformer.validate_data(transformed_data)
        
        return render_template('figure.html', figure=validated_data)
        
    except Exception as e:
        app.logger.error(f"Error displaying figure {name}: {str(e)}")
        flash('An error occurred while loading the figure information.', 'error')
        return redirect(url_for('index'))


@app.route('/api/search/<name>')
def api_search(name):
    """
    API endpoint for searching historical figures.
    
    Args:
        name (str): Name to search for
        
    Returns:
        JSON response with figure data
    """
    try:
        raw_data = wikipedia_client.get_figure_data(name)
        
        if not raw_data:
            return jsonify({'error': 'No information found'}), 404
        
        transformed_data = data_transformer.transform_figure_data(raw_data)
        validated_data = data_transformer.validate_data(transformed_data)
        
        return jsonify(validated_data)
        
    except Exception as e:
        app.logger.error(f"API error for {name}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/suggestions/<query>')
def api_suggestions(query):
    """
    API endpoint for search suggestions.
    
    Args:
        query (str): Partial search query
        
    Returns:
        JSON response with search suggestions
    """
    try:
        if len(query) < 2:
            return jsonify({'suggestions': []})
        
        search_results = wikipedia_client.search_figure(query, limit=5)
        suggestions = [result['title'] for result in search_results]
        
        return jsonify({'suggestions': suggestions})
        
    except Exception as e:
        app.logger.error(f"Suggestions error for {query}: {str(e)}")
        return jsonify({'suggestions': []})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Development server configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    print("Historical Figures Explorer")
    print("=" * 40)
    print(f"Starting development server on http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )

