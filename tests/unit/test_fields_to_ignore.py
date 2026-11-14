"""
Fields like id, dateAdded, source, type etc. are set by our scripts, not by the
contributor. If they appear in a properties file, they must be dropped before
validation so they never reach the database.
"""
import pytest
from scripts.parse_and_validate_properties_txt import (
    PropertiesBase, PropertiesExisting, LibraryPropertiesNew,
    validate_new, validate_existing, validate_new_library,
)

IGNORED_FIELDS = ['id', 'download', 'dateAdded', 'lastUpdated', 'status', 'source', 'type']


class TestFieldsToIgnore:

    @pytest.mark.parametrize("model", [PropertiesBase, PropertiesExisting, LibraryPropertiesNew])
    @pytest.mark.parametrize("field", IGNORED_FIELDS)
    def test_model_drops_ignored_field(self, model, field, properties_with_fields_to_ignore):
        props = model.model_validate(properties_with_fields_to_ignore)

        assert field not in props.model_dump()
        assert field not in (props.model_extra or {})

    @pytest.mark.parametrize("validate", [validate_new, validate_existing, validate_new_library])
    @pytest.mark.parametrize("field", IGNORED_FIELDS)
    def test_validate_drops_ignored_field(self, validate, field, properties_with_fields_to_ignore):
        props = validate(properties_with_fields_to_ignore)

        assert field not in props

    @pytest.mark.parametrize("validate", [validate_new, validate_existing, validate_new_library])
    def test_validate_keeps_other_fields(self, validate, properties_with_fields_to_ignore):
        props = validate(properties_with_fields_to_ignore)

        assert props['name'] == properties_with_fields_to_ignore['name']
        assert props['authors'] == properties_with_fields_to_ignore['authors']
        assert props['categories'] == properties_with_fields_to_ignore['categories']

    def test_ignored_fields_do_not_overwrite_type_and_source(self, properties_with_fields_to_ignore):
        """Mirrors __main__ in parse_and_validate_properties_txt.py: type and source come
        from the issue form, and must not be overwritten by values in the properties file."""
        contribution = {
            "type": "library",
            "source": "https://correct.com/library.txt",
        }
        contribution.update(validate_new_library(properties_with_fields_to_ignore))

        assert contribution['type'] == 'library'
        assert contribution['source'] == 'https://correct.com/library.txt'
        assert 'download' not in contribution
        assert 'id' not in contribution
