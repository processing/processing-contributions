import os
import sys

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts import fetch_updates


def test_log_broken():
    contribution = {
        "status": "VALID"
    }

    fetch_updates.log_broken(contribution, "file not found")

    assert contribution["status"] == "BROKEN"
    assert "log" in contribution
    assert contribution["log"] == ["file not found"]


def test_update_contribution():
    contribution = {
        "id": "test-id",
        "prettyVersion": "1.0",
        "source": "http://example.com/library.properties"
    }

    props = {
        "version": "2.0",
        "categories": '"Graphics,Animation"',
        "author": "Test Author"
    }

    fetch_updates.update_contribution(contribution, props)

    assert "lastUpdated" in contribution
    assert contribution["previousVersions"] == ["1.0"]
    assert contribution["version"] == "2.0"
    assert contribution["categories"] == ["Animation", "Graphics"]
    assert contribution["author"] == "Test Author"
    assert contribution["download"].endswith(".zip")
