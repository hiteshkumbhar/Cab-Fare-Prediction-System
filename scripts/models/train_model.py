import argparse
import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import mean_squared_error, make_scorer

def load_data(data_dir):
    # data load method form s3
    df = pd.read_csv(os.path.join(data_dir, "filtered.csv"))
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def main():
    parser = argparse.ArgumentParser()
    
    # 
    parser.add_argument("fareprice/model", type=str, default="/opt/ml/input/data")
    parser.add_argument("model", type=str, default="/opt/ml/model")
    
    args = parser.parse_args()
    
    #load data
    X, y = load_data(args.data_dir)
    
    # Define pipeline
    pipeline = Pipeline([
        ('model', GradientBoostingRegressor(random_state=42))
    ])
    
    # k fold cross val 
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        pipeline, X, y, cv=kfold, 
        scoring={
            'r2': 'r2',
            'rmse': make_scorer(lambda y_true, y_pred: np.sqrt(mean_squared_error(y_true, y_pred))),
            'mae': 'neg_mean_absolute_error'
        }, 
        return_train_score=True
    )
    
    # eval metrics
    print("Cross-Validation Results:")
    print(f"Average R-squared (CV): {np.mean(cv_results['test_r2'])}")
    print(f"Average RMSE (CV): {np.mean(cv_results['test_rmse'])}")
    print(f"Average MAE (CV): {-np.mean(cv_results['test_mae'])}")

    # Train final model
    pipeline.fit(X, y)

    # save to do further pred 
    model_path = os.path.join(args.model_dir, "model.joblib")
    from joblib import dump
    dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()

