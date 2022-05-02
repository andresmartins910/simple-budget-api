from app.exceptions.expenses_exceptions import ValuesTypeError


def verify_value_types(data):
    if type(data['name']) != str:
        raise ValuesTypeError({"data": "name must be of type string"})
    if type(data['amount']) != int:
        raise ValuesTypeError({"data": "amount must be of type integer"})
    if type(data['category_id']) != int:
        raise ValuesTypeError({"data": "category_id must be of type integer"})
    if type(data['budget_id']) != int:
        raise ValuesTypeError({"data": "budget_id must be of type integer"})
    try:
        if type(data['description']) != str:
            raise ValuesTypeError({"data": "description must be of type string"})
    except:
        pass

def verify_update_type(data):
    try:
        if type(data['name']) != str:
            raise ValuesTypeError({"data": "name must be of type string"})
    except:
        pass
    try:
        if type(data['description']) != str:
            raise ValuesTypeError({"data": "name must be of type string"})
    except:
        pass
