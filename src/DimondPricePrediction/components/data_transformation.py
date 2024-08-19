
import os
import sys
import numpy as np
import pandas as pd
from src.DimondPricePrediction.logger import logging
from src.DimondPricePrediction.exception import customexception
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from src.DimondPricePrediction.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transormation_config=DataTransformationConfig()

    def get_data_transormation(self):
        
        try:
            logging.info("data Transformation initiated")

            categroical_cols=['cut','color','clarity']
            numrical_cols=['carat','depth','table','x','y','z']

            cut_categories=["Fair","Good","Very Good","Premium","Ideal"]
            color_categories=['D','E','F','G','H','I','J']
            clarity_categories=['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info("Pipeline Initiated")

            num_pipline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ])

            cat_pipline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('ordinaencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories]))
                ])

            preprocessor=ColumnTransformer([
            ('num_pipline',num_pipline,numrical_cols),
            ('cat_pipline',cat_pipline,categroical_cols)
            ])

            return preprocessor

        except Exception as e:
            logging.info("exception occured in the initiate_datatransformation")

            raise  customexception(e,sys)
        
    
    def initialize_data_transformation(self,train_path,test_path):
        
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test data complete")
            logging.info(f"Train Dataframe head : \n{train_df.head().to_string()}")
            logging.info(f"Test Dataframe head : \n{test_df.head().to_string()}")

            preprocessing_obj=self.get_data_transormation()

            target_column_name='price'
            drop_columns=[target_column_name,'id']

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df =test_df[target_column_name]

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transormation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("preprocessing pickle fle saved")

            return (
                train_arr,
                test_arr
            )

        except Exception as e:
            logging.info("Exception occured in the initiate_datatransformation")

            raise  customexception(e,sys)
        