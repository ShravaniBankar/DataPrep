import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from scipy import stats
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Configure logging
logging.basicConfig(filename='processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df, num_impute_strategy='mean', remove_outliers=False, outlier_method='IQR'):
    logging.info("Cleaning data: Removing duplicates and handling missing values")
    df.drop_duplicates(inplace=True)

    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    num_imputer = SimpleImputer(strategy=num_impute_strategy)
    df[numeric_features] = num_imputer.fit_transform(df[numeric_features])

    if remove_outliers:
        if outlier_method == 'IQR':
            logging.info("Removing outliers using IQR method")
            Q1 = df[numeric_features].quantile(0.25)
            Q3 = df[numeric_features].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[numeric_features] < (Q1 - 1.5 * IQR)) | (df[numeric_features] > (Q3 + 1.5 * IQR))).any(axis=1)]
        elif outlier_method == 'Z-score':
            logging.info("Removing outliers using Z-score method")
            df = df[(stats.zscore(df[numeric_features]) < 3).all(axis=1)]
        elif outlier_method == 'percentile':
            logging.info("Removing outliers using percentile method")
            lower_bound = df[numeric_features].quantile(0.01)
            upper_bound = df[numeric_features].quantile(0.99)
            df = df[~((df[numeric_features] < lower_bound) | (df[numeric_features] > upper_bound)).any(axis=1)]
    
    categorical_features = df.select_dtypes(include=['object', 'category']).columns
    cat_imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_features] = cat_imputer.fit_transform(df[categorical_features])

    return df

def transform_data(df, encoding_method='onehot', num_impute_strategy='mean', remove_outliers=False, outlier_method='IQR'):
    logging.info("Cleaning and transforming data")
    df.drop_duplicates(inplace=True)

    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    num_imputer = SimpleImputer(strategy=num_impute_strategy)
    df[numeric_features] = num_imputer.fit_transform(df[numeric_features])

    if remove_outliers:
        if outlier_method == 'IQR':
            logging.info("Removing outliers using IQR method")
            Q1 = df[numeric_features].quantile(0.25)
            Q3 = df[numeric_features].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[numeric_features] < (Q1 - 1.5 * IQR)) | (df[numeric_features] > (Q3 + 1.5 * IQR))).any(axis=1)]
        elif outlier_method == 'Z-score':
            logging.info("Removing outliers using Z-score method")
            df = df[(stats.zscore(df[numeric_features]) < 3).all(axis=1)]
        elif outlier_method == 'percentile':
            logging.info("Removing outliers using percentile method")
            lower_bound = df[numeric_features].quantile(0.01)
            upper_bound = df[numeric_features].quantile(0.99)
            df = df[~((df[numeric_features] < lower_bound) | (df[numeric_features] > upper_bound)).any(axis=1)]
    
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    categorical_features = df.select_dtypes(include=['object', 'category']).columns
    if encoding_method == 'onehot':
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_data = encoder.fit_transform(df[categorical_features])
        encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())
        df = df.drop(columns=categorical_features)
        df = pd.concat([df, encoded_df], axis=1)

    return df

def visualize_data(df, title, plot_type='histogram'):
    plt.figure(figsize=(10, 5))
    if plot_type == 'histogram':
        df.hist(figsize=(10, 5))
    elif plot_type == 'boxplot':
        df.plot(kind='box', figsize=(10, 5))
    plt.suptitle(title)
    plt.show()
