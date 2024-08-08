from flask import Flask, request, jsonify, render_template
import pandas as pd
import re
from utils import standardize_genres, standardize_cast, extract_unique_genres, extract_unique_cast, extract_years, filter_by_mood

app = Flask(__name__)

# Load and standardize the CSV file into a DataFrame
df = pd.read_csv('..\\scraping\\movie_data.csv')
df = standardize_genres(df)
df = standardize_cast(df)

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

    This endpoint returns the unique genres, cast members, and years present in the movie data.

    Returns:
        json: A JSON object containing lists of unique genres, cast members, and years.
    """
    genres = extract_unique_genres(df)
    cast = extract_unique_cast(df)
    years = extract_years(df)
    return jsonify({"genres": genres, "cast": cast, "years": years})

@app.route('/movies', methods=['POST'])
def get_movies():
    """
    Get movies based on filters.

    This endpoint receives filter criteria via a POST request and returns movies that match the criteria.
    The filters can include genres, cast members, years, description keywords, title, and mood.

    Returns:
        json: A JSON object containing a list of movies that match the filter criteria.
    """
    filters = request.json
    print("Filters received:", filters)  # Debug: Check the received filters
    selected_genres = filters.get('genres', [])
    selected_cast = filters.get('cast', "").lower()
    selected_years = filters.get('years', [])
    description_keywords = filters.get('description', "").lower().split()
    title = filters.get('title', "").lower()
    mood = filters.get('mood', "").lower()
    page = filters.get('page', 1)
    items_per_page = filters.get('items_per_page', 10)
    filter_logic = filters.get('filter_logic', 'or').lower()

    filtered_df = df

    # If mood is selected, filter by mood criteria
    if mood:
        filtered_df = filter_by_mood(filtered_df, mood)
    else:
        conditions = []

        if selected_genres:
            if filter_logic == 'and':
                genre_condition = filtered_df['genres'].apply(lambda x: isinstance(x, str) and all(genre in x for genre in selected_genres))
            else:
                genre_condition = filtered_df['genres'].apply(lambda x: isinstance(x, str) and any(genre in x for genre in selected_genres))
            conditions.append(genre_condition)
            
        
        if selected_cast:
            cast_condition = filtered_df['cast'].str.contains(selected_cast, case=False, na=False)
            conditions.append(cast_condition)
            
        if selected_years:
            expanded_years = [int(year) for year in selected_years]
            year_condition = filtered_df['year'].isin(expanded_years)
            conditions.append(year_condition)

        if description_keywords:
            if filter_logic == 'and':
                description_condition = filtered_df['description'].apply(lambda x: isinstance(x, str) and all(keyword in x for keyword in description_keywords))
            else:
                description_condition = filtered_df['description'].apply(lambda x: isinstance(x, str) and any(keyword in x for keyword in description_keywords))
            conditions.append(description_condition)
            

        if title:
            title_condition = filtered_df['title'].str.contains(title, case=False, na=False)
            conditions.append(title_condition)

        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                if filter_logic == 'and':
                    combined_condition = combined_condition & condition
                else:
                    combined_condition = combined_condition | condition
            filtered_df = filtered_df[combined_condition]

    total_items = len(filtered_df)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_df = filtered_df.iloc[start_index:end_index]

    paginated_df = paginated_df.fillna('')

    print("Filtered movies:", paginated_df.to_dict(orient='records'))

    movies = paginated_df.to_dict(orient='records')
    return jsonify({
        "movies": movies,
        "total_items": total_items,
        "page": page,
        "items_per_page": items_per_page
    })

if __name__ == '__main__':
    app.run(debug=True)