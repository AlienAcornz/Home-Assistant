from .time_utils import *
from ...api_system.log_utils import add_log

def select_tool(actions, response_text):
    for action_name, params in actions.items():
        add_log(f"Searching for action {action_name} with the parameters: {params}", tag="tools")
        match action_name:
            case "set_timer":
                set_timer(int(params[0]))

            case "get_timer":
                if params and str(params[0]).strip().isdigit():
                    result = get_timer(int(params[0]))
                else:
                    result = get_timer()

                if result:
                    response_text = f"The timer has {result} seconds left"
                else:
                    response_text = "Could not find timer. This may be because the timer does not exist."

            case "delete_timer":
                if params and str(params[0]).strip().isdigit():
                    result = delete_timer(int(params[0]))
                else:
                    result = delete_timer()

                if not result:
                    response_text = "Could not find timer. This may be because the timer does not exist."

            case _:
                add_log(f"Action: {action_name} not found!", tag="tools")
                print(f"Action: {action_name} not found!")
                response_text = f"Action: {action_name} not found!"
    return response_text