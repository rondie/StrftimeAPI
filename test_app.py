import datetime
import re
from unittest.mock import patch

import pytest
from flask import Flask

from app import app as flask_app


@pytest.fixture
def client():
    """Create a test client for the app."""
    with flask_app.test_client() as client:
        yield client


def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to StrftimeAPI" in response.data


def test_time_format(client):
    """Test that time formatting works correctly."""
    # Fix the datetime to a specific value for testing
    test_datetime = datetime.datetime(2025, 4, 8, 12, 34, 56)

    with patch("datetime.datetime") as mock_datetime:
        # Configure the mock to return our fixed datetime when now() is called
        mock_datetime.now.return_value = test_datetime

        # Test a few different format strings
        test_cases = [
            ("%Y-%m-%d", "2025-04-08"),
            ("%H:%M:%S", "12:34:56"),
            ("%A, %B %d, %Y", "Tuesday, April 08, 2025"),
            ("%I:%M %p", "12:34 PM"),
        ]

        for format_string, expected in test_cases:
            response = client.get(f"/{format_string}")
            assert response.status_code == 200
            assert response.data.decode("utf-8") == expected


def test_invalid_format_string(client):
    """Test that invalid format strings are rejected."""
    # %K is not a valid format directive in strftime
    response = client.get("/%K")
    assert response.status_code == 400
    assert b"Error: Invalid format code" in response.data


def test_security_check(client):
    """Test that potentially malicious format strings are rejected."""
    security_test_cases = [
        "/%Y;rm -rf /",
        "/%Y&cat /etc/passwd",
        "/%Y`ls -la`",
        "/%Y|echo 'hacked'",
    ]

    for case in security_test_cases:
        response = client.get(case)
        assert response.status_code == 400
        assert b"Error" in response.data
