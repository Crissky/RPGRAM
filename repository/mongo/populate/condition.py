from repository.mongo import ConditionModel
from rpgram import Condition

CONDITIONS = []

if __name__ == "__main__":
    conditions_model = ConditionModel()
    for condition_dict in CONDITIONS:
        condition = Condition(**condition_dict)
        print(condition)
        conditions_model.save(condition)
