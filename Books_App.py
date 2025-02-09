import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Books_CloudAPI import scrap, get_data, get_industryIdentifier, get_year, get_books
from Books_DB_Operations import create_connection, create_books_table, fetch_data, get_ebook_vs_physical, get_publisher_most_published, get_publisher_highest_averagerating, get_top5_expensivebook_retailprice, get_books_published_after2010, get_books_discounts_greater20percentage, get_averagepage_count_ebooks_vs_physical, get_top_3_authors, get_publisher_morethan_10books, get_average_pagecount_each_category, get_books_morethan_3_authors, get_books_ratingcount_greater_average, get_books_sameauthor_year, get_books_specific_keyword_title, get_year_high_average_bookprice, get_count_authors_published_3_years, get_authors_published_sameyears_different_publisher, get_average_amount_retailprice, get_books_averagerating,  get_publisher_highest_averagerating


# Function to plot pie chart
def plot_pie_chart(ebook_count, physical_book_count):
    labels = 'eBooks', 'Physical Books'
    sizes = [ebook_count, physical_book_count]
    colors = ['#ff9999','#66b3ff']
    
    fig1, ax1 = plt.subplots()
    #ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

def plot_top_expensive_books(y_data, x_data, xlabel, title):
      
    fig, ax = plt.subplots()
    ax.barh(y_data, x_data, color='lightcoral')
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    st.pyplot(fig)

def plot_bar_graph(categories, counts, xlabel, ylabel, title):
    
    # Create bar graph
    fig, ax = plt.subplots()
    ax.bar(categories, counts, color=['blue', 'green'])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Display the graph in Streamlit
    st.pyplot(fig)

def plot_pie(data, title):
    fig = px.pie(data, names='book_count', title=title)
    st.plotly_chart(fig)

