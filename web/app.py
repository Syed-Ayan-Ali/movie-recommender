from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from utils import standardize_genres, standardize_cast, extract_unique_genres, extract_unique_cast, extract_years, filter_content

app = Flask(__name__)

# Load and standardize the CSV file into a DataFrame
movies_df = pd.read_csv('..\\scraping\\movie_data.csv')
tv_series_df = pd.read_csv('..\\scraping\\tv_series_data.csv')

movies_df = standardize_genres(movies_df)
movies_df = standardize_cast(movies_df)

tv_series_df = standardize_genres(tv_series_df)
tv_series_df = standardize_cast(tv_series_df)

@app.route('/')
def home():
    """
    Render the home page.

    Returns:
        str: The rendered HTML of the home page.
    """
    return render_template('index.html')

@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Get unique categories for filtering.

    This endpoint returns the unique genres, cast members, and years present in the selected content type (movies, TV series, or both).
    """
    content_type = request.args.get('type', 'movies')  # Accept content type as a parameter ('movies', 'series', or 'both')
    
    if content_type == 'movies':
        df = movies_df
    elif content_type == 'series':  # Changed from 'tv_series' to 'series' to match the HTML and JavaScript
        df = tv_series_df
    else:
        df = pd.concat([movies_df, tv_series_df], ignore_index=True)  # Combine both datasets

    genres = extract_unique_genres(df)
    cast = extract_unique_cast(df)
    years = extract_years(df)
    
    return jsonify({"genres": genres, "cast": cast, "years": years})

@app.route('/content', methods=['POST'])
def get_content():
    filters = request.json
    content_type = filters.get('type', 'movies')  # Accept content type from filters ('movies', 'series', or 'both')

    if content_type == 'movies':
        filtered_df, total_items = filter_content(movies_df, filters)
    elif content_type == 'series':  # Changed from 'tv_series' to 'series' to match the HTML and JavaScript
        filtered_df, total_items = filter_content(tv_series_df, filters)
    else:
        combined_df = pd.concat([movies_df, tv_series_df], ignore_index=True)
        filtered_df, total_items = filter_content(combined_df, filters)

    page = filters.get('page', 1)
    items_per_page = filters.get('items_per_page', 10)

    content = filtered_df.to_dict(orient='records')
    return jsonify({
        "content": content,
        "total_items": total_items,
        "page": page,
        "items_per_page": items_per_page
    })
    
if __name__ == '__main__':
    app.run(debug=True)