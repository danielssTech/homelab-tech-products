import logging
import sys

def setup_logging():
    fmt = "[%(asctime)s] %(levelname)s %(name)s :: %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)

    return logging.getLogger("app")
