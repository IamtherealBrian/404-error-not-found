import pytest
import data.text as txt

def test_create_text():
    new_key = 'NewPage'
    title = 'New Page Title'
    text_content = 'This is the content for the new page.'

    created_text = txt.create_text(new_key, title, text_content)

    assert new_key in txt.text_dict
    assert txt.text_dict[new_key][txt.TITLE] == title
    assert txt.text_dict[new_key][txt.TEXT] == text_content

def test_create_duplicate_text():
    duplicate_key = txt.TEST_KEY
    title = 'Duplicate Title'
    text_content = 'This should raise an error.'

    with pytest.raises(ValueError) as exc_info:
        txt.create_text(duplicate_key, title, text_content)

    assert str(exc_info.value) == f'Text with key "{duplicate_key}" already exists.'
