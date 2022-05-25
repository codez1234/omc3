from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps(
                {'status': "error", "message": data})
            #  data.get("non_field_errors")[0]
        else:
            response = json.dumps(data)

        return response
