import mysql.connector
import pandas as pd
from mysql.connector import Error


def create_connection():
    """Create a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='guviproj',
            user='root',
            password='T1e2s3t4',
            port=3306
        )
        if conn.is_connected():
            print(f"Successfully connected to the database")
        
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

def create_books_table(conn):
    """Create the books table if it doesn't already exist."""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id varchar(20) PRIMARY KEY,
                search_key varchar(45) NOT NULL,
                book_title varchar(255) DEFAULT NULL,
                book_subtitle text,
                book_authors text,
                book_publisher text,
                book_description text,
                industryIdentifiers text,
                text_readingModes boolean DEFAULT NULL,
                image_readingModes boolean DEFAULT NULL,
                pageCount int,
                categories text,
                language varchar(10),
                imageLinks text,
                ratingsCount int,
                averageRating decimal,
                country varchar(10),
                saleability varchar(100),
                isEbook boolean,
                amount_listPrice decimal,
                currencyCode_listPrice varchar(10),
                amount_retailPrice decimal,
                currencyCode_retailPrice varchar(10),
                buyLink text,
                year text  
            );
        ''')
        conn.commit()
        print("Books table created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()

def fetch_data(conn, query):
    """ Function to execute the query and return the dataframe"""
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Convert the result into a DataFrame
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    
    cursor.close()
    return df    

# SQL queries for each question
def get_ebook_vs_physical():
    query = """
    SELECT  
    CASE 
        WHEN isEbook = 0 THEN 'False'
        WHEN isEbook = 1 THEN 'True'
    END AS isEbook,
    COUNT(*) AS book_count
    FROM books
    GROUP BY isEbook;
    """
    return query

def get_publisher_most_published():
    query = """
    SELECT 
    book_publisher, 
    COUNT(*) AS books_count
    FROM books
    WHERE book_publisher != 'N/A'
    GROUP BY book_publisher
    ORDER BY books_count DESC
    LIMIT 1;
    """
    return query

def get_publisher_highest_averagerating():
    query = """
    SELECT 
    book_publisher, 
    AVG(averageRating) AS avg_rating
    FROM books
    GROUP BY book_publisher
    ORDER BY avg_rating DESC
    LIMIT 1;
    """
    return query

def get_top5_expensivebook_retailprice():
    query = """
    SELECT 
    book_title, 
    amount_retailPrice
    FROM books
    ORDER BY amount_retailPrice DESC
    LIMIT 5;
    """
    return query

def get_books_published_after2010():
    query = """
    SELECT 
    book_title, 
    year, 
    pageCount
    FROM books
    WHERE year != 'N/A' and year > '2010' AND pageCount >= 500
    order by pagecount;
    """
    return query

def get_books_discounts_greater20percentage():
    query = """
    SELECT 
    book_title, 
    amount_listPrice, 
    amount_retailPrice, 
    ROUND((amount_listPrice - amount_retailPrice) / amount_listPrice * 100, 2) AS discount_percentage
    FROM books
    WHERE (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 > 20
    order by discount_percentage;
    """
    return query

def get_averagepage_count_ebooks_vs_physical():
    query = """
    SELECT 
    CASE 
        WHEN isEbook = 0 THEN 'False'
        WHEN isEbook = 1 THEN 'True'
    END AS isEbook,
    ROUND(AVG(pageCount),2) AS avg_page_count
    FROM books
    GROUP BY isEbook;    
    """
    return query

def get_top_3_authors():
    query = """
    SELECT 
    book_authors, 
    COUNT(*) AS books_count
    FROM books
    WHERE book_authors != 'N/A'
    GROUP BY book_authors
    ORDER BY books_count DESC
    LIMIT 3;

    """
    return query

def get_publisher_morethan_10books():
    query = """
    SELECT 
    book_publisher, 
    COUNT(*) AS books_count
    FROM books
    WHERE book_publisher != 'N/A'
    GROUP BY book_publisher
    HAVING books_count > 10
    ORDER BY books_count;
    """
    return query

def get_average_pagecount_each_category():
    query = """
    SELECT 
    categories, 
    ROUND(AVG(pageCount), 2) AS avg_page_count    
    FROM books
    WHERE categories != 'N/A'
    GROUP BY categories
    ORDER BY avg_page_count DESC;
    """
    return query

def get_books_morethan_3_authors():
    query = """
    SELECT 
    book_title, 
    book_authors
    FROM books
    WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;

    """
    return query

def get_books_ratingcount_greater_average():
    query = """
    SELECT 
    book_title, 
    ratingsCount
    FROM books
    WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books)
    ORDER BY ratingsCount;
    """
    return query

def get_books_sameauthor_year():
    query = """
    SELECT 
    book_authors, 
    year, 
    COUNT(*) AS book_count
    FROM books
    WHERE book_authors != 'N/A' and year != 'N/A'
    GROUP BY book_authors, year
    HAVING book_count > 1
    ORDER BY book_count desc;
    """
    return query

def get_books_specific_keyword_title():
    query = """
    SELECT 
    search_key, 
    book_title
    FROM books
    WHERE book_title LIKE CONCAT('%', search_key, '%');
    """
    return query

def get_year_high_average_bookprice():
    query = """
    SELECT 
    year, 
    ROUND(AVG(amount_retailPrice),2) AS avg_book_price
    FROM books
    WHERE YEAR != 'N/A'
    GROUP BY year
    ORDER BY avg_book_price DESC;
    
    """
    return query

def get_count_authors_published_3_years():
    query = """
    SELECT b1.book_authors,
       b1.year AS year1,
       b2.year AS year2,
       b3.year AS year3
    FROM books b1
    JOIN books b2 ON b1.book_authors = b2.book_authors
    JOIN books b3 ON b1.book_authors = b3.book_authors
    WHERE CAST(b1.year AS SIGNED) = CAST(b2.year AS SIGNED) - 1
    AND CAST(b2.year AS SIGNED) = CAST(b3.year AS SIGNED) - 1
    AND b1.book_authors != 'N/A'
    GROUP BY b1.book_authors, year1, year2, year3
    ORDER BY b1.book_authors, year1;
    """
    return query

def get_authors_published_sameyears_different_publisher():
    query = """
    SELECT 
    book_authors, 
    year, 
    COUNT(DISTINCT book_publisher) AS publisher_count
    FROM books
    WHERE book_authors != 'N/A' AND year != 'N/A' 
    GROUP BY book_authors, year
    HAVING publisher_count > 1;
    """
    return query

def get_average_amount_retailprice():
    query = """
    SELECT 
    ROUND(AVG(CASE WHEN isEbook = 1 THEN amount_retailPrice ELSE NULL END),2) AS avg_ebook_price, 
    ROUND(AVG(CASE WHEN isEbook = 0 THEN amount_retailPrice ELSE NULL END),2) AS avg_physical_price
    FROM books;
    """
    return query

def get_books_averagerating():
    query = """
    WITH RatingStats AS (
    SELECT 
        AVG(averageRating) AS avg_rating,
        STDDEV(averageRating) AS stddev_rating
    FROM books
    )
    SELECT 
        book_title, 
        averageRating, 
        ratingsCount
    FROM books, RatingStats
    WHERE 
        averageRating > (avg_rating + 2 * stddev_rating) 
        OR averageRating < (avg_rating - 2 * stddev_rating);
    """
    return query

def get_publisher_highest_averagerating():
    query = """
    SELECT 
    book_publisher, 
    AVG(averageRating) AS avg_rating, 
    COUNT(*) AS books_count
    FROM books
    WHERE book_publisher != 'N/A'
    GROUP BY book_publisher
    HAVING books_count > 10
    ORDER BY avg_rating DESC;
    """
    return query

def insert_book_data(conn,book_id, search_key, book_title, book_subtitle, book_authors, book_publisher, book_description, 
                                industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language,
                                imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, 
                                currencyCode_listPrice,amount_retailPrice, currencyCode_retailPrice, buyLink, year):
    """ Insert book data into books table"""
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (book_id, search_key, book_title, book_subtitle, book_authors, book_publisher, book_description, 
                    industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language,
                    imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, 
                    currencyCode_listPrice,amount_retailPrice, currencyCode_retailPrice, buyLink, year)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (book_id, search_key, book_title, book_subtitle, book_authors, book_publisher, book_description, 
                    industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language,
                    imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, 
                    currencyCode_listPrice,amount_retailPrice, currencyCode_retailPrice, buyLink, year))
        
        conn.commit()
        cursor.close()        
    except Error as e:
        conn.rollback()
    

