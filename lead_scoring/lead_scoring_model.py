# FileName: MultipleFiles/lead_scoring_model.py
# FileContents:
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

class LeadScoringModel:
    """
    A class to train and use a Classifier for random data  lead scoring.
    """
    def __init__(self, data_path):
     
        self.data_path = data_path
        self.model = RandomForestClassifier(random_state=42) # Added random_state for reproducibility
        self.is_trained = False
        self.features = None # To store the feature columns after dummy encoding

    def load_data(self):
        """
     
            tuple: A tuple containing features (X) and target (y) DataFrames.
        """
        try:
            data = pd.read_csv(self.data_path)
        except FileNotFoundError:
            print(f"Error: Dataset not found at {self.data_path}")
            return pd.DataFrame(), pd.Series()

        data.fillna(0, inplace=True) 

        # Define features and target
        X = data[['job_title', 'company_size', 'website_visits', 'email_opens']]
        y = data['converted']

      
        X = pd.get_dummies(X)
        self.features = X.columns 
        return X, y

    def train_model(self):
      
        X, y = self.load_data()
        if X.empty or y.empty:
            print("Cannot train model: .")
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("Training model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Model trained successfully.")

        # Evaluate the model
        predictions = self.model.predict(X_test)
        print("\n--- Model Evaluation ---")
        print("Confusion Matrix:\n", confusion_matrix(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))
        print("------------------------")

    def score_lead(self, lead):
        
        if not self.is_trained:
            raise Exception("Model is not trained yet. Please train the model first.")
        if self.features is None:
            raise Exception("Model features not initialized. Train the model first.")

        # Prepare the lead data for prediction
        lead_data = pd.DataFrame([lead])
        lead_data = pd.get_dummies(lead_data)

        lead_data = lead_data.reindex(columns=self.features, fill_value=0)

        score = self.model.predict(lead_data)
        return score[0]


