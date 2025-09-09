import pytest
from pydantic import ValidationError
from scripts.parse_and_validate_properties_txt import validate_new, validate_existing, validate_new_library


# Test Cases
class TestValidateAndExport:

    def test_validate_existing_complete_data(self, valid_properties_data):
        """Test validate_existing with complete data"""
        props = validate_existing(valid_properties_data)

        assert props['name'] == valid_properties_data['name']
        assert props['authors'] == valid_properties_data['authors']
        assert props['url'] == valid_properties_data['url']
        assert props['categories'] == valid_properties_data['categories']
        assert props['sentence'] == valid_properties_data['sentence']
        assert props['paragraph'] == valid_properties_data['paragraph']
        assert props['version'] == valid_properties_data['version']
        assert props['prettyVersion'] == valid_properties_data['prettyVersion']
        assert props['minRevision'] == int(valid_properties_data['minRevision'])
        assert props['maxRevision'] == int(valid_properties_data['maxRevision'])
        assert props['modes'] == valid_properties_data['modes']


    def test_validate_existing_minimal_required_data(self, minimal_properties_existing_data):
        """Test validate_existing with minimal data"""
        props = validate_existing(minimal_properties_existing_data)

        assert props['name'] == minimal_properties_existing_data['name']
        assert props['authors'] == minimal_properties_existing_data['authors']
        assert props['url'] == minimal_properties_existing_data['url']
        assert props['categories'] is None
        assert props['sentence'] == minimal_properties_existing_data['sentence']
        assert props['paragraph'] is None
        assert props['version'] == minimal_properties_existing_data['version']
        assert props['prettyVersion'] is None
        assert props['minRevision'] == 0  # Default value
        assert props['maxRevision'] == 0  # Default value
        assert props['modes'] is None


    def test_validate_existing_extra_fields_allowed(self, properties_with_extra_fields):
        """Test validate_existing with extra fields"""
        props = validate_existing(properties_with_extra_fields)

        assert props['name'] == properties_with_extra_fields['name']
        assert props['customField'] == properties_with_extra_fields['customField']
        assert props['anotherExtra'] == properties_with_extra_fields['anotherExtra']


    def test_validate_new_complete_data(self, valid_properties_data):
        """Test validate_new with complete data"""
        props = validate_new(valid_properties_data)

        assert props['name'] == valid_properties_data['name']
        assert props['authors'] == valid_properties_data['authors']
        assert props['url'] == valid_properties_data['url']
        assert props['categories'] == valid_properties_data['categories']
        assert props['sentence'] == valid_properties_data['sentence']
        assert props['paragraph'] == valid_properties_data['paragraph']
        assert props['version'] == int(valid_properties_data['version'])
        assert props['prettyVersion'] == valid_properties_data['prettyVersion']
        assert props['minRevision'] == int(valid_properties_data['minRevision'])
        assert props['maxRevision'] == int(valid_properties_data['maxRevision'])
        assert props['modes'] == valid_properties_data['modes']


    def test_validate_new_minimal_required_data(self, minimal_properties_base_data):
        """Test validate_new with minimal data"""
        props = validate_new(minimal_properties_base_data)

        assert props['name'] == minimal_properties_base_data['name']
        assert props['authors'] == minimal_properties_base_data['authors']
        assert props['url'] == minimal_properties_base_data['url']
        assert props['categories'] is None
        assert props['sentence'] == minimal_properties_base_data['sentence']
        assert props['paragraph'] is None
        assert props['version'] == int(minimal_properties_base_data['version'])
        assert props['prettyVersion'] == minimal_properties_base_data['prettyVersion']
        assert props['minRevision'] == 0  # Default value
        assert props['maxRevision'] == 0  # Default value
        assert props['modes'] is None


    def test_validate_new_extra_fields_allowed(self, properties_with_extra_fields):
        """Test validate_new with extra fields"""
        props = validate_new(properties_with_extra_fields)

        assert props['name'] == properties_with_extra_fields['name']
        assert props['customField'] == properties_with_extra_fields['customField']
        assert props['anotherExtra'] == properties_with_extra_fields['anotherExtra']


    def test_validate_new_library_complete_data(self, valid_properties_data):
        """Test validate_new_library with complete data"""
        props = validate_new_library(valid_properties_data)

        assert props['name'] == valid_properties_data['name']
        assert props['authors'] == valid_properties_data['authors']
        assert props['url'] == valid_properties_data['url']
        assert props['categories'] == valid_properties_data['categories']
        assert props['sentence'] == valid_properties_data['sentence']
        assert props['paragraph'] == valid_properties_data['paragraph']
        assert props['version'] == int(valid_properties_data['version'])
        assert props['prettyVersion'] == valid_properties_data['prettyVersion']
        assert props['minRevision'] == int(valid_properties_data['minRevision'])
        assert props['maxRevision'] == int(valid_properties_data['maxRevision'])
        assert props['modes'] == valid_properties_data['modes']


    def test_validate_new_library_minimal_required_data(self, minimal_properties_library_data):
        """Test validate_new_library with minimal data"""
        props = validate_new_library(minimal_properties_library_data)

        assert props['name'] == minimal_properties_library_data['name']
        assert props['authors'] == minimal_properties_library_data['authors']
        assert props['url'] == minimal_properties_library_data['url']
        assert props['categories'] == minimal_properties_library_data['categories']
        assert props['sentence'] == minimal_properties_library_data['sentence']
        assert props['paragraph'] is None
        assert props['version'] == int(minimal_properties_library_data['version'])
        assert props['prettyVersion'] == minimal_properties_library_data['prettyVersion']
        assert props['minRevision'] == 0  # Default value
        assert props['maxRevision'] == 0  # Default value
        assert props['modes'] is None


    def test_validate_new_library_extra_fields_allowed(self, properties_with_extra_fields):
        """Test validate_new_library with extra fields"""
        props = validate_new_library(properties_with_extra_fields)

        assert props['name'] == properties_with_extra_fields['name']
        assert props['customField'] == properties_with_extra_fields['customField']
        assert props['anotherExtra'] == properties_with_extra_fields['anotherExtra']
