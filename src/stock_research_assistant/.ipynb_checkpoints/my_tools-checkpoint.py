from datetime import date 
from crewai.tools import BaseTool
from pydantic.v1 import BaseModel, Field # Use pydantic.v1 if needed
from api_calling import symbol_lookup , get_response

today =  date.today()

today_string = today.strftime("%Y-%m-%d")

class symbol_api_input_schema(BaseModel):
    """Input schema for the Legacy API Tool, defining info the LLM needs to find."""

    keyword: str = Field(description="Extract only the name of the company as a keyword to be looked up")


class stock_api_input_schema(BaseModel):
    """Input schema for the Legacy API Tool, defining info the LLM needs to find."""

    sym: str = Field(description="symbol_lookup_api_output_response , it'll be 3 to 5 capital letter string representing the symbol via which the stock is represented in NASDAQ stock exchange")
    start_date: str = Field(description="Compute this based on the input prompt and maybe calculate backwards from today's date or end date (however instructed)")
    end_date: str = Field(description="date in the format YYYY-MM-DD , based on the prompt given as input")



class symbol_getter(BaseTool):
    name: str = "This tool gives us the symbol of the stock, as indentified by NASDAQ Stock Exchange"
    description: str = (
        "This tool gives us the symbol of the stock, as indentified by NASDAQ Stock Exchange"
        "It is taking in the company name ONLY as input and using finnhub api to fetch the equivalent stock symbol mapped to the company in NASDAQ"
    )
    args_schema: type[BaseModel] = symbol_api_input_schema # Link the schema

    # 3. Implement the _run method
    # This method receives the validated arguments from the LLM.
    def _run(
        self,
        # Use explicit arguments matching your Pydantic schema fields
        keyword: str,
        ) -> str:
        """
        Uses the received arguments to call the actual underlying logic.
        Performs minimal formatting or validation, relying on Pydantic.
        """
        try:
            # --- Minimal Processing / Formatting (ONLY if necessary for the underlying call) ---
            # Example: Convert date string to a specific format required by the backend
            # Example: Convert a string value to an internal enum or constant

            # --- Call the Actual Underlying Logic ---
            # This is where you integrate with your external system, API, database, etc.
            # Replace `call_your_backend_function` with your actual code.
            # Pass the processed arguments to your function.
            result = symbol_lookup(keyword)

            # --- Return the Result ---
            # The result should be a string that the LLM can understand and use.
            return str(result) # Convert the result to a string

        except Exception as e:
            # --- Handle Errors ---
            # Catch exceptions from your backend function call.
            return f"An error occurred while using {self.name}: {e}"




            
class data_getter(BaseTool):
    name: str = "This tool gives us the historical data of the stock"
    description: str = (
        """This tool gives us the historical data of the stock, based on the specified time window"
        "It is taking in the stock symbol, start_date and end_date as input and using market data api to fetch the data in the format of lists with corresponding information mapped to the equivalent indices. For example , in this sample data : {'timeframe': [1744603200,
  1744689600,
  1744776000,
  1744862400,
  1745208000,
  1745294400],
 'opening_price': [144.16, 145.84, 144.11, 140.34, 142.5, 142.28],
 'highest_price_of_the_day': [147.175,
  145.98,
  144.4,
  143.5664,
  142.83,
  144.275],
 'lowest_price_of_the_day': [143.5,
  142.6274,
  139.7698,
  140.075,
  140.57,
  141.95],
 'closing_price_of_the_day': [146.75, 142.84, 140.09, 142.84, 141.73, 143.46]}

  In this sample output , the data is a dictionary of list where every let's say timeframe list corresponds to the unix encoded dates where for index 0 , all the other lists will have the corresponding values at index 0 that are associated to timeframe list value at index 0.
    """
    )
    args_schema: type[BaseModel] = stock_api_input_schema # Link the schema

    # 3. Implement the _run method
    # This method receives the validated arguments from the LLM.
    def _run(
        self,
        # Use explicit arguments matching your Pydantic schema fields
        sym: str,
        start_date:str,
        end_date:str,
        ) -> str:
        """
        Uses the received arguments to call the actual underlying logic.
        Performs minimal formatting or validation, relying on Pydantic.
        """
        try:
            # --- Minimal Processing / Formatting (ONLY if necessary for the underlying call) ---
            # Example: Convert date string to a specific format required by the backend
            # Example: Convert a string value to an internal enum or constant

            # --- Call the Actual Underlying Logic ---
            # This is where you integrate with your external system, API, database, etc.
            # Replace `call_your_backend_function` with your actual code.
            # Pass the processed arguments to your function.
            result = get_response(sym,start_date,end_date)

            # --- Return the Result ---
            # The result should be a string that the LLM can understand and use.
            return result # Convert the result to a string

        except Exception as e:
            # --- Handle Errors ---
            # Catch exceptions from your backend function call.
            return f"An error occurred while using {self.name}: {e}"

    

    
