import re
import json

# Load mood criteria from JSON file
with open('mood_criteria.json', 'r') as file:
    mood_criteria = json.load(file)


# Define a mapping of similar genres to their standardized form
genre_mapping = {
    'sci-fi': 'science fiction',
    'science fiction': 'science fiction',
    'scifi': 'science fiction',
    'rom-com': 'romantic comedy',
    'romantic comedy': 'romantic comedy'
    # Add more mappings as needed
}

# Define genres to exclude
excluded_genres = ['sci-fi fantasy', 'n/a', '']

def clean_genre(genre):
    """
    Clean and standardize a genre string.

    This function removes unwanted characters (apostrophes, ampersands, square brackets)
    and converts the genre string to lowercase. It also maps similar genres to a standard form.

    Parameters:
        genre (str): The genre string to be cleaned.

    Returns:
        str: The cleaned and standardized genre string.
    """
    genre = re.sub(r"[\'&\[\]]", "", genre.strip().lower())
    return genre_mapping.get(genre, genre)

def clean_cast_member(cast_member):
    """
    Clean and standardize a cast member string.

    This function removes unwanted characters (apostrophes, ampersands, square brackets)
    and converts the cast member string to lowercase.

    Parameters:
        cast_member (str): The cast member string to be cleaned.

    Returns:
        str: The cleaned and standardized cast member string.
    """
    cast_member = re.sub(r"[\'&\[\]]", "", cast_member.strip().lower())
    return cast_member

def standardize_genres(df):
    """
    Standardize the genres in a DataFrame.

    This function applies the clean_genre function to each genre in the 'genres' column
    of the DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.

    Returns:
        pandas.DataFrame: The DataFrame with standardized genres.
    """
    df['genres'] = df['genres'].dropna().apply(lambda x: ','.join([clean_genre(genre) for genre in x.split(',')]))
    return df

def standardize_cast(df):
    """
    Standardize the cast members in a DataFrame.

    This function applies the clean_cast_member function to each cast member in the 'cast' column
    of the DataFrame.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.

    Returns:
        pandas.DataFrame: The DataFrame with standardized cast members.
    """
    df['cast'] = df['cast'].dropna().apply(lambda x: ','.join([clean_cast_member(cast) for cast in x.split(',')]))
    return df

def extract_unique_genres(df):
    """
    Extract unique genres from a DataFrame.

    This function cleans and flattens the genres in the 'genres' column of the DataFrame,
    excluding specified genres, and returns a list of unique genres.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.

    Returns:
        list: A list of unique cleaned genres.
    """
    genres_list = df['genres'].dropna().apply(lambda x: [clean_genre(genre) for genre in x.split(',') if clean_genre(genre) not in excluded_genres]).tolist()
    flattened_genres = [genre for sublist in genres_list for genre in sublist]
    unique_genres = list(set(flattened_genres))
    return unique_genres

def extract_unique_cast(df):
    """
    Extract unique cast members from a DataFrame.

    This function cleans and flattens the cast members in the 'cast' column of the DataFrame,
    and returns a list of unique cast members.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.

    Returns:
        list: A list of unique cleaned cast members.
    """
    cast_list = df['cast'].dropna().apply(lambda x: [clean_cast_member(cast_member) for cast_member in x.split(',')]).tolist()
    flattened_cast = [cast_member for sublist in cast_list for cast_member in sublist]
    unique_cast = list(set(flattened_cast))
    return unique_cast

def extract_years(df):
    """
    Extract unique years from a DataFrame.

    This function extracts the unique years from the 'year' column of the DataFrame,
    sorts them in descending order, and returns them as a list.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.

    Returns:
        list: A list of unique years sorted in descending order.
    """
    years = df['year'].dropna().unique().tolist()
    years = sorted([year for year in years], reverse=True)
    return years


def filter_by_mood(df, mood):
    """
    Filter a DataFrame by mood criteria.

    This function filters the DataFrame based on predefined mood criteria, including genres,
    description keywords, and years.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing movie data.
        mood (str): The mood to filter by.

    Returns:
        pandas.DataFrame: The filtered DataFrame.
    """
    criteria = mood_criteria.get(mood, {})
    filtered_df = df
    
    if 'genres' in criteria:
        genre_condition = filtered_df['genres'].apply(lambda x: any(genre in x for genre in criteria['genres']))
        filtered_df = filtered_df[genre_condition]
    
    if 'description_keywords' in criteria:
        description_condition = filtered_df['description'].apply(lambda x: isinstance(x, str) and any(keyword in x for keyword in criteria['description_keywords']))
        filtered_df = filtered_df[description_condition]
    
    if 'year' in criteria:
        year_condition = criteria['year']
        if year_condition.startswith("<"):
            year_limit = int(year_condition[1:])
            filtered_df = filtered_df[filtered_df['year'] < year_limit]
    
    return filtered_df


def filter_content(df, filters):
    selected_genres = filters.get('genres', [])
    selected_cast = filters.get('cast', "").lower()
    selected_years = filters.get('years', [])
    description_keywords = filters.get('description', "").lower().split()
    filter_logic = filters.get('filter_logic', 'or').lower()
    title = filters.get('title', "").lower()
    mood = filters.get('mood', "").lower()
    page = filters.get('page', 1)
    items_per_page = filters.get('items_per_page', 10)

    # Apply mood-based filtering if applicable
    if mood:
        df = filter_by_mood(df, mood)
    else:
        conditions = []

        if selected_genres:
            if filter_logic == 'and':
                genre_condition = df['genres'].apply(lambda x: all(genre in x for genre in selected_genres))
            else:
                genre_condition = df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))
            conditions.append(genre_condition)

        if selected_cast:
            cast_condition = df['cast'].str.contains(selected_cast, case=False, na=False)
            conditions.append(cast_condition)

        if selected_years:
            expanded_years = [int(year) for year in selected_years]
            year_condition = df['year'].isin(expanded_years)
            conditions.append(year_condition)

        if description_keywords:
            if filter_logic == 'and':
                description_condition = df['description'].apply(lambda x: isinstance(x, str) and all(keyword in x for keyword in description_keywords))
            else:
                description_condition = df['description'].apply(lambda x: isinstance(x, str) and any(keyword in x for keyword in description_keywords))
            conditions.append(description_condition)

        if title:
            title_condition = df['title'].str.contains(title, case=False, na=False)
            conditions.append(title_condition)

        if conditions:
            combined_condition = conditions[0]
            for condition in conditions[1:]:
                if filter_logic == 'and':
                    combined_condition = combined_condition & condition
                else:
                    combined_condition = combined_condition | condition
            df = df[combined_condition]

    # Paginate results
    total_items = len(df)
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_df = df.iloc[start_index:end_index]

    return paginated_df.fillna(''), total_items
