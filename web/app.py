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
    return render_template('index.html')

@app.route('/categories', methods=['GET'])
def get_categories():
    genres = extract_unique_genres(df)
    cast = extract_unique_cast(df)
    years = extract_years(df)
    return jsonify({"genres": genres, "cast": cast, "years": years})

@app.route('/movies', methods=['POST'])
def get_movies():
    filters = request.json
    print("Filters received:", filters)  # Debug: Check the received filters
    selected_genres = filters.get('genres', [])
    selected_cast = filters.get('cast', "").lower()
    selected_years = filters.get('years', [])
    description_keywords = filters.get('description', "").lower().split()
    description_logic = filters.get('description_logic', 'or').lower()
    title = filters.get('title', "").lower()
    mood = filters.get('mood', "").lower()

    filtered_df = df

    # If mood is selected, filter by mood criteria
    if mood:
        filtered_df = filter_by_mood(filtered_df, mood)
    else:
        # Dynamically build filter conditions based on the provided parameters
        if selected_genres:
            genre_condition = filtered_df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))
            filtered_df = filtered_df[genre_condition]

        if selected_cast:
            filtered_df = filtered_df[filtered_df['cast'].str.contains(selected_cast, case=False, na=False)]

        if selected_years:
            expanded_years = []
            for year in selected_years:
                expanded_years.append(int(year))
            filtered_df = filtered_df[filtered_df['year'].isin(expanded_years)]

        if description_keywords:
            if description_logic == 'and':
                description_condition = filtered_df['description'].apply(lambda x: isinstance(x, str) and all(keyword in x for keyword in description_keywords))
            else:
                description_condition = filtered_df['description'].apply(lambda x: isinstance(x, str) and any(keyword in x for keyword in description_keywords))
            filtered_df = filtered_df[description_condition]

        if title:
            filtered_df = filtered_df[filtered_df['title'].str.contains(title, case=False, na=False)]

    # Ensure there are no NaN values in the output
    filtered_df = filtered_df.fillna('')

    print("Filtered movies:", filtered_df.to_dict(orient='records'))  # Debug: Check the filtered DataFrame

    movies = filtered_df.to_dict(orient='records')
    return jsonify(movies)

if __name__ == '__main__':
    app.run(debug=True)
