import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Book, Borrower, Loan
from ..serializers import BookSerializer, LoanSerializer

# Setting up logger
logger = logging.getLogger(__name__)

class BookListCreateAPIView(APIView):
    """
    View to list available books and create new books.
    """

    def get(self, request):
        """
        List available books.

        Filters books by availability (available=True).

        Returns:
            Response: List of available books or error message.
        """
        try:
            books = Book.objects.filter(available=True)
            serializer = BookSerializer(books, many=True)
            logger.info(f"Retrieved {len(books)} available books.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving books: {str(e)}")
            return Response({'detail': 'Error retrieving books.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new book.

        Returns:
            Response: Serialized book data or validation errors.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                logger.info(f"Book '{serializer.validated_data.get('title')}' created.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating book: {str(e)}")
                return Response({'detail': 'Error creating the book.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Failed to create book: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
