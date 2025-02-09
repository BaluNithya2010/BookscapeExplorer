import requests
from datetime import datetime
from Books_DB_Operations import insert_book_data

def scrap(query, apikey):
    """
    Sending the GET request with the query parameters.
    
    query:
    - Search query (e.g., "Python programming")
    
    apikey:
    - API key for authentication
    
    """

    # The URL to send the GET request to
    url = "https://www.googleapis.com/books/v1/volumes"
    # Dictionary of query parameters
    params = {
    "q" : query,
    "key" : apikey}
    response = requests.get(url, params)
    return response

def get_data(inputField):
    """Validate authors having more than one or not based on the type"""
    if isinstance(inputField, list):
        inputField = ", ".join(inputField)  # Join authors if it's a list
    elif isinstance(inputField, dict):
        inputField = ", ".join(inputField)  # Join authors if it's a dictionary
    elif isinstance(inputField, str):
        inputField = inputField  # If it's already a string, use it as is
    elif isinstance(inputField, bool):
        inputField = inputField  # If it's already a boolean, use it as is
    else:
        inputField = 'N/A'  # In case authors is None or missing

    return inputField

def get_industryIdentifier(industry_identifiers):
    """Loop through the industryIdentifiers list to find the ISBNs"""
    isbn_13 = isbn_10 = 'N\A'

    for identifier in industry_identifiers:
        if identifier.get('type') == 'ISBN_13':
            isbn_13 = identifier.get('identifier', 'N\A')  # Default to None if null
        elif identifier.get('type') == 'ISBN_10':
            isbn_10 = identifier.get('identifier', 'N\A')  # Default to None if null

    return "isbn_13:" + isbn_13 + ", " + "isbn_10:" + isbn_10

def get_year(published_date):
    """If publishedDate is not None, extract the year"""
    year = 'N/A'
    if published_date:
        try:
            # Parse the published date string to a datetime object
            date_object = datetime.fromisoformat(published_date)
            # Extract the year
            year = date_object.year            
        except ValueError:
            print("Invalid date format")    
    return year

def get_books(query, conn, total_results=200):
    """ get the books based on search key and load into databases"""
    url = 'https://www.googleapis.com/books/v1/volumes'
    apikey = 'AIzaSyDSumHoHJDCYnuWTYGYj-0sgFjVbqN19dY'

     # List to store all books
    all_books = []

    # StartIndex to paginate through results
    start_index = 0
    max_results_per_request = 40  # Max results per request (Google Books API allows up to 40)

    while len(all_books) < total_results:
        # Define parameters for the API request
        params = {
            "q": query,  # Search query (e.g., 'python programming')
            "key" : apikey,
            "startIndex": start_index,  # Index to start fetching from
            "maxResults": max_results_per_request,  # Number of results per request
        }
        
        # Send GET request to Google Books API
        response = requests.get(url, params=params)

        # Check for successful response
        if response.status_code == 200:
            books = response.json().get("items", [])
            
            success_rec_count = 0
            fail_rec_count = 0
            # Loop through books and add to the all_books list
            for book in books:
                book_id = book.get('id')
                search_key = query
                book_title = get_data(book['volumeInfo'].get('title'))
                book_subtitle = get_data(book['volumeInfo'].get('subtitle')) 
                book_authors = get_data(book['volumeInfo'].get('authors')) 
                book_publisher = get_data(book['volumeInfo'].get('publisher'))
                book_description = get_data(book['volumeInfo'].get('description')) 
                industryIdentifiers = get_industryIdentifier(book['volumeInfo'].get('industryIdentifiers',[]))
                text_readingModes = get_data(book['volumeInfo'].get('readingModes',{}).get('text'))
                image_readingModes = get_data(book['volumeInfo'].get('readingModes',{}).get('image'))
                pageCount = book['volumeInfo'].get('pageCount',0)
                categories = get_data(book['volumeInfo'].get('categories'))
                language = get_data(book['volumeInfo'].get('language'))
                imageLinks = get_data(book['volumeInfo'].get('imageLinks',{}).get('thumbnail'))
                ratingsCount = book['volumeInfo'].get('ratingsCount',0)
                averageRating = book['volumeInfo'].get('averageRating',0)
                country = get_data(book['saleInfo'].get('country'))
                saleability = book['saleInfo'].get('saleability','N/A')
                isEbook = get_data(book['saleInfo'].get('isEbook'))
                amount_listPrice = book['saleInfo'].get('listPrice',{}).get('amount',0)
                currencyCode_listPrice = get_data(book['saleInfo'].get('listPrice',{}).get('currencyCode'))
                amount_retailPrice = book['saleInfo'].get('retailPrice',{}).get('amount',0)
                currencyCode_retailPrice = get_data(book['saleInfo'].get('retailPrice',{}).get('currencyCode'))
                buyLink = get_data(book['saleInfo'].get('buyLink'))
                year = get_year(book['volumeInfo'].get('publishedDate','N/A'))

                all_books.append({
                'book_id':book_id,
                'search_key':search_key, 
                'book_title':book_title,
                'book_subtitle':book_subtitle,
                'book_authors':book_authors,
                'book_publisher':book_publisher,
                'book_description':book_description,
                'industryIdentifiers':industryIdentifiers,
                'text_readingModes':text_readingModes,
                'image_readingModes':image_readingModes,
                'pageCount':pageCount,
                'categories':categories,
                'language':language,
                'imageLinks':imageLinks,
                'ratingsCount':ratingsCount,
                'averageRating':averageRating,
                'country':country,
                'saleability':saleability,
                'isEbook':isEbook,
                'amount_listPrice':amount_listPrice,
                'currencyCode_listPrice':currencyCode_listPrice,
                'amount_retailPrice':amount_retailPrice,
                'currencyCode_retailPrice':currencyCode_retailPrice,
                'buyLink':buyLink,
                'year':year
                })

                # Insert the book data into database
                insert_book_data(conn, book_id, search_key, book_title, book_subtitle, book_authors, book_publisher, book_description, 
                            industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language,
                            imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, 
                            currencyCode_listPrice,amount_retailPrice, currencyCode_retailPrice, buyLink, year)
                    
            # If we've collected enough books, stop pagination
            if len(all_books) >= total_results:
                break
            
            # Increase the start index for the next batch of results
            start_index += max_results_per_request
        else:
            print("Failed to retrieve data")
            break
    return all_books
