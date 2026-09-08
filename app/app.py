import streamlit as st
import sys
import os
import ast
import html

# ==================================================
# PROJECT PATH
# ==================================================

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, project_root)


# ==================================================
# IMPORT RECOMMENDER
# ==================================================

from src.clustering import MovieClusterer
from src.recommender import MovieRecommender


# ==================================================
# STREAMLIT PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Movie Finder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: #ffffff;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- Hide Streamlit chrome ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ---------- Typography ---------- */

    h1, h2, h3 {
        color: #111827 !important;
    }

    p {
        color: #4b5563;
    }

    /* ---------- Header ---------- */

    .movie-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 24px;
        margin-bottom: 35px;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        background: #f8fafc;
        backdrop-filter: blur(10px);
    }

    .brand {
        font-size: 1.45rem;
        font-weight: 800;
        color: #111827;
    }

    .brand span {
        color: #38bdf8;
    }

    .status {
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        color: #86efac;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ---------- Hero ---------- */

    .hero {
        text-align: center;
        padding: 50px 20px 45px;
        margin-bottom: 35px;
        border-radius: 24px;
        background:
            radial-gradient(
                circle at top,
                rgba(56,189,248,0.16),
                transparent 55%
            ),
            linear-gradient(
                135deg,
                rgba(30,41,59,0.95),
                rgba(15,23,42,0.95)
            );
        border: 1px solid #e5e7eb;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 12px;
        color: #111827;
    }

    .hero-subtitle {
        max-width: 700px;
        margin: auto;
        font-size: 1.05rem;
        color: #4b5563;
    }

    /* ---------- Section ---------- */

    .section-title {
        font-size: 1.55rem;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 6px;
        color: #111827;
    }

    .section-description {
        color: #4b5563;
        margin-bottom: 20px;
    }

    /* ---------- Movie Cards ---------- */

    .movie-card {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        overflow: hidden;
        height: 100%;
        transition: transform 0.2s ease;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        border-color: rgba(56,189,248,0.35);
    }

    .movie-info {
        padding: 14px;
    }

    .movie-title {
        font-size: 1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .movie-meta {
        color: #4b5563;
        font-size: 0.82rem;
    }

    .similarity-badge {
        display: inline-block;
        margin-top: 10px;
        padding: 5px 9px;
        border-radius: 8px;
        background: rgba(56,189,248,0.10);
        color: #7dd3fc;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .movie-overview {
        margin-top: 12px;
        color: #4b5563;
        font-size: 0.82rem;
        line-height: 1.5;
    }

    /* ---------- Metrics ---------- */

    div[data-testid="stMetric"] {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        padding: 18px;
        border-radius: 14px;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 1rem;
        font-weight: 700;
    }

    /* ---------- Selectbox ---------- */

    div[data-baseweb="select"] > div {
        background: #ffffff;
        border-radius: 12px;
        border-color: #d1d5db;
    }

    /* ---------- Info boxes ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* ---------- Divider ---------- */

    hr {
        border-color: #e5e7eb;
        margin: 35px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.html(
    """
    <div class="movie-header">
        <div class="brand">
            🎬 Movie<span>Finder</span>
        </div>

        <div class="status">
            🟢 AI READY
        </div>
    </div>
    """
)


# ==================================================
# HELPER FUNCTION:
# SHORTEN MOVIE OVERVIEW
# ==================================================

def shorten_text(
    text,
    max_length=180
):
    """
    Shorten a movie overview so that
    the UI remains compact and readable.
    """

    if not text:
        return "No overview available."

    text = str(text)

    if len(text) <= max_length:
        return text

    return (
        text[:max_length]
        .rsplit(" ", 1)[0]
        + "..."
    )


# ==================================================
# HELPER FUNCTION:
# EXTRACT GENRES
# ==================================================

def extract_genres(genres_text):
    """
    Convert the genres column from its
    string representation into a list of
    genre names.
    """

    if not genres_text:
        return []

    try:

        genres = ast.literal_eval(
            genres_text
        )

        return [
            genre["name"]
            for genre in genres
            if isinstance(genre, dict)
            and "name" in genre
        ]

    except (
        ValueError,
        SyntaxError,
        TypeError
    ):

        return []


# ==================================================
# LOAD RECOMMENDER
# ==================================================

@st.cache_resource
def load_recommender():
    """
    Load the recommendation model only once.

    Streamlit normally reruns the Python script
    whenever the user interacts with the UI.

    cache_resource prevents the recommender from
    being recreated every time.
    """

    return MovieRecommender()

@st.cache_resource
def load_clusterer():

    return MovieClusterer()


# ==================================================
# INITIALIZE RECOMMENDER
# ==================================================

try:

    recommender = load_recommender()
    clusterer = load_clusterer()

except Exception as error:

    st.error(
        "Unable to load the movie recommender."
    )

    st.error(
        f"Error: {error}"
    )

    st.stop()


# ==================================================
# TMDB STATUS
# ==================================================

if hasattr(recommender, "tmdb_available"):

    if not recommender.tmdb_available:

        st.info(
            "ℹ️ Movie recommendations are available, "
            "but movie posters are currently unavailable."
        )


# ==================================================
# MOVIE OPTIONS
# ==================================================

movie_options = (
    recommender.movies[
        ["id", "title"]
    ]
    .dropna(subset=["id", "title"])
    .to_dict("records")
)


# ==================================================
# MOVIE SELECTOR
# ==================================================

st.markdown(
    '<div class="section-title">🎯 Choose a Movie</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Select a movie and let the recommendation engine find similar titles.'
    '</div>',
    unsafe_allow_html=True
)

selected_movie = st.selectbox(
    "Movie",
    movie_options,
    index=None,
    placeholder="Search for a movie...",

    # What the user sees in the dropdown
    format_func=lambda movie: (
        f'{movie["title"]} '
        f'(ID: {movie["id"]})'
    )
)

recommend_clicked = st.button(
    "✨ Get Recommendations",
    width="stretch",
    type="primary"
)

if selected_movie is None:
    if recommend_clicked:
        st.warning(
            "Please select a movie first."
        )

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:50px 20px;
            border:1px dashed rgba(255,255,255,0.12);
            border-radius:18px;
            margin-top:25px;
        ">

            <div style="font-size:3rem;">
                🍿
            </div>

            <h3>
                Ready to discover something?
            </h3>

            <p>
                Choose a movie above and we'll find
                similar movies for you.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ==================================================
# SELECTED MOVIE INFORMATION
# ==================================================

selected_movie_id = int(
    selected_movie["id"]
)

selected_movie_title = (
    selected_movie["title"]
)

# ==================================================
# RECOMMEND BUTTON
# ==================================================

if recommend_clicked:

    with st.spinner(
        "🎬 Finding movies you'll love..."
    ):

        try:

            recommendations = (
                recommender.recommend(
                    selected_movie_id,
                    number_of_recommendations=5
                )
            )

        except Exception as error:

            st.error(
                "We couldn't generate recommendations right now. "
                "Please try another movie."
            )

            st.stop()


    if not recommendations:

        st.warning(
            "No sufficiently similar movies were found."
        )

    else:

        st.markdown(
            '<div class="section-title">'
            '🎯 Recommended For You'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Movies selected based on content similarity.'
            '</div>',
            unsafe_allow_html=True
        )

        cols = st.columns(5)

        for i, movie in enumerate(recommendations[:5]):

            with cols[i]:

                poster_url = movie.get(
                    "poster_url"
                )

                if poster_url:
                    st.image(
                        poster_url,
                        width="stretch"
                    )
                else:
                    st.html(
                        """
                        <div style="
                            height:300px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#1f2937;
                            border-radius:12px;
                            color:#64748b;
                            text-align:center;
                        ">
                            🎬<br>No poster available
                        </div>
                        """
                    )

                safe_title = html.escape(
                    str(movie.get("title", "Unknown Movie"))
                )

                similarity = movie.get(
                    "score",
                    0
                )

                safe_overview = html.escape(
                    shorten_text(
                        movie.get(
                            "overview",
                            ""
                        ),
                        max_length=140
                    )
                )

                st.html(
                    f"""
                    <div class="movie-info">

                        <div class="movie-title">
                            {safe_title}
                        </div>

                        <div class="similarity-badge">
                            {similarity:.0%} similarity
                        </div>

                        <div class="movie-overview">
                            {safe_overview}
                        </div>

                    </div>
                    """
                )

        st.markdown(
            """
            <div class="section-title">
                🧠 How Recommendations Work
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "The system converts movie information into TF-IDF vectors "
            "and uses cosine similarity to identify movies with similar "
            "content. The similarity score indicates how close the movie "
            "representations are - it is not a probability."
        )

        st.caption(
            "Similarity scores represent relative content similarity "
            "between movie representations and should not be interpreted "
            "as probabilities."
        )


st.divider()

st.markdown(
    """
    <div class="section-title">
        🔬 Explore Movie Clusters
    </div>

    <div class="section-description">
        See how K-Means automatically groups movies based
        on their feature similarity.
    </div>
    """,
    unsafe_allow_html=True
)

# Cluster selector
cluster_ids = sorted(
    clusterer.movies["cluster"].unique()
)

selected_cluster = st.selectbox(
    "Select a cluster to explore",
    cluster_ids
)

# Cluster data
cluster_movies = clusterer.get_cluster_movies(
    selected_cluster
)

cluster_size = len(cluster_movies)

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Cluster",
        selected_cluster
    )

with col2:
    st.metric(
        "Movies",
        cluster_size
    )

with col3:
    st.metric(
        "Algorithm",
        "K-Means"
    )

# Top genres
top_genres = clusterer.get_top_genres(
    selected_cluster
)

st.subheader(
    "🔎 Characteristics of This Cluster"
)

st.caption(
    "These are the most common genres observed among "
    "movies in this cluster. They were not provided to "
    "K-Means as target labels."
)

for genre, count in top_genres:
    st.write(
        f"**{genre}** - {count} movies"
    )

# Movies
st.subheader(
    f"Movies in Cluster {selected_cluster}"
)

st.dataframe(
    cluster_movies[
        ["title", "overview"]
    ].head(20),
    width="stretch",
    hide_index=True,
    column_config={
        "title": st.column_config.TextColumn(
            "Movie",
            width="medium"
        ),
        "overview": st.column_config.TextColumn(
            "Overview",
            width="large"
        )
    }
)

# Distribution
st.subheader("Cluster Distribution")

cluster_counts = (
    clusterer.movies["cluster"]
    .value_counts()
    .sort_index()
)

st.bar_chart(cluster_counts)

st.info(
    "K-Means automatically groups movies based on "
    "similarities in their feature representations. "
    "Cluster numbers are identifiers, not predefined "
    "genre labels."
)

st.divider()

st.html(
    """
    <div style="
        text-align:center;
        padding:25px 0;
        color:#64748b;
        font-size:0.85rem;
    ">

        🎬 <strong>MovieFinder</strong>

        <br>

        Built with Python • Streamlit • Scikit-learn • TMDB

        <br><br>

        Content-based recommendation + unsupervised clustering

    </div>
    """
)

