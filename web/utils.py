import re

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
    genre = re.sub(r"[\'&\[\]]", "", genre.strip().lower())
    return genre_mapping.get(genre, genre)

def clean_cast_member(cast_member):
    cast_member = re.sub(r"[\'&\[\]]", "", cast_member.strip().lower())
    return cast_member

def standardize_genres(df):
    df['genres'] = df['genres'].dropna().apply(lambda x: ','.join([clean_genre(genre) for genre in x.split(',')]))
    return df

def standardize_cast(df):
    df['cast'] = df['cast'].dropna().apply(lambda x: ','.join([clean_cast_member(cast) for cast in x.split(',')]))
    return df

def extract_unique_genres(df):
    genres_list = df['genres'].dropna().apply(lambda x: [clean_genre(genre) for genre in x.split(',') if clean_genre(genre) not in excluded_genres]).tolist()
    flattened_genres = [genre for sublist in genres_list for genre in sublist]
    unique_genres = list(set(flattened_genres))
    return unique_genres

def extract_unique_cast(df):
    cast_list = df['cast'].dropna().apply(lambda x: [clean_cast_member(cast_member) for cast_member in x.split(',')]).tolist()
    flattened_cast = [cast_member for sublist in cast_list for cast_member in sublist]
    unique_cast = list(set(flattened_cast))
    return unique_cast

def extract_years(df):
    years = df['year'].dropna().unique().tolist()
    years = sorted([year for year in years], reverse=True)
    return years

# Define mood criteria mapping
mood_criteria = {
    "nature documentary": {
        "genres": ["documentary"],
        "description_keywords": ["nature", "wildlife", "environment"]
    },
    "old timer": {
        "year": "<1950"
    },
    "india": {
        "description_keywords": ["india", "indian"]
    },
    "musical": {
        "genres": ["musical"]
    },
    "romantic": {
        "genres": ["romantic"]
    },
    "exciting": {
        "genres": ["action", "thriller", "adventure"]
    },
    "melancholic": {
        "genres": ["drama", "melancholic"]
    }
}

def filter_by_mood(df, mood):
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
