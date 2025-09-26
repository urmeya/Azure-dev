import logging
import time
from .base_processor import BaseProcessor, ProcessorRegistry

# The unique key used for routing this processor
PROCESSOR_NAME = "downstream_app_1"

class DownstreamAppProcessor(BaseProcessor):
    """
    Concrete implementation for the first downstream application.
    Performs specific data filtering and transformation.
    """
    def process(self, data: dict) -> dict:
        """
        Transforms the input data:
        1. Filters items to include only those where 'status' is 'active'.
        2. Renames keys for consistency ('user_id' -> 'userId').
        3. Adds a processing timestamp.
        """
        logging.info(f"[{PROCESSOR_NAME}] Starting data processing.")

        processed_items = []
        raw_items = data.get("items", [])
        
        # Iteratively process items with error handling per item
        for item in raw_items:
            try:
                # Filtering logic
                if item.get("status") == "active":
                    transformed_item = {
                        "userId": item.get("user_id"),
                        "productName": item.get("product_name", "N/A"), # Default value for robustness
                        "quantity": item.get("quantity", 0),
                        "processed_timestamp": time.time()
                    }
                    processed_items.append(transformed_item)
            except Exception as e:
                # Log an error for a specific item but continue processing
                logging.error(f"[{PROCESSOR_NAME}] Failed to process item: {item}. Error: {e}")

        # Final output object, including a summary
        output = {
            "source_data_key": data.get("source_id", "unknown"),
            "processed_items": processed_items,
            "summary": {
                "total_items_received": len(raw_items),
                "total_items_processed": len(processed_items)
            }
        }
        logging.info(f"[{PROCESSOR_NAME}] Data processing completed. {len(processed_items)} items finalized.")
        return output

# --- Self-Registration Pattern ---
# The processor registers itself upon module import, making it available
# in the central registry without the main function needing to know about it.
ProcessorRegistry.register_processor(PROCESSOR_NAME, DownstreamAppProcessor())
