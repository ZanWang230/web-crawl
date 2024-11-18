# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 11:46:44 2024

@author: ASUS
"""
def get_tomatos(movie_name, release_year):
    # Import necessary libraries
    import requests as rq  # Requests library for making HTTP requests
    from bs4 import BeautifulSoup as bs  # BeautifulSoup for parsing HTML content
    import re  # Regular expressions for text manipulation and cleaning

    # Construct the Rotten Tomatoes search URL using the movie name
    url = f'https://www.rottentomatoes.com/search?search={movie_name}'

    # Create a session for making requests to the web
    sess = rq.Session()

    # Send a GET request to Rotten Tomatoes with a custom User-Agent to mimic a real browser
    r = sess.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})

    # Parse the response content (HTML) using BeautifulSoup
    soup = bs(r.text, 'html.parser')

    # Select all the movie details from the page using CSS selectors
    movies_detail = soup.select('search-page-media-row')

    # Iterate over each movie found in the search results
    for movie_detail in movies_detail:
        # Extract the tomato meter score, release year, and title for the movie
        score = movie_detail.get('tomatometerscore')
        year = movie_detail.get('releaseyear')
        title = movie_detail.select_one('a>img').get('alt')  # Get movie title from the image's alt attribute
        
        # Print the movie title for debugging purposes
        print(title)

        try:
            # If the release year is earlier than the search year and the titles match
            if int(year) < int(release_year) and str.lower(re.sub(r'[^a-zA-Z]', '', title)) == str.lower(re.sub(r'[^a-zA-Z]', '', movie_name)):
                return f'{score}%'  # Return the tomato meter score with percentage
            elif year == release_year:
                return f'{score}%'  # Return the score if the year matches
        except ValueError:
            # If the release year is not a valid integer (in case of missing or incorrect data)
            # Compare the cleaned-up titles (lowercased and non-alphabetical characters removed)
            if str.lower(re.sub(r'[^a-zA-Z]', '', title)) == str.lower(re.sub(r'[^a-zA-Z]', '', movie_name)):
                return f'{score}%'  # Return the score if titles match
            elif year == release_year:
                return f'{score}%'  # Return the score if the year matches

        # If the movie title doesn't exactly match, check how many characters match
        matched = 0

        # Compare each character in the movie title with the search query (case-insensitive)
        for n, i in enumerate(title):
            try:
                # If the characters match, increment the matched count
                if str.lower(i) == str.lower(movie_name[n]):
                    matched += 1
            except IndexError:
                break  # Exit the loop if the index exceeds the length of the search query

        # If the matched characters are at least 87% of the length of the search query, return the score
        if matched >= len(movie_name) * 0.87:
            return f'{score}%'  # Return the score with percentage

    # If no movie matched the criteria, return a default message
    return 'there is no tomatometer yet'

# Example call to the function with a movie name and release year
print(get_tomatos('NAUSICAA OF THE VALLEY OF THE WIND', '2024'))