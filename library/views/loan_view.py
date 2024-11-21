from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Loan
import logging

# Setting up logger
logger = logging.getLogger(__name__)

class ReturnAPIView(APIView):
    """
    View for returning a borrowed book.
    Marks the book as returned and updates availability.
    """

    def post(self, request):
        """
        Return a borrowed book by book_id.

        Validates if there is an active loan for the book and updates 
        the loan and book status accordingly.

        Returns:
            Response: Success or error message.
        """
        book_id = request.data.get('book_id')

        try:
            loan = Loan.objects.get(book_id=book_id, is_returned=False)
        except Loan.DoesNotExist:
            logger.error(f"No active loan found for book with id {book_id}.")
            return Response({"error": "No active loan found for the given book."}, status=status.HTTP_404_NOT_FOUND)

        # Mark the loan as returned and set the return date
        loan.is_returned = True
        loan.returned_at = timezone.now()
        loan.save()

        # Update the book availability
        book = loan.book
        book.available = True
        book.save()

        logger.info(f"Book with id {book_id} returned successfully.")
        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
