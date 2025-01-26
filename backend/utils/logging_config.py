
import logging
import absl.logging

def setup_logging():
    """Setup logging configuration."""
    # Configure Python logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Configure absl logging to use Python logging handlers
    absl.logging.use_absl_handler()
    absl.logging.set_verbosity('info')

setup_logging()


