import pytest
from pydantic import ValidationError
from scripts.parse_and_validate_properties_txt import PropertiesBase


# Test Cases
class TestPropertiesBase:

    def test_valid_complete_data(self, valid_properties_data):
        """Test creation with all valid fields"""
        props = PropertiesBase(**valid_properties_data)

        assert props.name == valid_properties_data['name']
        assert props.authors == valid_properties_data['authors']
        assert props.url == valid_properties_data['url']
        assert props.categories == valid_properties_data['categories']
        assert props.sentence == valid_properties_data['sentence']
        assert props.paragraph == valid_properties_data['paragraph']
        assert props.version == int(valid_properties_data['version'])
        assert props.prettyVersion == valid_properties_data['prettyVersion']
        assert props.minRevision == int(valid_properties_data['minRevision'])
        assert props.maxRevision == int(valid_properties_data['maxRevision'])
        assert props.modes == valid_properties_data['modes']


    def test_valid_complete_data_aliases(self, valid_properties_data_aliases):
        """Test creation with all valid fields"""
        props = PropertiesBase(**valid_properties_data_aliases)

        assert props.name == valid_properties_data_aliases['name']
        assert props.authors == valid_properties_data_aliases['authorList']
        assert props.url == valid_properties_data_aliases['url']
        assert props.categories == valid_properties_data_aliases['category']
        assert props.sentence == valid_properties_data_aliases['sentence']
        assert props.paragraph == valid_properties_data_aliases['paragraph']
        assert props.version == int(valid_properties_data_aliases['version'])
        assert props.prettyVersion == valid_properties_data_aliases['prettyVersion']
        assert props.minRevision == int(valid_properties_data_aliases['minRevision'])
        assert props.maxRevision == int(valid_properties_data_aliases['maxRevision'])
        assert props.modes == valid_properties_data_aliases['compatibleModesList']


    def test_minimal_required_data(self, minimal_properties_base_data):
        """Test creation with only required fields"""
        props = PropertiesBase(**minimal_properties_base_data)

        assert props.name == minimal_properties_base_data['name']
        assert props.authors == minimal_properties_base_data['authors']
        assert props.url == minimal_properties_base_data['url']
        assert props.categories is None
        assert props.sentence == minimal_properties_base_data['sentence']
        assert props.paragraph is None
        assert props.version == int(minimal_properties_base_data['version'])
        assert props.prettyVersion == minimal_properties_base_data['prettyVersion']
        assert props.minRevision == 0  # Default value
        assert props.maxRevision == 0  # Default value
        assert props.modes is None


    def test_minimal_required_data_aliases(self, minimal_properties_base_data_aliases):
        """Test creation with only required fields"""
        props = PropertiesBase(**minimal_properties_base_data_aliases)

        assert props.name == minimal_properties_base_data_aliases['name']
        assert props.authors == minimal_properties_base_data_aliases['authorList']
        assert props.url == minimal_properties_base_data_aliases['url']
        assert props.categories is None
        assert props.sentence == minimal_properties_base_data_aliases['sentence']
        assert props.paragraph is None
        assert props.version == int(minimal_properties_base_data_aliases['version'])
        assert props.prettyVersion == minimal_properties_base_data_aliases['prettyVersion']
        assert props.minRevision == 0  # Default value
        assert props.maxRevision == 0  # Default value
        assert props.modes is None


    def test_extra_fields_allowed(self, properties_with_extra_fields):
        """Test that extra fields are allowed due to extra='allow'"""
        props = PropertiesBase(**properties_with_extra_fields)

        assert props.name == properties_with_extra_fields['name']
        assert props.customField == properties_with_extra_fields['customField']
        assert props.anotherExtra == properties_with_extra_fields['anotherExtra']


    def test_missing_required_field_name(self, minimal_properties_base_data):
        """Test validation error when required field 'name' is missing"""
        minimal_properties_base_data.pop("name")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "name" in str(exc_info.value)
        assert "Field required" in str(exc_info.value)


    def test_missing_required_field_authors(self, minimal_properties_base_data):
        """Test validation error when required field 'authors' is missing"""
        minimal_properties_base_data.pop("authors")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "authors" in str(exc_info.value)


    def test_missing_required_field_url(self, minimal_properties_base_data):
        """Test validation error when required field 'url' is missing"""
        minimal_properties_base_data.pop("url")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "url" in str(exc_info.value)


    def test_missing_required_field_sentence(self, minimal_properties_base_data):
        """Test validation error when required field 'sentence' is missing"""
        minimal_properties_base_data.pop("sentence")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "sentence" in str(exc_info.value)


    def test_missing_required_field_version(self, minimal_properties_base_data):
        """Test validation error when required field 'version' is missing"""
        minimal_properties_base_data.pop("version")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "version" in str(exc_info.value)


    def test_missing_required_field_pretty_version(self, minimal_properties_base_data):
        """Test validation error when required field 'prettyVersion' is missing"""
        minimal_properties_base_data.pop("prettyVersion")

        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "prettyVersion" in str(exc_info.value)


    def test_invalid_type_version(self, minimal_properties_base_data):
        """Test validation error when 'version' has wrong type"""
        minimal_properties_base_data["version"] = "not_an_int"
        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "version" in str(exc_info.value)
        assert "Input should be a valid integer" in str(exc_info.value)


    def test_invalid_type_min_revision(self, minimal_properties_base_data):
        """Test validation error when 'minRevision' has wrong type"""
        minimal_properties_base_data["minRevision"] = "not_an_int"
        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "minRevision" in str(exc_info.value)
        assert "Input should be a valid integer" in str(exc_info.value)


    def test_invalid_type_max_revision(self, minimal_properties_base_data):
        """Test validation error when 'maxRevision' has wrong type"""
        minimal_properties_base_data["maxRevision"] = "not_an_int"
        with pytest.raises(ValidationError) as exc_info:
            PropertiesBase(**minimal_properties_base_data)

        assert "maxRevision" in str(exc_info.value)
        assert "Input should be a valid integer" in str(exc_info.value)


    def test_model_dump(self, valid_properties_data):
        """Test that model serialization works correctly"""
        props = PropertiesBase(**valid_properties_data)
        dumped = props.model_dump()

        assert dumped["name"] == "Test Library"
        assert dumped["modes"] == "standard,debug"
        assert "compatibleModesList" not in dumped  # Should use field name, not alias


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
