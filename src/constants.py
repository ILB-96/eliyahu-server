import os


URL = os.getenv("SHOPIFY_URL")
API_VERSION = os.getenv("SHOPIFY_API_VERSION")
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
ORIGIN = os.getenv("TRUSTED_ORIGIN")
HOST = os.getenv("TRUSTED_HOST")
API_URL = f"{URL}/admin/api/{API_VERSION}/graphql.json"
