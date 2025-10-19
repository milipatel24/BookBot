import pandas as pd

# Read dataset safely
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
books = pd.read_csv('data/books.csv', low_memory=False)

# Rename columns to standard names
books.rename(columns={
    'Book-Title': 'title',
    'Book-Author': 'authors'
}, inplace=True)

# Drop rows where title or authors are missing
books.dropna(subset=['title', 'authors'], inplace=True)

# Save cleaned data
books.to_csv('data/clean_books.csv', index=False)

print("✅ Data cleaned and saved as data/clean_books.csv")
