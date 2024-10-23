import logging


def handle_error(e):
    """Handle errors and log them."""
    logging.error(f"Error: {str(e)}")
    return {"error": str(e)}