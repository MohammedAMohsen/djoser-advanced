from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    Global renderer that wraps all successful API responses.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context["response"]
        # Don't wrap empty responses (204 No Content)
        if response.status_code == 204:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )
        # Don't wrap errors.
        # They will be handled by the global exception handler.
        if response.status_code >= 400:
            return super().render(
                data,
                accepted_media_type,
                renderer_context,
            )
        wrapped = {
            "success": True,
            "message": "Request completed successfully.",
            "data": data,
        }
        return super().render(
            wrapped,
            accepted_media_type,
            renderer_context,
        )