import logging
import sys

# Custom formatter to include additional context (e.g., svix_id) in log messages
class SvixFormatter(logging.Formatter):
    def format(self, record):
        # Generate the base log message using the parent class's format method
        base = super().format(record)
        extras = []
        
        # Check if the log record has the attribute 'svix_id' and include it in the log
        if hasattr(record, "svix_id"):
            extras.append(f"svix-id={record.svix_id}")
            
        # Append any extra information to the base log message
        if extras:
            return f"{base} | {' '.join(extras)}"
        return base
    
# Function to set up and return a logger with console and file handlers
def setup_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG to capture all messages

    # Define a custom formatter with a specific format and date format
    formatter = SvixFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )
    
    # Console handler to output logs to the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler to write logs to a file
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
