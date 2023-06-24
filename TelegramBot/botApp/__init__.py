import logging
from .app import dp
from . import account_action
from . import authorization
from . import workout_creator
from . import workout_delete

logging.basicConfig(level=logging.INFO)