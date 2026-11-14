import pytest
from scripts.add_new_contribution_to_yaml import postprocess_properties


@pytest.fixture
def new_contribution_props():
    """What parse_and_validate_properties_txt.py outputs, plus fields the database sets."""
    return {
        "type": "library",
        "source": "https://example.com/releases/library.txt",
        "name": "Test Library",
        "authors": "Some Author",
        "url": "https://example.com",
        "categories": "b,a",
        "sentence": "A test library",
        "version": 1,
        "prettyVersion": "1.0",
        "id": 999,
        "dateAdded": "2001-01-01T00:00:00+0000",
        "lastUpdated": "2001-01-01T00:00:00+0000",
        "status": "DEPRECATED",
    }


class TestPostprocessProperties:

    @pytest.mark.parametrize("field", ['id', 'dateAdded', 'lastUpdated', 'status'])
    def test_removes_database_fields(self, field, new_contribution_props):
        postprocess_properties(new_contribution_props)

        assert field not in new_contribution_props

    def test_keeps_type_and_source(self, new_contribution_props):
        postprocess_properties(new_contribution_props)

        assert new_contribution_props['type'] == 'library'
        assert new_contribution_props['source'] == 'https://example.com/releases/library.txt'

    def test_download_derived_from_source(self, new_contribution_props):
        postprocess_properties(new_contribution_props)

        assert new_contribution_props['download'] == 'https://example.com/releases/library.zip'

    def test_categories_split_and_sorted(self, new_contribution_props):
        postprocess_properties(new_contribution_props)

        assert new_contribution_props['categories'] == ['a', 'b']
