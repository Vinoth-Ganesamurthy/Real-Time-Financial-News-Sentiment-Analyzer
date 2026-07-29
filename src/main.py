from data.news_loader import load_dataset
from data.data_validator import validate_dataset
from preprocessing.text_preprocessor import preprocess_dataset
from data.duplicate_handler import (
    inspect_duplicates,
    remove_duplicates,
)
from data.data_saver import save_dataset
from visualization.eda import plot_sentiment_distribution
from visualization.text_analysis import analyse_headline_lengths
from visualization.word_frequency import analyse_word_frequency
from models.predictor import predict_sentiment
from features.feature_extractor import (
    extract_bow_features,
    extract_tfidf_features,
)

from models.logistic_regression import train_logistic_regression
from models.naive_bayes import train_naive_bayes
from models.evaluator import evaluate_model
from models.svm import train_svm
from models.model_saver import save_model

def main() -> None:
    # ========================================
    # Load Dataset
    # ========================================
    df = load_dataset("data/raw/all-data.csv")

    # ========================================
    # Validate Dataset
    # ========================================
    validate_dataset(df)

    # ========================================
    # Preprocess Dataset
    # ========================================
    processed_df = preprocess_dataset(df)

    # ========================================
    # Inspect Duplicates
    # ========================================
    inspect_duplicates(processed_df)

    # ========================================
    # Remove Duplicates
    # ========================================
    cleaned_df = remove_duplicates(processed_df)

    # ========================================
    # Save Cleaned Dataset
    # ========================================
    save_dataset(
        cleaned_df,
        "data/processed/financial_news_cleaned.csv",
    )

    # ========================================
    # Preview Dataset
    # ========================================
    print("\nFirst 5 cleaned headlines:\n")
    print(cleaned_df.head())

    # ========================================
    # Exploratory Data Analysis
    # ========================================
    plot_sentiment_distribution(cleaned_df)
    analyse_headline_lengths(cleaned_df)
    analyse_word_frequency(cleaned_df)

    # ========================================
    # Feature Extraction
    # ========================================
    X_bow, bow_vectorizer = extract_bow_features(cleaned_df)

    X_tfidf, tfidf_vectorizer = extract_tfidf_features(cleaned_df)

    # ========================================
    # Logistic Regression
    # ========================================
    model, encoder, X_test, y_test = train_logistic_regression(
        X_tfidf,
        cleaned_df,
    )

    lr_results = evaluate_model(
        model,
        X_test,
        y_test,
        "Logistic Regression",
    )

    # ========================================
    # Naive Bayes
    # ========================================
    nb_model, nb_encoder, nb_X_test, nb_y_test = train_naive_bayes(
        X_tfidf,
        cleaned_df,
    )

    nb_results = evaluate_model(
        nb_model,
        nb_X_test,
        nb_y_test,
        "Naive Bayes",
    )

    # ========================================
    # Linear SVM
    # ========================================

    svm_model, svm_encoder, svm_X_test, svm_y_test = train_svm(
    X_tfidf,
    cleaned_df,
    )

    svm_results = evaluate_model(
    svm_model,
    svm_X_test,
    svm_y_test,
    "Linear SVM",
    )

    # ========================================
    # Model Comparison
    # ========================================
    print("\n" + "=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)

    print(f"{'Model':25}{'Accuracy':>12}{'Macro F1':>12}")
    print("-" * 50)

    for result in [lr_results, nb_results, svm_results]:        
        print(
            f"{result['Model']:25}"
            f"{result['Accuracy']:>12.4f}"
            f"{result['Macro F1']:>12.4f}"
        )

    # ========================================
    # Save Best Model
    # ========================================
    save_model(
        svm_model,
        tfidf_vectorizer,
        svm_encoder,
    )

    # ========================================
    # Sample Predictions
    # ========================================
    print("\n" + "=" * 40)
    print("SAMPLE PREDICTIONS")
    print("=" * 40)

    headlines = [
        "Apple reports record quarterly profits.",
        "Company announces layoffs of 500 employees.",
        "Board schedules annual shareholder meeting.",
    ]

    for headline in headlines:
        sentiment = predict_sentiment(headline)

        print(f"\nHeadline   : {headline}")
        print(f"Prediction : {sentiment}")


if __name__ == "__main__":
    main()
