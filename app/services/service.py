from settings import table


def new_page(body: dict):
    table.put_item(
        Item={
            "page_id": int(body["page_id"]),
            "posts": 0,
            "followers": 0,
            "follow_requests": 0,
            "likes": 0,
        }
    )


def add_like(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET likes = likes + :count",
        ExpressionAttributeValues={":count": 1},
    )


def del_like(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET likes = likes - :count",
        ExpressionAttributeValues={":count": 1},
    )


def add_requests(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET follow_requests = follow_requests + :count",
        ExpressionAttributeValues={":count": body["count"]},
    )


def del_requests(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET follow_requests = follow_requests - :count",
        ExpressionAttributeValues={":count": body["count"]},
    )


def add_followers(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET followers = followers + :count",
        ExpressionAttributeValues={":count": body["count"]},
    )


def del_followers(body: dict):
    table.update_item(
        Key={"page_id": int(body["page_id"])},
        UpdateExpression=f"SET followers = followers - :count",
        ExpressionAttributeValues={":count": body["count"]},
    )


def get_statistics_for_page(page_id: int):
    response = table.get_item(
        Key={
            "page_id": page_id,
        }
    )
    return response["Item"]


methods_dict = {
    "add_followers": add_followers,
    "del_followers": del_followers,
    "add_follow_requests": add_requests,
    "del_follow_requests": del_requests,
    "del_like": del_like,
    "add_like": add_like,
    "create": new_page,
}
