import logging

import azure.functions as func
import json
from datetime import datetime
from pytz import timezone

def main(myblob: func.InputStream, documents: func.DocumentList, out: func.Out[func.Document]):
    try:
        tz = timezone('EST')
        today = datetime.now(tz).strftime('%Y-%m-%d')
        json_body = json.load(myblob)
        operations = json_body.get("Operations", [])
        if not documents:
            documents = func.DocumentList()
        for item in operations:
            has_item = False
            product_id = item['ProductID']
            product_name = item['Product']
            operation = item['Operation']
            received = 0 if operation != "Received" else int(item['Count'])
            shipped = 0 if operation != "Shipped" else int(item['Count'])
            returned = 0 if operation != "Returned" else int(item['Count'])
            for i in range(len(documents)):
                if documents[i].get("product_id") == product_id:
                    has_item = True
                    if documents[i].get("last_updated") != today:
                        documents[i]["last_updated"] = today
                        documents[i]["received"] = received
                        documents[i]["shipped"] = shipped
                        documents[i]["returned"] = returned
                    else:
                        documents[i]["received"] += received
                        documents[i]["shipped"] += shipped
                        documents[i]["returned"] += returned
                    documents[i]["total"] += received
                    documents[i]["total"] -= shipped
                    documents[i]["total"] += returned
                    break
            if not has_item:
                newDict = {
                    "product_id": product_id,
                    "product_name": product_name,
                    "received": received,
                    "shipped": shipped,
                    "returned": returned,
                    "total": received,
                    "last_updated": today,
                    "id": product_id
                }
                documents.append(func.Document.from_dict(newDict))
        out.set(documents)
    except Exception as e:
        logging.error(e)

