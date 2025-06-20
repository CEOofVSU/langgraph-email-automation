import sys
from pathlib import Path

# Ensure src directory is on the path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tools.GmailTools import GmailToolsClass


def test_clean_body_text_normalizes_whitespace():
    sample = "Hello,\n   this is  \n a test.\r\n Thanks  "
    cleaner = GmailToolsClass.__new__(GmailToolsClass)
    result = cleaner._clean_body_text(sample)
    assert result == "Hello, this is a test. Thanks"
  
