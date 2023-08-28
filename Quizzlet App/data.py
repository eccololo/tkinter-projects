import requests


def get_questions():
    # Write your code here.
    parameters = {
        "amount": 10,
        "type": "boolean",
        "category": 18
    }
    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()
    questions_list = data["results"]
    return questions_list


question_data = get_questions()