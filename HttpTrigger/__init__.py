import azure.functions as func
import json


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:

    docs = []

    for document in documents:
        docs.append({
            "product_id": document.get("product_id"),
            "product_name": document.get("product_name"),
            "received": document.get("received"),
            "shipped": document.get("shipped"),
            "returned": document.get("returned"),
            "total": document.get("total"),
            "last_updated": document.get("last_updated"),
        })
    return func.HttpResponse(json.dumps({
        "Products": docs
    }))