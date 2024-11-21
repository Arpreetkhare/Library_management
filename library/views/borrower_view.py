import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Book, Borrower, Loan
from ..serializers import BookSerializer, LoanSerializer, BorrowerSerializer
from django.db.models import F

# Setting up logger
logger = logging.getLogger(__name__)

class BorrowAPIView(APIView):
    """
    View for borrowing a book.
    Validates book availability, borrower status, and borrowing limit.
    """

    def post(self, request):
        """
        Borrow a book by book_id and borrower_id.

        Validates if the book is available, if the borrower is active, and if 
        the borrower has not exceeded the borrowing limit of 3 books.
        
        Returns:
            Response: Success or error message.
        """
        book_id = request.data.get('book_id')
        borrower_id = request.data.get('borrower_id')

        try:
            book = Book.objects.get(id=book_id, available=True)
        except Book.DoesNotExist:
            logger.error(f"Book with id {book_id} is unavailable or already borrowed.")
            return Response({"error": "Book is unavailable or already borrowed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrower = Borrower.objects.get(id=borrower_id)
        except Borrower.DoesNotExist:
            logger.error(f"Borrower with id {borrower_id} not found.")
            return Response({"error": "Borrower not found."}, status=status.HTTP_404_NOT_FOUND)

        if not borrower.is_active:
            logger.error(f"Borrower {borrower_id} has an inactive membership.")
            return Response({"error": "Borrower's membership is inactive."}, status=status.HTTP_400_BAD_REQUEST)

        active_loans_count = Loan.objects.filter(borrower=borrower, is_returned=False).count()
        if active_loans_count >= 3:
            logger.error(f"Borrower {borrower_id} has reached the borrowing limit of 3 books.")
            return Response({"error": "Borrower has reached the borrowing limit of 3 books."}, status=status.HTTP_400_BAD_REQUEST)

        # Create loan and update book availability
        Loan.objects.create(borrower=borrower, book=book)
        book.available = False
        book.borrow_count = F('borrow_count') + 1
        book.save()

        logger.info(f"Book with id {book_id} borrowed successfully by borrower {borrower_id}.")
        return Response({"message": "Book borrowed successfully."}, status=status.HTTP_200_OK)


class BorrowedBooksAPIView(APIView):
    """
    View to list all active borrowed books of a borrower.
    """

    def get(self, request, borrower_id):
        """
        List all currently borrowed (unreturned) books for the borrower.
        
        Returns:
            Response: A list of borrowed books.
        """
        loans = Loan.objects.filter(borrower_id=borrower_id, is_returned=False).select_related('book')
        borrowed_books = [{"book_id": loan.book.id, "title": loan.book.title} for loan in loans]
        
        logger.info(f"Listed {len(borrowed_books)} borrowed books for borrower {borrower_id}.")
        return Response(borrowed_books, status=status.HTTP_200_OK)


class BorrowerHistoryAPIView(APIView):
    """
    View to list the entire borrowing history for a borrower.
    """

    def get(self, request, borrower_id):
        """
        List all books ever borrowed by the borrower, including return status.
        
        Returns:
            Response: A list of all borrowed books with their return status.
        """
        loans = Loan.objects.filter(borrower_id=borrower_id).select_related('book')
        history = [
            {
                "book_id": loan.book.id,
                "title": loan.book.title,
                "borrowed_at": loan.borrowed_at,
                "returned_at": loan.returned_at,
                "is_returned": loan.is_returned,
            }
            for loan in loans
        ]

        logger.info(f"Listed borrowing history for borrower {borrower_id}. Total {len(history)} entries.")
        return Response(history, status=status.HTTP_200_OK)
