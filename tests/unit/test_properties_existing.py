import pytest
from pydantic import ValidationError
from scripts.parse_and_validate_properties_txt import PropertiesExisting


# Test Cases
class TestPropertiesExisting:
    def test_valid_complete_data(self, valid_properties_data):
        """Test creation with all valid fields"""
        props = PropertiesExisting(**valid_properties_data)

        assert props.name == valid_properties_data['name']
        assert props.authors == valid_properties_data['authors']
        assert props.url == valid_properties_data['url']
        assert props.categories == valid_properties_data['categories']
        assert props.sentence == valid_properties_data['sentence']
        assert props.paragraph == valid_properties_data['paragraph']
        assert props.version == valid_properties_data['version']
        assert props.prettyVersion == valid_properties_data['prettyVersion']
        assert props.minRevision == int(valid_properties_data['minRevision'])
        assert props.maxRevision == int(valid_properties_data['maxRevision'])
        assert props.modes == valid_properties_data['modes']


    def test_valid_complete_data_aliases(self, valid_properties_data_aliases):
        """Test creation with all valid fields"""
        props = PropertiesExisting(**valid_properties_data_aliases)

        assert props.name == valid_properties_data_aliases['name']
        assert props.authors == valid_properties_data_aliases['authorList']
        assert props.url == valid_properties_data_aliases['url']
        assert props.categories == valid_properties_data_aliases['category']
        assert props.sentence == valid_properties_data_aliases['sentence']
        assert props.paragraph == valid_properties_data_aliases['paragraph']
        assert props.version == valid_properties_data_aliases['version']
        assert props.prettyVersion == valid_properties_data_aliases['prettyVersion']
        assert props.minRevision == int(valid_properties_data_aliases['minRevision'])
        assert props.maxRevision == int(valid_properties_data_aliases['maxRevision'])
        assert props.modes == valid_properties_data_aliases['compatibleModesList']


    def test_minimal_required_data(self, minimal_properties_existing_data):
        """Test creation with only required fields"""
        props = PropertiesExisting(**minimal_properties_existing_data)

        assert props.name == minimal_properties_existing_data['name']
        assert props.authors == minimal_properties_existing_data['authors']
        assert props.url == minimal_properties_existing_data['url']
        assert props.categories is None
        assert props.sentence == minimal_properties_existing_data['sentence']
        assert props.paragraph is None
        assert props.version == minimal_properties_existing_data['version']
        assert props.prettyVersion is None
        assert props.minRevision == 0  # Default value
        assert props.maxRevision == 0  # Default value
        assert props.modes is None


    def test_minimal_required_data_alias(self, minimal_properties_existing_data_aliases):
        """Test creation with only required fields"""
        props = PropertiesExisting(**minimal_properties_existing_data_aliases)

        assert props.name == minimal_properties_existing_data_aliases['name']
        assert props.authors == minimal_properties_existing_data_aliases['authorList']
        assert props.url == minimal_properties_existing_data_aliases['url']
        assert props.categories is None
        assert props.sentence == minimal_properties_existing_data_aliases['sentence']
        assert props.paragraph is None
        assert props.version == minimal_properties_existing_data_aliases['version']
        assert props.prettyVersion is None
        assert props.minRevision == 0  # Default value
        assert props.maxRevision == 0  # Default value
        assert props.modes is None


    def test_extra_fields_allowed(self, properties_with_extra_fields):
        """Test that extra fields are allowed due to extra='allow'"""
        props = PropertiesExisting(**properties_with_extra_fields)

        assert props.name == properties_with_extra_fields['name']
        assert props.customField == properties_with_extra_fields['customField']
        assert props.anotherExtra == properties_with_extra_fields['anotherExtra']


    def test_missing_required_field_name(self, minimal_properties_existing_data):
        """Test validation error when required field 'name' is missing"""
        minimal_properties_existing_data.pop("name")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesExisting(**minimal_properties_existing_data)

        assert "name" in str(exc_info.value)
        assert "Field required" in str(exc_info.value)


    def test_missing_required_field_authors(self, minimal_properties_existing_data):
        """Test validation error when required field 'authors' is missing"""
        minimal_properties_existing_data.pop("authors")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesExisting(**minimal_properties_existing_data)

        assert "authors" in str(exc_info.value)


    def test_missing_required_field_url(self, minimal_properties_existing_data):
        """Test validation error when required field 'url' is missing"""
        minimal_properties_existing_data.pop("url")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesExisting(**minimal_properties_existing_data)

        assert "url" in str(exc_info.value)


    def test_missing_required_field_sentence(self, minimal_properties_existing_data):
        """Test validation error when required field 'sentence' is missing"""
        minimal_properties_existing_data.pop("sentence")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesExisting(**minimal_properties_existing_data)

        assert "sentence" in str(exc_info.value)


    def test_missing_required_field_version(self, minimal_properties_existing_data):
        """Test validation error when required field 'version' is missing"""
        minimal_properties_existing_data.pop("version")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesExisting(**minimal_properties_existing_data)

        assert "version" in str(exc_info.value)


    def test_string_type_version(self, minimal_properties_existing_data):
        """Test validation when 'version' is string"""
        minimal_properties_existing_data["version"] = "not_an_int"
        props = PropertiesExisting(**minimal_properties_existing_data)
        assert props.version == minimal_properties_existing_data['version']


    def test_string_type_min_revision(self, minimal_properties_existing_data):
        """Test when 'minRevision' string defaults to 0"""
        minimal_properties_existing_data["minRevision"] = "not_an_int"
        props =PropertiesExisting(**minimal_properties_existing_data)
        assert props.minRevision == 0


    def test_string_type_max_revision(self, minimal_properties_existing_data):
        """Test when 'maxRevision' string defaults to 0"""
        minimal_properties_existing_data["maxRevision"] = "not_an_int"
        props =PropertiesExisting(**minimal_properties_existing_data)
        assert props.maxRevision == 0


    def test_model_dump(self, valid_properties_data):
        """Test that model serialization works correctly"""
        props = PropertiesExisting(**valid_properties_data)
        dumped = props.model_dump()

        assert dumped["name"] == "Test Library"
        assert dumped["modes"] == "standard,debug"
        assert "compatibleModesList" not in dumped  # Should use field name, not alias



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
