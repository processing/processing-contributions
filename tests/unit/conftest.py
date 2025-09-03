import pytest


# Test Fixtures
@pytest.fixture
def valid_properties_data():
    """Complete valid data for PropertiesExisting"""
    return {
        "name": "Test Library",
        "authors": "John Doe, Jane Smith",
        "url": "https://example.com/library",
        "categories": "utility,helper",
        "sentence": "A helpful test library for demonstrations",
        "paragraph": "This is a more detailed description of the test library.",
        "version": "1",
        "prettyVersion": "1.0.0",
        "minRevision": "5",
        "maxRevision": "10",
        "modes": "standard,debug"
    }


@pytest.fixture
def valid_properties_data_aliases():
    """Complete valid data for PropertiesExisting"""
    return {
        "name": "Test Library",
        "authorList": "John Doe, Jane Smith",
        "url": "https://example.com/library",
        "category": "utility,helper",
        "sentence": "A helpful test library for demonstrations",
        "paragraph": "This is a more detailed description of the test library.",
        "version": "1",
        "prettyVersion": "1.0.0",
        "minRevision": "5",
        "maxRevision": "10",
        "compatibleModesList": "standard,debug"
    }


@pytest.fixture
def minimal_properties_base_data():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authors": "Test Author",
        "url": "https://minimal.com",
        "sentence": "A minimal test case",
        "version": "1",
        "prettyVersion": "1.0"
    }


@pytest.fixture
def minimal_properties_base_data_aliases():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authorList": "Test Author",
        "url": "https://minimal.com",
        "sentence": "A minimal test case",
        "version": "1",
        "prettyVersion": "1.0"
    }


@pytest.fixture
def minimal_properties_existing_data():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authors": "Test Author",
        "url": "https://minimal.com",
        "sentence": "A minimal test case",
        "version": "1",
    }


@pytest.fixture
def minimal_properties_existing_data_aliases():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authorList": "Test Author",
        "url": "https://minimal.com",
        "sentence": "A minimal test case",
        "version": "1",
    }


@pytest.fixture
def minimal_properties_library_data():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authors": "Test Author",
        "url": "https://minimal.com",
        "categories": "minimal,library",
        "sentence": "A minimal test case",
        "version": "1",
        "prettyVersion": "1.0"
    }


@pytest.fixture
def minimal_properties_library_data_aliases():
    """Minimal required data for PropertiesExisting"""
    return {
        "name": "Minimal Library",
        "authorList": "Test Author",
        "url": "https://minimal.com",
        "category": "minimal,library",
        "sentence": "A minimal test case",
        "version": "1",
        "prettyVersion": "1.0"
    }


@pytest.fixture
def properties_with_extra_fields():
    """Data with extra fields (should be allowed due to extra='allow')"""
    return {
        "name": "Extra Fields Library",
        "authors": "Extra Author",
        "url": "https://extra.com",
        "categories": "extra,fields",
        "sentence": "Library with extra fields",
        "version": "2",
        "prettyVersion": "2.0",
        "customField": "custom value",
        "anotherExtra": "42"
    }
