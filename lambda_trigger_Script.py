import boto3
import json
import os
import pandas as pd
import numpy as np
import io
import psycopg2
from psycopg2.extras import execute_values
import warnings


pd.options.mode.chained_assignment = None

def lambda_handler(event, context):
    try:
        # Environment Variables (Set in Lambda)
        BUCKET_NAME = "careerspace-survey"
        AWS_REGION = "ca-central-1"


    # Initialize AWS S3 Client
        s3 = boto3.client("s3", region_name=AWS_REGION)
        print("S3 Client Initialized")
        # Fetch all CSV files from S3 bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        print("S3 Client Initialized II")
        files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".csv")]
        print(files)
        final_df = pd.DataFrame()
        for file_key in files:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
            df = pd.read_csv(io.BytesIO(obj["Body"].read()))
            
            survey_number = file_key.replace(".csv", "").replace(" ", "_")
            
            for i in range(2, len(df)):
                temp = pd.DataFrame(df.iloc[[0, i]]).reset_index()
                temp = temp.T.reset_index()
                temp.columns = ['Question_id', 'Question', 'Response']
                temp['Survey_number'] = survey_number + '_' + str(i)
                temp_up = temp[3:]
                temp_up['Start_Date'] = temp.loc[1].values[2]
                temp_up['End_Date'] = temp.loc[2].values[2]
                final_df = pd.concat([final_df, temp_up], ignore_index=True)

        print("Shape of DataFrame after processing:",final_df.shape)
        print("Columns in DataFrame:", final_df.columns.tolist())
        #final_df['Senti_emot']=np.nan 
        DB_NAME = "postgres"
        DB_USER = "group_B04"
        DB_PASSWORD = "Surveyanalysis_b04"
        DB_HOST = "careerspace.ctsoqg24oatl.ca-central-1.rds.amazonaws.com"
        DB_PORT = "5432"

        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            cur = conn.cursor()
            print("Connected to the database")
        except:
            print("Unable to connect to the database")
        
        #columns = ["Question_id", "Question", "Response", "Survey_number", "Start_Date", "End_Date"]
        columns= final_df.columns.tolist()
        values = final_df[columns].values.tolist()
        table_name= "Survey_data_table_2025"
        try :
            print("Creating table")
            cur.execute(f"DROP TABLE IF EXISTS public.{table_name}")
            cur.execute( f"""
            CREATE TABLE IF NOT EXISTS public.{table_name} (
                "Question_id" TEXT,
                "Question" TEXT,
                "Response" TEXT,
                "Survey_Number" TEXT,
                "Start_Date" TEXT,
                "End_Date" TEXT
            );
            """
            )
            print("Table created")
        except:
            print("Table Creation Failed or Table already exists")
        try:
            print("Truncating table to remove old values")
            cur.execute(f"TRUNCATE TABLE public.{table_name}")
            print("Inserting values")
            insert_query = f"""
            INSERT INTO public.{table_name} ("Question_id", "Question", "Response", "Survey_Number", "Start_Date", "End_Date")
            VALUES %s
            """
            print("Table Updated")

            execute_values(cur, insert_query, values)
            conn.commit()
            
            print("Values Inserted")
        except Exception as e :
            print("Insert Into Table Failed", str(e))
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Lambda Executed"
            })
        }

    except Exception as e:
        print(f"S3 Access Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
