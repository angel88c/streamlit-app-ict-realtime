from dataclasses import dataclass
from enum import Enum

class TestStatus(Enum):
    passed = 0,
    failed = 1,
    failed_compliance_limit = 2,
    failed_detector_timeout = 3,
    failed_aborted_operator = 4
    
@dataclass
class Test:
    name: str
    status: TestStatus 
    measurement: float
    nominal: float
    high_limit: float
    low_limit: float
    test_type: str
    test_units: str
