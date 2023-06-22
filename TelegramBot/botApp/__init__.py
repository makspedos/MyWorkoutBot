import logging
from .app import dp
from . import commands
from . import authorization

logging.basicConfig(level=logging.INFO)