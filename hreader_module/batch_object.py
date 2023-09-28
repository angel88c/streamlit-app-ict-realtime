from dataclasses import dataclass
from typing import List
from btest_object import BTest

@dataclass
class Batch:
    uut_type: str 
    uut_type_rev: str
    fixture_id: int
    testhead_number: int
    testhead_type: str
    process_step: str
    id: str
    operator_id: str
    controller: str
    testplan_id: str
    testplan_rev: str
    parent_panel_type: str
    parent_panel_type_rev: str
    version_label: str
    board_records: List[BTest]