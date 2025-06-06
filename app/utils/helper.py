from datetime import datetime, timedelta, time, date
import os
import orjson
import pytz
import math
import json
import re
import asyncio

def check_market_hours():

    holidays = ['2025-01-01', '2025-01-09','2025-01-20', '2025-02-17', '2025-04-18', '2025-05-26', '2025-06-19', '2025-07-04', '2025-09-01', '2025-11-27', '2025-12-25']

    
    # Get the current date and time in ET (Eastern Time)
    et_timezone = pytz.timezone('America/New_York')
    current_time = datetime.now(et_timezone)
    current_date_str = current_time.strftime('%Y-%m-%d')
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_day = current_time.weekday()  # Monday is 0, Sunday is 6

    # Check if the current date is a holiday or weekend
    is_weekend = current_day >= 5  # Saturday (5) or Sunday (6)
    is_holiday = current_date_str in holidays

    # Determine the market status
    if is_weekend or is_holiday:
        return False #"Market is closed."
    elif (current_hour == 16 and current_minute == 10) or 9 <= current_hour < 16:
        return True #"Market hours."
    else:
        return False #"Market is closed."


def load_latest_json(directory: str, find=True):
    """
    Load the JSON file corresponding to today's date (New York time) or the last Friday if today is a weekend.
    If `find` is True, try going back one day up to 10 times until a JSON file is found.
    If `find` is False, only check the current date (or adjusted Friday for weekends).
    """
    try:
        # Get today's date in New York timezone
        ny_tz = pytz.timezone("America/New_York")
        today_ny = datetime.now(ny_tz).date()

        # Adjust to Friday if today is Saturday or Sunday
        if today_ny.weekday() == 5:  # Saturday
            today_ny -= timedelta(days=1)
        elif today_ny.weekday() == 6:  # Sunday
            today_ny -= timedelta(days=2)

        attempts = 0

        # Loop to find the JSON file
        while True:
            # Construct the filename based on the adjusted date
            target_filename = f"{today_ny}.json"
            target_file_path = os.path.join(directory, target_filename)

            # Check if the file exists and load it
            if os.path.exists(target_file_path):
                with open(target_file_path, 'rb') as file:
                    print(f"JSON file found for date: {today_ny}")
                    return orjson.loads(file.read())

            # If find is False, only check the current date and exit
            if not find:
                print(f"No JSON file found for date: {today_ny}. Exiting as `find` is set to False.")
                break

            # Increment attempts and move to the previous day
            attempts += 1
            if attempts >= 10:
                print("No JSON file found after 10 attempts.")
                break
            today_ny -= timedelta(days=1)

        # Return an empty list if no file is found
        return []

    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

'''
def get_last_completed_quarter():
    today = datetime.today()
    year = today.year
    month = today.month
    # Calculate the current quarter (1 to 4)
    current_quarter = (month - 1) // 3 + 1

    # The previous quarter is the last completed quarter.
    # If we're in Q1, the previous quarter is Q4 of last year.
    if current_quarter == 1:
        return 4, year - 1
    else:
        return current_quarter - 1, year
'''

def get_last_completed_quarter():
    #return last two quarters ago
    today = datetime.today()
    year = today.year
    month = today.month
    # Calculate the current quarter (1 to 4)
    current_quarter = (month - 1) // 3 + 1

    # Determine the quarter that is two quarters ago.
    target_quarter = current_quarter - 2
    if target_quarter < 1:
        target_quarter += 4
        year -= 1

    return target_quarter, year



