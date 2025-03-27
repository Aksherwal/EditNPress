
# EditNpress - News Content Extraction and Analysis

EditNpress is a web application that allows users to extract and analyze news content from the Indian Express website. It provides a simple interface for users to input a news article URL, which is then processed, cleaned, and stored in a PostgreSQL database. The application also provides various metrics and visualizations related to the news content.

### Live Demo
[Click Here](https://editnpress.onrender.com/)
## Features

1. **URL Validation**: The application checks the validity of the input URL and ensures that it is from the Indian Express website.
2. **Text Cleaning**: The application uses Natural Language Processing (NLP) techniques to clean the extracted text, removing unnecessary elements such as HTML tags, advertisements, and formatting.
3. **Content Analysis**: The application provides various metrics about the news content, including word count, sentence count, stop words count, and the most frequent words.
4. **Part-of-Speech (POS) Tagging**: The application uses the Universal POS Tagging scheme to analyze the part-of-speech tags in the news content.
5. **Data Storage**: The application stores the processed news content in a PostgreSQL database, allowing for easy retrieval and analysis.
6. **Admin Dashboard**: The application provides an admin dashboard where authorized users can view the entire history of processed news content and clear the database if necessary.
7. **Authentication**: The application uses Google OAuth 2.0 for user authentication, allowing for secure access to the admin dashboard.

## Technologies Used

- **Backend**: Flask (Python web framework), PostgreSQL (database), Authlib (Google OAuth 2.0 integration)
- **Frontend**: HTML, CSS, JavaScript
- **NLP**: NLTK (Natural Language Toolkit)
- **Web Scraping**: BeautifulSoup, urllib

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/Aksherwal/EditNPress.git
```
2. Create a virtual environment and activate it:
```
python -m venv env
source env/bin/activate
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Set up the PostgreSQL database:
   - Install and configure PostgreSQL on your system.
   - Create a new database and user for the application.
   - Update the database connection details in the `main.py` file.
5. Set up the Google OAuth 2.0 credentials:
   - Create a new Google Cloud project and enable the Google OAuth 2.0 API.
   - Obtain the client ID and client secret and update them in the `main.py` file.
6. Run the application:
```
python main.py
```
7. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Visit the home page and enter the URL of the news article you want to analyze.
2. The application will process the content, store it in the database, and display the results.
3. To access the admin dashboard, click on the "Admin" link and log in using the pre-defined admin credentials.
4. In the admin dashboard, you can view the full history of processed news content and clear the database if necessary.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to create a new issue or submit a pull request. Contributions are always welcome!

## License

This project is licensed under the [MIT License](LICENSE).
