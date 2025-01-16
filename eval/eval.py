import json

def get_default_match_result():
    return {
        "correct_tool_call": 0,
        "tool_name_match": 0,
        "wrong_tool_call_number": 0,
        "tool_parameter_required_key_match": 0,
        "tool_parameter_hallucination": 0,
        "correct_param_and_value": 0,
        "num_predicted_param": 0,
        "value_type_error": 0,
    }

def match(expected_tool_calls, infer_result, use_strict_string_match=True):
    match_result = get_default_match_result()
    
    if not expected_tool_calls:
        match_result["answer"] = "Negative"
        match_result["prediction"] = "TRUE_NEGATIVE" if not infer_result else "FALSE_POSITIVE"
        return match_result
    
    if len(expected_tool_calls) == 1:
        match_result["answer"] = "Single Positive"
        if not infer_result:
            match_result["prediction"] = "FALSE_NEGATIVE"
            return match_result
        if len(infer_result) == 1:
            match_result["prediction"] = "TRUE_POSITIVE"
        else:
            match_result["prediction"] = "Reference answer has a single tool call, Prediction has multiple tool calls"
            return match_result
    else:
        print('Parallel function call not supported now.')
        return match_result
    
    if match_result["prediction"] == "TRUE_POSITIVE":
        if expected_tool_calls[0]['name'] != infer_result[0]['name']:
            match_result["tool_name_match"] = False
            return match_result

        match_result["tool_name_match"] = True
        for para_name, para_value in expected_tool_calls[0]['args'].items():
            match_result["wrong_tool_call_number"] += 1
            if para_name not in infer_result[0]['args']:
                match_result["tool_parameter_required_key_match"] += 1
                continue
            args_dict = infer_result[0]['args']
            if args_dict[para_name] != para_value:
                match_result["tool_parameter_hallucination"] += 1
                continue
            match_result["correct_param_and_value"] += 1

        for para_name in infer_result[0]['args']:
            match_result["num_predicted_param"] += 1
            if para_name not in expected_tool_calls[0]['args']:
                match_result["value_type_error"] += 1
                continue
    
    return match_result

def get_summary(eval_results):
    total_examples = len(eval_results)
    summary = {
        "total_examples": total_examples,
        "func_name_accuracy": sum([r["tool_name_match"] for r in eval_results]) / total_examples,
    }
    return summary
