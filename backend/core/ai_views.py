from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ai_service import generate_ai_response

class AIChatView(APIView):
    """
    Public endpoint for Coco Hotel AI Virtual Concierge chat.
    Accepts: { "message": "...", "history": [...] }
    Returns: { "reply": "..." }
    """
    permission_classes = []

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        history = request.data.get('history', [])

        if not user_message:
            return Response(
                {'error': 'Message field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reply = generate_ai_response(user_message, history=history)
        return Response({'reply': reply}, status=status.HTTP_200_OK)
