from dataclasses import dataclass
from enum import Enum
from typing import List
from test_object import Test

class BoardStatus(Enum):
    passed = 0,
    uncategorized = 1,
    failed_in_pins = 2,
    failed_in_learn = 3,
    failed_in_shorts = 4,
    failed_in_analog = 6,
    failed_in_owerSuply = 7,
    failed_in_digital_Or_BScan = 8,
    failed_in_functional = 9,
    failed_in_preShorts = 10,
    failed_in_board_Handler = 11,
    failed_in_barcode = 12,
    xed_out = 13,
    failed_in_testjet = 14,
    failed_in_polarity_check = 15,
    failed_in_connect_check = 16,
    failed_in_analog_cluster = 17,
    runtime_error = 80,
    aborted_stop = 81,
    aborted_break = 82,

@dataclass
class BTest:
    board_id: str
    board_test_status: BoardStatus
    board_start_time: str
    board_duration: int
    board_is_multiple_test: bool
    board_log_level: str
    board_log_set: int
    board_is_learning_on: bool
    board_is_known_good: bool
    board_end_time: str
    board_status_qualifier: str
    board_number: int
    board_parent_panel: str
    board_tests: List[Test]
    