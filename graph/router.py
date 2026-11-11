from graph.state import StudyAssistantState

def route_request (state : StudyAssistantState):
    #request from state
    request_type = state.get("request_type") 
    if request_type == "question":
        return "qa"

    elif request_type == "summary":
        return "summary"

    elif request_type == "mcq":
        return "mcq"

    elif request_type == "descriptive":
        return "descriptive"

    else:
        raise ValueError("Invalid request type")