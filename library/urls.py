from django.urls import path

from .views import BookListCreateAPIView, BorrowAPIView, BorrowedBooksAPIView, BorrowerHistoryAPIView, ReturnAPIView

urlpatterns = [
    # Book Management
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),

    # Borrowing and Returning
    path('borrow/', BorrowAPIView.as_view(), name='borrow-book'),
    path('return/', ReturnAPIView.as_view(), name='return-book'),

    # Borrowed Books and Borrower History
    path('borrowed/<int:borrower_id>/', BorrowedBooksAPIView.as_view(), name='borrowed-books'),
    path('history/<int:borrower_id>/', BorrowerHistoryAPIView.as_view(), name='borrower-history'),
]
