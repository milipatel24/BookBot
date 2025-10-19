import streamlit as st
from recommender import BookRecommender

st.set_page_config(page_title="AI Book Recommendation System", layout="wide")
st.title("📚 BookBot")

st.write("Get personalized book suggestions based on what you’ve read and your favorite genre!")

# Initialize recommender
recommender = BookRecommender()

# User inputs
user_books = st.text_input("Enter some books you've already read (comma separated):")
genre = st.selectbox("Select your preferred genre:", 
                     ["Romantic", "Funny", "Suspense", "Thriller", "Horror",
                      "Biography", "Spiritual", "Philosophical"])

if st.button("Get Recommendations"):
    if user_books and genre:
        book_list = [b.strip() for b in user_books.split(',')]
        recommendations = recommender.recommend(book_list, genre)
        
        st.subheader("✨ Recommended Books:")
        for rec in recommendations:
            if isinstance(rec, list):
                title, author = rec
                st.markdown(f"**📖 {title}** — *{author}*")
            else:
                st.markdown(f"- {rec}")
    else:
        st.warning("Please enter books and select a genre.")
