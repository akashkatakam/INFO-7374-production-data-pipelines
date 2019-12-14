from datetime import datetime
from sagemaker.tuner import ContinuousParameter

config = {}

config["job_level"] = {
    "region_name": "<region-name>",
    "run_hyperparameter_opt": "no"
}

config["ingest_data"] = {
    "fred_key": "d956c0978bfabcf773879232e72c9088",
    "s3_out_bucket": "<s3-bucket>",  # replace
    "s3_out_prefix": "raw/",
    "delimiter": "\t"
}

