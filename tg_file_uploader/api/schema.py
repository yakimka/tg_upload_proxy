from marshmallow import Schema, fields, validate

from tg_file_uploader.api.fields import FileOrString


class SendAudio(Schema):
    chat_id = fields.Int(required=True)
    audio = FileOrString(required=True)
    caption = fields.Str(validate=validate.Length(min=0, max=1024))
    parse_mode = fields.Str()
    duration = fields.Int(strict=True, missing=0)
    performer = fields.Str(missing=None)
    title = fields.Str(missing=None)
    thumb = FileOrString(missing=None)
    reply_to_message_id = fields.Int(strict=True, missing=None)
    # TODO: not used for now
    disable_notification = fields.Boolean()
    reply_markup = fields.Str()


class SendAudioResponse(Schema):
    file_id = fields.Str(required=True)
