import io
import os

from aiohttp.web_request import FileField
from marshmallow import ValidationError, fields


class FileOrString(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            if os.path.exists(value):
                raise ValidationError('Invalid input type')
            return value

        if not isinstance(value, FileField):
            raise ValidationError('Invalid input type')

        file_ = io.BytesIO(value.file.read())
        file_.name = value.filename
        return file_
