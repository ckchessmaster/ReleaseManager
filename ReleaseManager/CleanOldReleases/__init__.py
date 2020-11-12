import logging

import azure.functions as func

def main(blob: func.InputStream):
  logging.info(f"Python blob trigger function triggered by new release: {blob.name}")