def replace_representative(office):
    replacements = {
        'Banks, James E. (Senator)': 'James Banks',
        'Banks, James (Senator)': 'James Banks',
        'James E Hon Banks': 'James Banks',
        'Knott, Brad (Senator)': 'Brad Knott',
        'Moody, Ashley B. (Senator)': 'Ashley Moody',
        'McCormick, David H. (Senator)': 'Dave McCormick',
        'McCormick, David H.': 'Dave McCormick',
        'Carper, Thomas R. (Senator)': 'Tom Carper',
        'Thomas R. Carper': 'Tom Carper',
        'Tuberville, Tommy (Senator)': 'Tommy Tuberville',
        'Ricketts, Pete (Senator)': 'John Ricketts',
        'Pete Ricketts': 'John Ricketts',
        'Moran, Jerry (Senator)': 'Jerry Moran',
        'Fischer, Deb (Senator)': 'Deb Fischer',
        'Mullin, Markwayne (Senator)': 'Markwayne Mullin',
        'Whitehouse, Sheldon (Senator)': 'Sheldon Whitehouse',
        'Toomey, Pat (Senator)': 'Pat Toomey',
        'Sullivan, Dan (Senator)': 'Dan Sullivan',
        'Capito, Shelley Moore (Senator)': 'Shelley Moore Capito',
        'Roberts, Pat (Senator)': 'Pat Roberts',
        'King, Angus (Senator)': 'Angus King',
        'Hoeven, John (Senator)': 'John Hoeven',
        'Duckworth, Tammy (Senator)': 'Tammy Duckworth',
        'Perdue, David (Senator)': 'David Perdue',
        'Inhofe, James M. (Senator)': 'James M. Inhofe',
        'Murray, Patty (Senator)': 'Patty Murray',
        'Boozman, John (Senator)': 'John Boozman',
        'Loeffler, Kelly (Senator)': 'Kelly Loeffler',
        'Reed, John F. (Senator)': 'John F. Reed',
        'Collins, Susan M. (Senator)': 'Susan M. Collins',
        'Cassidy, Bill (Senator)': 'Bill Cassidy',
        'Wyden, Ron (Senator)': 'Ron Wyden',
        'Hickenlooper, John (Senator)': 'John Hickenlooper',
        'Booker, Cory (Senator)': 'Cory Booker',
        'Donald Beyer, (Senator).': 'Donald Sternoff Beyer',
        'Peters, Gary (Senator)': 'Gary Peters',
        'Donald Sternoff Beyer, (Senator).': 'Donald Sternoff Beyer',
        'Donald S. Beyer, Jr.': 'Donald Sternoff Beyer',
        'Donald Sternoff Honorable Beyer': 'Donald Sternoff Beyer',
        'K. Michael Conaway': 'Michael Conaway',
        'C. Scott Franklin': 'Scott Franklin',
        'Scott Scott Franklin': 'Scott Franklin',
        'Robert C. "Bobby" Scott': 'Bobby Scott',
        'Kelly Louise Morrison': 'Kelly Morrison',
        'Madison Cawthorn': 'David Madison Cawthorn',
        'Cruz, Ted (Senator)': 'Ted Cruz',
        'Smith, Tina (Senator)': 'Tina Smith',
        'Graham, Lindsey (Senator)': 'Lindsey Graham',
        'Hagerty, Bill (Senator)': 'Bill Hagerty',
        'Scott, Rick (Senator)': 'Rick Scott',
        'Warner, Mark (Senator)': 'Mark Warner',
        'McConnell, A. Mitchell Jr. (Senator)': 'Mitch McConnell',
        'Mitchell McConnell': 'Mitch McConnell',
        'Charles J. "Chuck" Fleischmann': 'Chuck Fleischmann',
        'Vance, J.D. (Senator)': 'James Vance',
        'Neal Patrick MD, Facs Dunn': 'Neal Dunn',
        'Neal Patrick MD, Facs Dunn (Senator)': 'Neal Dunn',
        'Neal Patrick Dunn, MD, FACS': 'Neal Dunn',
        'Neal P. Dunn': 'Neal Dunn',
        'Tillis, Thom (Senator)': 'Thom Tillis',
        'W. Gregory Steube': 'Greg Steube',
        'W. Grego Steube': 'Greg Steube',
        'W. Greg Steube': 'Greg Steube',
        'David David Madison Cawthorn': 'David Madison Cawthorn',
        'Blunt, Roy (Senator)': 'Roy Blunt',
        'Thune, John (Senator)': 'John Thune',
        'Rosen, Jacky (Senator)': 'Jacky Rosen',
        'Britt, Katie (Senator)': 'Katie Britt',
        'Britt, Katie': 'Katie Britt',
        'James Costa': 'Jim Costa',
        'Lummis, Cynthia (Senator)': 'Cynthia Lummis',
        'Coons, Chris (Senator)': 'Chris Coons',
        'Udall, Tom (Senator)': 'Tom Udall',
        'Kennedy, John (Senator)': 'John Kennedy',
        'Bennet, Michael (Senator)': 'Michael Bennet',
        'Casey, Robert P. Jr. (Senator)': 'Robert Casey',
        'Van Hollen, Chris (Senator)': 'Chris Van Hollen',
        'Manchin, Joe (Senator)': 'Joe Manchin',
        'Cornyn, John (Senator)': 'John Cornyn',
        'Enzy, Michael (Senator)': 'Michael Enzy',
        'Cardin, Benjamin (Senator)': 'Benjamin Cardin',
        'Kaine, Tim (Senator)': 'Tim Kaine',
        'Joseph P. Kennedy III': 'Joe Kennedy',
        'James E Hon Banks': 'Jim Banks',
        'Michael F. Q. San Nicolas': 'Michael San Nicolas',
        'Barbara J Honorable Comstock': 'Barbara Comstock',
        'Darin McKay LaHood': 'Darin LaHood',
        'Harold Dallas Rogers': 'Hal Rogers',
        'April McClain Delaney': 'April Delaney',
        'Mr ': '',
        'Mr. ': '',
        'Dr ': '',
        'Dr. ': '',
        'Mrs ': '',
        'Mrs. ': '',
        '(Senator)': '',
    }

    for old, new in replacements.items():
        office = office.replace(old, new)
        office = ' '.join(office.split())
    return office


