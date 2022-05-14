from pathlib import Path
import yaml
from chieftane.strategy.models import Strategy
from loguru import logger

from chieftane.strategy.raw.models import RawStrategy


def parse_strategy_file(file_path: Path) -> Strategy:
    logger.info(f'Parsing strategy file {file_path}')
    configs = yaml.safe_load(file_path.read_text())
    print(configs)

    raw = RawStrategy.parse_obj(configs)

    return Strategy.from_raw(raw)
