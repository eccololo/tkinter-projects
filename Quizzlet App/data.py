import requests
import settings


def get_questions():
    # Write your code here.
    parameters = {
        "amount": settings.API_DATA_AMOUNT,
        "type": settings.API_DATA_TYPE,
        "category": 18
    }
    response = requests.get(settings.API_URL, params=parameters)
    response.raise_for_status()
    data = response.json()
    questions_list = data["results"]
    return questions_list


question_data = get_questions()