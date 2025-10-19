import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

class BookRecommender:
    def __init__(self, data_path='data/clean_books.csv'):
        warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)
        self.books = pd.read_csv('data/clean_books.csv', low_memory=False)
        self.books.fillna('', inplace=True)

        # ✅ If dataset has no 'genres', create a default one
        if 'genres' not in self.books.columns:
            self.books['genres'] = 'Unknown'

        # Combine columns for text features
        self.books['combined'] = (
            self.books['title'].astype(str) + ' ' +
            self.books['authors'].astype(str) + ' ' +
            self.books['genres'].astype(str)
        )

        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.matrix = self.vectorizer.fit_transform(self.books['combined'])
        self.similarity = None

    def recommend(self, user_books, genre, top_n=10):
        indices = []
        for book in user_books:
            idx = self.books[self.books['title'].str.contains(book, case=False, na=False)].index
            indices.extend(idx)
        if not indices:
            return ["No similar books found. Try different input."]

        from sklearn.metrics.pairwise import cosine_similarity

        # Compute similarity only for selected books
        sim_scores = sum(cosine_similarity(self.matrix[i], self.matrix)[0] for i in indices)

        self.books['score'] = sim_scores

        # ✅ If no real genres, just ignore filtering
        if 'genres' in self.books.columns and self.books['genres'].nunique() > 1:
            filtered = self.books[self.books['genres'].str.contains(genre, case=False, na=False)]
        else:
            filtered = self.books

        recommended = filtered.sort_values(by='score', ascending=False)
        return recommended[['title', 'authors']].head(top_n).values.tolist()
