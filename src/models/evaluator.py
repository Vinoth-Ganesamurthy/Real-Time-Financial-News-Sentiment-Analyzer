"""
Module for evaluating machine learning models.
"""

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluate a trained model.

    Returns:
        Dictionary containing evaluation metrics.
    """

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")

    print("\n" + "=" * 40)
    print(f"{model_name.upper()} EVALUATION")
    print("=" * 40)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Macro F1 : {macro_f1:.4f}")

    print("\nClassification Report")
    print("-" * 40)
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix")
    print("-" * 40)
    print(confusion_matrix(y_test, y_pred))

    return {
        "Model": model_name,
        "Accuracy": accuracy,
        "Macro F1": macro_f1,
    }