def compute_option_return(option: dict, current_price: float) -> float:
   
    try:
        # --- Parse and validate basic fields ---
        pc = option.get("put_call")

    
        strike = float(option["strike_price"])
        sentiment = option.get("sentiment")
        if sentiment is None:
            return None
        sentiment = str(sentiment).strip().capitalize()

        # Determine long/short from sentiment
        if pc == "Calls":
            is_long = sentiment in ("Bullish", "Neutral")
        else:  # PUT
            is_long = sentiment in ("Bearish", "Neutral")

        # --- Cost basis ---
        # If provided, use it; else calculate
        cost_basis = option.get("cost_basis")
        size = option.get('size',0)

        multiplier = 100

        intrinsic = 0.0
        if pc == "Calls":
            intrinsic = max(current_price - strike, 0.0)
        else:
            intrinsic = max(strike - current_price, 0.0)

        current_premium = intrinsic

        # --- Mark-to-market P/L ---
        current_value = current_premium * size * multiplier

        if is_long:
            profit = current_value - cost_basis
        else:
            profit = cost_basis - current_value

        pct_return = (profit / cost_basis) * 100.0

        if not math.isfinite(pct_return):
            return None

        return round(pct_return, 2)

    except Exception:
        return None

def json_to_string(json_data):
    try:
        # Use json.dumps() for a more robust and readable conversion
        formatted_string = json.dumps(json_data, indent=4)  # Indent for better readability
        return formatted_string
    except TypeError as e:
        return f"Error: Invalid JSON data.  Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# --- Enhanced Configuration for Trigger Phrases ---
