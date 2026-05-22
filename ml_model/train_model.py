import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv('../data/rows.csv', low_memory=False)

# Keep only the columns we need
df = df[['Consumer complaint narrative', 'Product']].copy()

# Drop rows where complaint text is missing
df.dropna(subset=['Consumer complaint narrative', 'Product'], inplace=True)

# Clean column name
df.rename(columns={'Consumer complaint narrative': 'complaint'}, inplace=True)

# Check what product categories exist
print("Categories found:")
print(df['Product'].value_counts())
print(f"\nTotal records: {len(df)}")

# Build pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000, stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    df['complaint'],
    df['Product'],
    test_size=0.2,
    random_state=42
)

# Train
print("\nTraining model...")
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print("\nModel Performance:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(pipeline, 'complaint_classifier.pkl')
print("\nModel saved as complaint_classifier.pkl")