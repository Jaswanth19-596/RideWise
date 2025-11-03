import mlflow
from mlflow import MlflowClient
from dotenv import load_dotenv

load_dotenv()


mlflow.set_tracking_uri("databricks")

# Set experiment in the tracking server
mlflow.set_experiment("/Users/madhajaswanth@gmail.com/RideWise")


client = MlflowClient()

result = client.copy_model_version(
    src_model_uri='models:/ridewise.development.xgboost@latest',
    dst_name = 'ridewise.production.xgboost'
)

client.set_registered_model_alias(
    name = 'ridewise.production.xgboost',
    alias='champion',
    version=result.version
)