def main():

    # Define the menu items
    menu_items = ['Search and Upload Books', 'View Books', 'Query']

    # Create a sidebar menu
    selected_menu = st.sidebar.radio("Select a menu option", menu_items)

    # Create a connection to the database
    conn = create_connection()
    
    if conn:
        # Create books table if it doesn't exist
        create_books_table(conn)
        st.title("Bookscape Explorer")       
        # Display content in the main area based on the selected menu
        if selected_menu == 'Search and Upload Books':
            query = st.text_input("Enter book name:")              

            # Search books using API and load the books in the database
            books = get_books(query, conn, total_results = 200)
            
            if books:
                st.write(f"Retrieved {len(books)} books:")
                df = pd.DataFrame(books)
                st.write(df)
                st.write(f"{len(books)} Book details has been uploaded to database.")
            else:
                print("No books found.")
        elif selected_menu == 'View Books':
            if st.button('Get Books from DB'):
                # Execute a SELECT query to fetch data from the table
                query = "select * from books" 
                df = fetch_data(conn, query)                
                st.write(f"{len(df)} Book details has been retrieved from database.")
                # Display the DataFrame
                st.dataframe(df, width=1000)
        elif selected_menu == 'Query':
            # Define the list of questions
            guvi_questions = [
                "1.Check Availability of eBooks vs Physical Books",
                "2.Find the Publisher with the Most Books Published",
                "3.Identify the Publisher with the Highest Average Rating",
                "4.Get the Top 5 Most Expensive Books by Retail Price",
                "5.Find Books Published After 2010 with at Least 500 Pages",
                "6.List Books with Discounts Greater than 20%",
                "7.Find the Average Page Count for eBooks vs Physical Books",
                "8.Find the Top 3 Authors with the Most Books",      
                "9.List Publishers with More than 10 Books",
                "10.Find the Average Page Count for Each Category",
                "11.Retrieve Books with More than 3 Authors",
                "12.Books with Ratings Count Greater Than the Average",
                "13.Books with the Same Author Published in the Same Year",
                "14.Books with a Specific Keyword in the Title",
                "15.Year with the Highest Average Book Price",
                "16.Count Authors Who Published 3 Consecutive Years",
                "17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year.",
                "18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries.",      
                "19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers.",
                "20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published."
            ]

            guvi_selected_question = st.selectbox("Select guvi provided question", guvi_questions)

            # Build the query based on the questions selected from dropdown list
            if guvi_selected_question == "1.Check Availability of eBooks vs Physical Books":
                query = get_ebook_vs_physical()            
            elif guvi_selected_question == "2.Find the Publisher with the Most Books Published":
                query = get_publisher_most_published()
            elif guvi_selected_question == "3.Identify the Publisher with the Highest Average Rating":
                query = get_publisher_highest_averagerating()
            elif guvi_selected_question == "4.Get the Top 5 Most Expensive Books by Retail Price":
                query = get_top5_expensivebook_retailprice()
            elif guvi_selected_question == "5.Find Books Published After 2010 with at Least 500 Pages":
                query = get_books_published_after2010()
            elif guvi_selected_question == "6.List Books with Discounts Greater than 20%":
                query = get_books_discounts_greater20percentage()
            elif guvi_selected_question == "7.Find the Average Page Count for eBooks vs Physical Books":
                query = get_averagepage_count_ebooks_vs_physical()
            elif guvi_selected_question == "8.Find the Top 3 Authors with the Most Books":
                query = get_top_3_authors()
            elif guvi_selected_question == "9.List Publishers with More than 10 Books":
                query = get_publisher_morethan_10books()
            elif guvi_selected_question == "10.Find the Average Page Count for Each Category":
                query = get_average_pagecount_each_category()
            elif guvi_selected_question == "11.Retrieve Books with More than 3 Authors":
                query = get_books_morethan_3_authors()
            elif guvi_selected_question == "12.Books with Ratings Count Greater Than the Average":
                query = get_books_ratingcount_greater_average()
            elif guvi_selected_question == "13.Books with the Same Author Published in the Same Year":
                query = get_books_sameauthor_year()
            elif guvi_selected_question == "14.Books with a Specific Keyword in the Title":
                query = get_books_specific_keyword_title()
            elif guvi_selected_question == "15.Year with the Highest Average Book Price":
                query = get_year_high_average_bookprice()
            elif guvi_selected_question == "16.Count Authors Who Published 3 Consecutive Years":
                query = get_count_authors_published_3_years()
            elif guvi_selected_question == "17.Write a SQL query to find authors who have published books in the same year but under different publishers. Return the authors, year, and the COUNT of books they published in that year.":
                query = get_authors_published_sameyears_different_publisher()
            elif guvi_selected_question == "18.Create a query to find the average amount_retailPrice of eBooks and physical books. Return a single result set with columns for avg_ebook_price and avg_physical_price. Ensure to handle cases where either category may have no entries.":
                query = get_average_amount_retailprice()
            elif guvi_selected_question == "19.Write a SQL query to identify books that have an averageRating that is more than two standard deviations away from the average rating of all books. Return the title, averageRating, and ratingsCount for these outliers.":
                query = get_books_averagerating()
            elif guvi_selected_question == "20.Create a SQL query that determines which publisher has the highest average rating among its books, but only for publishers that have published more than 10 books. Return the publisher, average_rating, and the number of books published.":
                query = get_publisher_highest_averagerating()

            # Fetch the data and display it
            if st.button('Get Results'):
                if(len(str(guvi_selected_question)) > 5):                
                    df = fetch_data(conn, query)
                    st.write(f"Results for: {guvi_selected_question} - {len(df)} Records")
                    # Display the results in grid
                    st.dataframe(df, width=1000)

                    # Display graphs for the below questions
                    if guvi_selected_question == "1.Check Availability of eBooks vs Physical Books":
                        # Mapping isEbook values to categories
                        df['Book Type'] = df['isEbook'].map({'True': 'eBooks', 'False': 'Physical Books'})
                        # Display the graph in Streamlit
                        plot_bar_graph(df['Book Type'],df['book_count'],'Book Type','Book Count', 'Book Count of eBooks vs Physical Books')
                    elif guvi_selected_question == "4.Get the Top 5 Most Expensive Books by Retail Price":
                        plot_top_expensive_books(df['book_title'], df['amount_retailPrice'],'Retail Price ($)',f'Top {len(df)} Most Expensive Books by Retail Price')
                    elif guvi_selected_question == "7.Find the Average Page Count for eBooks vs Physical Books":
                        df['Book Type'] = df['isEbook'].map({'True': 'eBooks', 'False': 'Physical Books'})
                        # Display the graph in Streamlit
                        plot_bar_graph(df['Book Type'],df['avg_page_count'],'Book Type','Average Page Count', 'Average Page Count of eBooks vs Physical Books')
                    elif guvi_selected_question == "8.Find the Top 3 Authors with the Most Books":
                        plot_top_expensive_books(df['book_authors'], df['books_count'],'Number of Books',f'Top {len(df)} Authors with the Most Books')
        #close the connection
        conn.close()

if __name__ == "__main__":
    main()
