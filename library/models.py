from django.db import models

class Book(models.Model):
    """
    Represents a book in the library.

    Fields:
    - title: Title of the book.
    - author: Author of the book.
    - available: Whether the book is available for borrowing.
    - borrow_count: Number of times the book has been borrowed.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    borrow_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrower(models.Model):
    """
    Represents a borrower in the library.

    Fields:
    - name: Name of the borrower.
    - is_active: Whether the borrower is active.
    """
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    """
    Tracks the borrowing and returning of books.

    Fields:
    - borrower: The borrower of the book.
    - book: The book being borrowed.
    - borrowed_at: The date the book was borrowed.
    - returned_at: The date the book was returned (if any).
    - is_returned: Whether the book has been returned.
    """
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.name}"
