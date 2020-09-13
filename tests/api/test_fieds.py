import io
from unittest.mock import MagicMock

import pytest
from aiohttp.web_request import FileField
from marshmallow import ValidationError

from tg_file_uploader.api.fields import FileOrString


class TestFileOrString:
    def test__deserialize_has_file_in_system(self):
        with pytest.raises(ValidationError, match='Invalid input type'):
            FileOrString()._deserialize(__file__, '', {})

    def test__deserialize_string_value(self):
        value = FileOrString()._deserialize('url_or_path', '', {})

        assert 'url_or_path' == value

    def test__deserialize_not_file_type(self):
        with pytest.raises(ValidationError, match='Invalid input type'):
            FileOrString()._deserialize(object(), '', {})

    def test__deserialize_file(self):
        mock_file = MagicMock(spec=FileField)
        mock_file.file = io.BytesIO(b'hello')
        mock_file.filename = 'test file name'

        file_ = FileOrString()._deserialize(mock_file, '', {})

        assert 'test file name' == file_.name
        assert b'hello' == file_.read()
