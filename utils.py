import json
from typing import List, Dict, Any, Optional, Union

def dict_to_json(dict_list: List[Dict[str, Any]], filename: str) -> Optional[str]:
    try: 
        json_str = json.dumps(dict_list, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        return None

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_str)
    except IOError as e:
        print(f"Error: {e}")
        return None
    

def json_to_dict(filename: str) -> Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            json_str = file.read()
    except IOError as e:
        print(f"Error: {e}")
        return None
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error: {e}")
        return None