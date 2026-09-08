# 🎬 Movie Recommender System

A machine learning based movie recommendation system that recommends movies similar to a user's selected movie using TF-IDF, Cosine Similarity, and K-Means Clustering.

The project combines supervised-style application development concepts with unsupervised machine learning techniques, focusing primarily on content-based recommendation and unsupervised clustering.

The system uses the TMDB 5000 Movie Dataset and integrates the TMDB API to retrieve movie posters and additional movie information.

---

## 📌 Project Overview

Finding a good movie to watch can be difficult when thousands of movies are available.

This project solves that problem by allowing a user to:

- Select a movie
- Get movies similar to the selected movie
- View movie posters
- Explore movie clusters discovered using K-Means
- Understand which movies belong to the same automatically discovered group
- Explore the characteristics of different movie clusters

The project demonstrates how machine learning can be used to build a real-world recommendation system.

---

## 🎯 Objectives

The main objectives of this project are:

1. Build a real-world content-based movie recommendation system
2. Understand and implement TF-IDF
3. Understand and implement Cosine Similarity
4. Apply K-Means clustering
5. Demonstrate unsupervised learning
6. Build an interactive web application using Streamlit
7. Integrate the TMDB API
8. Handle real-world API failures and missing data
9. Implement API caching to improve performance
10. Provide a clean and user-friendly interface
11. Visualize movie clusters
12. Understand how machine learning models are integrated into production applications

---

## 🧠 Machine Learning Concepts

### TF-IDF
Converts movie text (overview, genres, keywords, cast) into numerical vectors.


### Cosine Similarity
Measures how similar two movie vectors are. Score ranges from 0 (different) to 1 (very similar).



### K-Means Clustering
An unsupervised algorithm that groups similar movies together without predefined labels (e.g. Action, Romance).

---

## 🔍 Recommendation Pipeline

This project uses a content-based recommendation system.

The recommendation pipeline is:

```

                    Movie Dataset
                         │
                         ▼
                Data Preprocessing
                         │
                         ▼
              Feature Combination
                         │
                         ▼
                       TF-IDF
                         │
                         ▼
                Movie Feature Matrix
                         │
                         ▼
                Cosine Similarity
                         │
                         ▼
              Similarity Scores
                         │
                         ▼
             Top Similar Movies
                         │
                         ▼
                  TMDB Posters
                         │
                         ▼
                    Streamlit UI

```
The system recommends movies based on the content/features of the selected movie.

---

## 🧩 K-Means Pipeline

The clustering pipeline is:

```
Movie Dataset
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
TF-IDF Representation
      │
      ▼
K-Means Algorithm
      │
      ▼
Movie Clusters
      │
      ▼
Cluster Analysis
      │
      ▼
Streamlit Cluster Explorer

```
The application allows users to explore the clusters created by K-Means.


---

## ✨ Features

- **Movie Recommendation** — select a movie, get similar ones
- **Movie Posters** — fetched via TMDB API
- **Similarity Scores** — shows how close a match is (not a "chance you'll like it" score)
- **Cluster Explorer** — view clusters, their size, and common genres
- **Cluster Distribution** — visualize movie counts per cluster

---

## 🌐 TMDB API Integration

The project integrates the TMDB API to retrieve movie-related information such as:

- Movie posters
- Movie images
- Additional movie information

The machine learning model does not depend on the TMDB API to calculate recommendations.

The recommendation model works using the local dataset.

The API is primarily used to enrich the user interface with movie information and images.

---

## 🗂️ Dataset

The project uses the:

TMDB 5000 Movie Dataset

The dataset contains information about thousands of movies.

Two main CSV files are used:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

---

## 📁 Project Structure

```
Movie Recommender/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   ├── similarity.pkl
│   ├── tfidf.pkl
│   └── kmeans.pkl
├── notebooks/
├── src/
│   ├── recommender.py
│   └── clustering.py
├── app/
│   └── app.py
├── .gitignore
├── README.md
└── requirements.txt
```
---

## 🏗️ Application Architecture

The application follows a simple layered architecture:

```


                  Streamlit Frontend
                         │
                         ▼
                  Application Layer
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Recommender                Clusterer
             │                       │
             ▼                       ▼
      TF-IDF / Similarity          K-Means
             │                       │
             └───────────┬───────────┘
                         ▼
                  Processed Dataset
                         │
                         ▼
                  Movie Information
                         │
                         ▼
                     TMDB API

```
---

## 🛠️ Technologies Used

- **Language:** Python
- **ML:** Scikit-learn (TF-IDF, Cosine Similarity, K-Means, PCA)
- **Data:** Pandas, NumPy
- **Visualization:** Matplotlib, Streamlit charts
- **Web App:** Streamlit
- **API:** TMDB API

---

## ⚙️ Installation

1. Clone the repository

```
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project:

```
cd Movie-Recommender
```

2. Create a Virtual Environment

Windows:

```
python -m venv .venv
```

Activate it:

```
.venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Add the Dataset

Download the TMDB 5000 Movie Dataset and place the files inside:

data/raw/

The directory should contain:

```
data/raw/
├── tmdb_5000_movies.csv
└── tmdb_5000_credits.csv
```

---

## 🔑 TMDB API Configuration

The application uses the TMDB API for movie posters and additional movie information.

Create a TMDB account and generate an API key.

Then configure the API key using an environment variable or Streamlit secrets.

For local development, create:

`.env`

or use the project's configured secrets mechanism.

Example:

```
TMDB_API_KEY=your_api_key_here
```

Do not commit your API key to GitHub.

Make sure .env is included in .gitignore.

---

## ▶️ Running the Project

```
streamlit run app/app.py
```

Then open `http://localhost:8501` in your browser.

---

### 🔬 Data Preprocessing & Feature Engineering
Genres, keywords, and overview are cleaned, combined, and converted into TF-IDF vectors.

### 🤖 Why Unsupervised Learning?
K-Means discovers movie groupings from the data itself — no predefined genre labels are used.

### 🧱 Model Persistence
Models (`tfidf.pkl`, `similarity.pkl`, `kmeans.pkl`) are trained once and reloaded on startup, avoiding retraining.

---

## 📜 License
Intended for educational and portfolio purposes. Review dataset/API licensing before commercial use.

---

## 👨‍💻 Author

Sanika Gajarishi

---

## ⭐ Support

If you found this useful, consider giving the repo a ⭐ on GitHub.