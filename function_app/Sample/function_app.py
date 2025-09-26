# import azure.functions as func
# import datetime
# import json
# import logging

# app = func.FunctionApp()

# @app.route(route="pi_response_processor", auth_level=func.AuthLevel.ANONYMOUS)
# def ExtractJobDetails(req: func.HttpRequest) -> func.HttpResponse:
#     return func.HttpResponse("This HTTP triggered function executed successfully.")

import json
import logging

import azure.functions as func

# Import the processors package to initialize the registry and fetch components
from processors.base_processor import configure_logging, ProcessorRegistry

# Initialize logging for the main function app
configure_logging(logging.INFO)

# The main FunctionApp instance using the V2 decorator model.
app = func.FunctionApp()

# --- HTTP Trigger for Data Processing ---
@app.route(route="process_data", auth_level=func.AuthLevel.ANONYMOUS)#func.AuthLevel.FUNCTION)
def process_data_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main entry point. Routes incoming JSON data to the correct processor
    based on the 'downstream_app' identifier provided in the header or query.
    """
    logging.info('Python HTTP trigger function received a request.')

    try:
        # 1. Get Downstream Application Identifier
        # We check both headers and query parameters for flexibility
        downstream_app = req.get_json().get("downstream_app", "")#req.headers.get('downstream_app', req.params.get('downstream_app'))
        if not downstream_app:
            return func.HttpResponse(
                "Error 400: Please provide a 'downstream_app' identifier in the query string or request headers.",
                status_code=400
            )

        # 2. Parse Input Payload
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("Invalid JSON format in the request body.")
            return func.HttpResponse(
                 "Error 400: Invalid JSON format in the request body.",
                 status_code=400
            )
        
        # 3. Routing and Processor Isolation
        processor = ProcessorRegistry.get_processor(downstream_app)
        if not processor:
            logging.warning(f"Error 404: No processor found for app: {downstream_app}")
            available_apps = ", ".join(ProcessorRegistry.list_processors())
            return func.HttpResponse(
                f"Error 404: No processor registered for '{downstream_app}'. Available apps: {available_apps}",
                status_code=404
            )

        # 4. Process Data - This calls the specific, modularized processor logic
        processed_data = processor.process(req_body)

        # 5. Return Success
        return func.HttpResponse(
            json.dumps(processed_data),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        # 6. Global Error Handling
        # This catches exceptions thrown during the processing phase
        logging.critical(f"Unhandled system error during execution: {e}", exc_info=True)
        return func.HttpResponse(
             "Error 500: An internal server error occurred.",
             status_code=500
        )

# --- HTTP Trigger for Health Check ---
@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Basic health check endpoint, returns 200 OK.
    """
    return func.HttpResponse("Healthy", status_code=200)