TRIGGER_CONFIG = {
    "@Analyst": {
        "description": "Handles analyst-related queries by forcing specific financial tool calls.",
        "parameter_extraction": {
            "prompt_template": "First identify the stock ticker symbols mentioned in the user's query: '{query}'. If no specific tickers are mentioned, identify which companies the user is likely interested in and determine their ticker symbols. Return ONLY the ticker symbols as a comma-separated list without any explanation or additional text. Example response format: 'AAPL,MSFT,GOOG'",
            "regex_pattern": r'\$?([A-Z]{1,5})\b',
            "default_value": ["AAPL"],
            "param_name": "tickers_list"
        },
        "perform_initial_llm_call": True,
        "pre_forced_tools_assistant_message_template": "Let me check the analyst information for {params}.",
        "forced_tool_calls": [
            {
                "id_template": "afunc1_{index}",
                "function_name": "get_analyst_estimate",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True  # Ensures this function MUST be called
            },
            {
                "id_template": "afunc2_{index}",
                "function_name": "get_analyst_ratings",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            }
        ],
        "validate_all_calls_executed": True,  # New flag to ensure all functions are called
    },
    "@OptionsFlow": {
        "description": "Handles options flow order related queries by forcing specific financial tool calls.",
        "parameter_extraction": {
            "prompt_template": "First identify the stock ticker symbols mentioned in the user's query: '{query}'. Return ONLY the ticker symbols as a comma-separated list without any explanation or additional text. Example response format: 'AAPL,MSFT,GOOG'. If no specific tickers are mentioned, set the argument to an empty list",
            "regex_pattern": r'\$?([A-Z]{1,5})\b',
            "default_value": [],
            "param_name": "tickers_list"
        },
        "perform_initial_llm_call": True,
        "pre_forced_tools_assistant_message_template": "Let me check the latest options flow orders information for {params}.",
        "forced_tool_calls": [
            {
                "id_template": "ofeed_{index}",
                "function_name": "get_latest_options_flow_feed",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
        ],
        "validate_all_calls_executed": True,
    },
    "@DarkPoolFlow": {
        "description": "Handles dark pool flow order related queries by forcing specific financial tool calls.",
        "parameter_extraction": {
            "prompt_template": "First identify the stock ticker symbols mentioned in the user's query: '{query}'. Return ONLY the ticker symbols as a comma-separated list without any explanation or additional text. Example response format: 'AAPL,MSFT,GOOG'. If no specific tickers are mentioned, set the argument to an empty list",
            "regex_pattern": r'\$?([A-Z]{1,5})\b',
            "default_value": [],
            "param_name": "tickers_list"
        },
        "perform_initial_llm_call": True,
        "pre_forced_tools_assistant_message_template": "Let me check the latest dark pool flow orders information for {params}.",
        "forced_tool_calls": [
            {
                "id_template": "dark_pool_feed_{index}",
                "function_name": "get_latest_dark_pool_feed",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
        ],
        "validate_all_calls_executed": True,
    },
    "@News": {
        "description": "Handles news-related queries by forcing specific financial tool calls.",
        "parameter_extraction": {
            "prompt_template": "First identify the stock ticker symbols mentioned in the user's query: '{query}'. If no specific tickers are mentioned, identify which companies the user is likely interested in and determine their ticker symbols. Return ONLY the ticker symbols as a comma-separated list without any explanation or additional text. Example response format: 'AAPL,MSFT,GOOG'",
            "regex_pattern": r'\$?([A-Z]{1,5})\b',
            "default_value": ["AAPL"],
            "param_name": "tickers_list"
        },
        "perform_initial_llm_call": True,
        "pre_forced_tools_assistant_message_template": "Let me check the latest news information for {params}.",
        "forced_tool_calls": [
            {
                "id_template": "wiim_{index}",
                "function_name": "get_why_priced_moved",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "marketNews_{index}",
                "function_name": "get_market_news",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            }
        ],
        "validate_all_calls_executed": True,
    },
    "@RealtimeData": {
        "description": "Retrieves and aggregates real-time market insights relevant to today's activity for specified stocks. This includes automatic invocation of financial tools to analyze price movements, news, dark pool activity, options flow, and analyst ratings.",
        "parameter_extraction": {
            "prompt_template": "Identify the stock ticker symbols mentioned in the user's query: '{query}'. If no explicit symbols are provided, infer which companies the user is likely referring to and return their ticker symbols. Output only the symbols as a comma-separated list with no additional text. Example: 'AAPL,MSFT,GOOG'.",
            "regex_pattern": "\\$?([A-Z]{1,5})\\b",
            "default_value": ["AAPL"],
            "param_name": "tickers_list"
        },
        "perform_initial_llm_call": True,
        "pre_forced_tools_assistant_message_template": "Provide only the relevant data for today's trading session. If today is a weekend or market holiday, reference the most recent trading day instead for {params}.",
        "forced_tool_calls": [
            {
                "id_template": "realtime_wiim_{index}",
                "function_name": "get_why_priced_moved",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "realtime_marketNews_{index}",
                "function_name": "get_market_news",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "realtime_dp_{index}",
                "function_name": "get_latest_dark_pool_feed",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "realtime_options_{index}",
                "function_name": "get_latest_options_flow_feed",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "realtime_analyst_rating_{index}",
                "function_name": "get_analyst_ratings",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            },
            {
                "id_template": "realtime_stock_quote_{index}",
                "function_name": "get_stock_quote",
                "arguments_mapping": {"tickers": "tickers_list"},
                "required": True
            }
        ],
        "validate_all_calls_executed": True,
    },
}


# --- Enhanced Helper Functions ---
class ForcedToolCallExecutionError(Exception):
    """Raised when forced tool calls fail to execute properly."""
    pass


async def _extract_parameters(user_query, extraction_config, async_client, model, max_tokens, semaphore, context_messages):
    """Extracts parameters based on the provided configuration."""
    extracted_values = []
    param_name = extraction_config["param_name"]

    # 1. LLM-based extraction
    if extraction_config.get("prompt_template"):
        extraction_prompt_content = extraction_config["prompt_template"].format(query=user_query)
        
        llm_extraction_messages = context_messages.copy()
        llm_extraction_messages.append({"role": "system", "content": extraction_prompt_content})
        
        async with semaphore:
            response = await async_client.chat.completions.create(
                model=model,
                messages=llm_extraction_messages,
                max_tokens=max_tokens
            )
        params_str = response.choices[0].message.content.strip()
        if params_str:
            extracted_values = [p.strip() for p in params_str.split(',') if p.strip()]

    # 2. Regex fallback
    if not extracted_values and extraction_config.get("regex_pattern"):
        matches = re.findall(extraction_config["regex_pattern"], user_query)
        if matches:
            if isinstance(matches[0], tuple):
                extracted_values = [m[0].strip() for m in matches if m[0].strip()]
            else:
                extracted_values = [m.strip() for m in matches if m.strip()]
    
    # 3. Default fallback
    if not extracted_values and extraction_config.get("default_value"):
        extracted_values = extraction_config["default_value"]

    return {param_name: extracted_values}


async def _execute_and_append_tool_calls(tool_calls_to_process, messages, function_map, validate_execution=False):
    """
    Executes a list of tool calls and appends results to messages.
    
    Args:
        tool_calls_to_process: List of tool calls to execute
        messages: Message list to append results to
        function_map: Available functions
        validate_execution: If True, raises exception if any tool call fails
    """
    execution_results = {"successful": [], "failed": []}
    
    async def execute_single_tool(call_info):
        is_forced_call_dict = isinstance(call_info, dict)
        tool_call_id = call_info.id if not is_forced_call_dict else call_info["id"]
        fn_name = call_info.function.name if not is_forced_call_dict else call_info["function"]["name"]
        arguments_str = call_info.function.arguments if not is_forced_call_dict else call_info["function"]["arguments"]
        
        result_content_payload = {}
        success = False
        
        try:
            args = json.loads(arguments_str)
            if fn_name in function_map:
                result_content_payload = await function_map[fn_name](**args)
                success = True
                print(f"✓ Successfully executed function: {fn_name}")
            else:
                error_msg = f"Unknown function {fn_name} requested by tool call."
                print(f"✗ Error: {error_msg}")
                result_content_payload = {"error": error_msg}
        except json.JSONDecodeError as e:
            error_msg = f"Invalid arguments format for {fn_name}: {str(e)}"
            print(f"✗ JSON Error: {error_msg}. Arguments: '{arguments_str}'")
            result_content_payload = {"error": error_msg}
        except Exception as e:
            error_msg = f"Error executing function {fn_name}: {str(e)}"
            print(f"✗ Execution Error: {error_msg}")
            result_content_payload = {"error": error_msg}

        tool_result = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": fn_name,
            "content": json.dumps(result_content_payload)
        }
        
        if success:
            execution_results["successful"].append(fn_name)
        else:
            execution_results["failed"].append(fn_name)
            
        return tool_result

    # Execute all tool calls concurrently
    tasks = [execute_single_tool(tc) for tc in tool_calls_to_process]
    tool_results_messages = await asyncio.gather(*tasks)

    # Append all results to messages
    for res_msg in tool_results_messages:
        messages.append(res_msg)
    
    # Validate execution if required
    if validate_execution and execution_results["failed"]:
        failed_functions = ", ".join(execution_results["failed"])
        raise ForcedToolCallExecutionError(
            f"Failed to execute required functions: {failed_functions}"
        )
    
    print(f"Tool execution summary - Successful: {len(execution_results['successful'])}, "
          f"Failed: {len(execution_results['failed'])}")
    
    return execution_results


async def _validate_forced_tool_calls_completion(config, execution_results):
    """
    Validates that all required forced tool calls were executed successfully.
    """
    if not config.get("validate_all_calls_executed", False):
        return True
    
    required_functions = [
        tool_call["function_name"] 
        for tool_call in config.get("forced_tool_calls", [])
        if tool_call.get("required", True)
    ]
    
    successful_functions = execution_results.get("successful", [])
    missing_functions = [fn for fn in required_functions if fn not in successful_functions]
    
    if missing_functions:
        raise ForcedToolCallExecutionError(
            f"Required functions were not executed successfully: {', '.join(missing_functions)}"
        )
    
    print(f"✓ All {len(required_functions)} required functions executed successfully")
    return True


async def _handle_configured_case(data, base_messages, config, user_query, 
                                  async_client, chat_model, max_tokens, semaphore, 
                                  function_map, system_message, tools_payload):
    """Handles request processing for a specifically configured trigger case."""
    messages = base_messages.copy()
    extracted_data = {}

    print(f"Processing configured case: {config['description']}")

    # 1. Parameter Extraction
    if "parameter_extraction" in config:
        context_for_extraction = messages.copy()
        extracted_data = await _extract_parameters(
            user_query,
            config["parameter_extraction"],
            async_client,
            chat_model,
            max_tokens,
            semaphore,
            context_for_extraction
        )
        print(f"Extracted parameters: {extracted_data}")
        
        # Ensure default is applied if extraction yields nothing
        param_conf = config["parameter_extraction"]
        if not extracted_data.get(param_conf["param_name"]) and param_conf.get("default_value"):
           extracted_data[param_conf["param_name"]] = param_conf["default_value"]

    # 2. Initial LLM Call (optional)
    if config.get("perform_initial_llm_call", False):
        print("Performing initial LLM call...")
        async with semaphore:
            initial_response = await async_client.chat.completions.create(
                model=chat_model,
                messages=messages,
                max_tokens=max_tokens
            )
        assistant_msg_before_forced = initial_response.choices[0].message
        messages.append(assistant_msg_before_forced)

    # 3. Execute Forced Tool Calls (GUARANTEED EXECUTION)
    if "forced_tool_calls" in config and config["forced_tool_calls"]:
        print(f"Executing {len(config['forced_tool_calls'])} forced tool calls...")
        
        forced_tool_call_objects_for_api = []
        param_values_for_template = []
        
        if "parameter_extraction" in config:
            param_values_for_template = extracted_data.get(
                config["parameter_extraction"]["param_name"], []
            )

        # Build forced tool call objects
        for i, tool_conf in enumerate(config["forced_tool_calls"]):
            function_args = {}
            if "arguments_mapping" in tool_conf:
                for func_arg_name, source_param_key in tool_conf["arguments_mapping"].items():
                    if source_param_key in extracted_data:
                        function_args[func_arg_name] = extracted_data[source_param_key]
                    else:
                        print(f"Warning: Source parameter '{source_param_key}' not found. Using empty list.")
                        function_args[func_arg_name] = []
            
            forced_tool_call_objects_for_api.append({
                "id": tool_conf["id_template"].format(index=i),
                "type": "function",
                "function": {
                    "name": tool_conf["function_name"],
                    "arguments": json.dumps(function_args)
                }
            })

        if forced_tool_call_objects_for_api:
            # Create assistant message with forced tool calls
            assistant_content = "Proceeding with required actions..."
            if config.get("pre_forced_tools_assistant_message_template"):
                assistant_content = config["pre_forced_tools_assistant_message_template"].format(
                    params=", ".join(map(str, param_values_for_template)) if param_values_for_template else "the relevant items"
                )
            
            messages.append({
                "role": "assistant",
                "content": assistant_content,
                "tool_calls": forced_tool_call_objects_for_api
            })
            
            # Execute forced tools with validation
            execution_results = await _execute_and_append_tool_calls(
                forced_tool_call_objects_for_api, 
                messages, 
                function_map,
                validate_execution=config.get("validate_all_calls_executed", False)
            )
            
            # Additional validation step
            await _validate_forced_tool_calls_completion(config, execution_results)

    # 4. Final Response from LLM
    print("Getting final response from LLM...")
    final_llm_messages = messages.copy()
    
    async with semaphore:
        final_response = await async_client.chat.completions.create(
            model=chat_model,
            messages=final_llm_messages,
            max_tokens=max_tokens
        )
    final_assistant_msg = final_response.choices[0].message
    messages.append(final_assistant_msg)

    print("✓ Configured case processing completed successfully")
    return messages


async def process_request(data, async_client, function_map, request_semaphore, system_message, 
                         CHAT_MODEL, MAX_TOKENS, tools_payload):
    """
    Enhanced process_request function with guaranteed function execution for triggers.
    """
    user_query = data.query.lower()
    current_messages_history = list(data.messages) 

    prepared_initial_messages = [system_message] + current_messages_history + [
        {"role": "user", "content": user_query}
    ]

    active_config = None
    trigger_phrase_found = None

    # Check for trigger phrases
    for trigger, config_item in TRIGGER_CONFIG.items():
        if trigger.lower() in user_query:
            active_config = config_item
            trigger_phrase_found = trigger
            print(f"🎯 Detected trigger: {trigger_phrase_found}")
            break
            
    try:
        if active_config:
            # Handle request using the specific configuration for the detected trigger
            # This guarantees all configured functions will be called
            return await _handle_configured_case(
                data, prepared_initial_messages, active_config, user_query,
                async_client, CHAT_MODEL, MAX_TOKENS, request_semaphore,
                function_map, system_message, tools_payload
            )
        else:
            # Standard flow: LLM decides on tool usage
            print("Processing standard request (no triggers detected)")
            messages = prepared_initial_messages.copy()

            async with request_semaphore:
                response = await async_client.chat.completions.create(
                    model=CHAT_MODEL,
                    messages=messages,
                    max_tokens=MAX_TOKENS,
                    tools=tools_payload,
                    tool_choice="auto" if tools_payload else "none"
                )
            
            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            # Handle multiple rounds of tool calls if initiated by the LLM
            while hasattr(assistant_msg, 'tool_calls') and assistant_msg.tool_calls:
                await _execute_and_append_tool_calls(assistant_msg.tool_calls, messages, function_map)
                
                async with request_semaphore:
                    followup_response = await async_client.chat.completions.create(
                        model=CHAT_MODEL,
                        messages=messages,
                        max_tokens=MAX_TOKENS,
                        tools=tools_payload,
                        tool_choice="auto" if tools_payload else "none" 
                    )
                assistant_msg = followup_response.choices[0].message
                messages.append(assistant_msg)
            
            return messages

    except ForcedToolCallExecutionError as e:
        print(f"❌ Forced tool call execution failed: {e}")
        # You might want to return an error message or retry logic here
        raise
    except Exception as e:
        print(f"❌ Request processing failed: {e}")
        raise


# --- Utility Functions for Monitoring ---

def get_trigger_statistics():
    """Returns statistics about configured triggers."""
    stats = {}
    for trigger, config in TRIGGER_CONFIG.items():
        forced_calls = config.get("forced_tool_calls", [])
        stats[trigger] = {
            "description": config.get("description", ""),
            "total_forced_functions": len(forced_calls),
            "required_functions": len([fc for fc in forced_calls if fc.get("required", True)]),
            "function_names": [fc["function_name"] for fc in forced_calls],
            "validation_enabled": config.get("validate_all_calls_executed", False)
        }
    return stats


def validate_trigger_config():
    """Validates the trigger configuration for consistency."""
    issues = []
    
    for trigger, config in TRIGGER_CONFIG.items():
        # Check for required fields
        if not config.get("description"):
            issues.append(f"{trigger}: Missing description")
        
        # Check forced tool calls
        forced_calls = config.get("forced_tool_calls", [])
        for i, call in enumerate(forced_calls):
            if not call.get("function_name"):
                issues.append(f"{trigger}: Tool call {i} missing function_name")
            if not call.get("id_template"):
                issues.append(f"{trigger}: Tool call {i} missing id_template")
    
    return issues