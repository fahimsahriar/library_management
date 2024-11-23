
# Library Management System API

This is a Django-based backend project that manages a library system. It includes role-based access control with two user roles: Admin and Member.

Admins:
- Perform CRUD operations on books.
- View a list of all members and their borrowing history.
- Ban/unban members.
Members:
- Borrow and return books.
- View their borrowed books, total fines, and credit balance.


## Features
### Role-Based Access Control

- Admin: Full access to manage books and users.
- Member: Limited access to borrow and return books.

### Borrowing and Returning Books
- Members can borrow up to 5 books at a time.
- A 14-day borrowing deadline is enforced.
- Fine of 5 BDT/day is applied for overdue books.

### User Management
- Members start with a default credit of 200 BDT.
- Fines are automatically deducted from the user’s credit.
- If credit is exhausted, the user is automatically banned until unbanned by an admin.


## Installation

### Prerequisites
1. Python 3.8+
2. Django 5+
3. Django Rest Framework

### Steps
1. Clone the repository:
```bash
  git clone https://github.com/fahimsahriar/library_management  
  cd library_management  
```
2. Create a virtual environment:
```bash
  python -m venv venv  
  source venv/bin/activate  # On Windows: venv\Scripts\activate  
```
3. Install dependencies:
```bash
  pip install -r requirements.txt    
```
4. Apply migrations:
```bash
  python manage.py makemigrations  
  python manage.py migrate     
```
5. Create a superuser (Admin/Super User):
```bash
  python manage.py createsuperuser      
```
6. Run the development server:
```bash
  python manage.py runserver       
```

## Additional Notes
### File Structure
```text
library_management /  
├── library/  # Project settings  
├── management/         # App for book and borrowing management  
├── users/              # App for user authentication and roles  
├── venv/               # Virtual environment  
├── db.sqlite3          # SQLite database  
├── requirements.txt    # Dependencies  
└── manage.py           # Django management script  
```

    
## API Reference

#### Authentication
- Login (Obtain Token)\
  POST ```/api/users/login/```\
  Request Body:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
  Response:
  ```json
  {
      "access": "your_access_token",
      "refresh": "your_refresh_token"
  }
  ```

### Books
- List All Books\
  GET ```/api/management/books/```

- Create a New Book (Admin Only)\
  POST ```/api/management/books/```\
  Request Body:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "is_available": true
  }
  ```
- Retrieve Book Details\
  GET ```/api/management/books/<int:pk>/```

- Update Book (Admin Only)\
  POST ```/api/management/books/<int:pk>/```\
  Request Body:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "is_available": true
  }
  ```

- Delete Book (Admin Only)\
  DELETE ```/api/management/books/<int:pk>/```

### Borrow & Return
- Borrow a Book (Member Only)\
  POST ```/api/management/borrow/```\
  Request Body:
  ```json
  {
    "book": 1  # ID of the book to borrow
  }
  ```
- Return a Book (Member Only)\
  PUT ```/api/management/return/<int:pk>/```\
  Replace <int:pk> with the Borrow ID.
- View All Borrowed Books (Admin Only)\
  GET ```/api/management/all-borrowed-list/```

### Users
- List All Members (Admin Only)\
  GET ```/api/users/members/```

- View Member Details (Admin Only)\
  GET ```/api/users/members/<int:pk>/```\
  Includes user's borrowing history and current borrowed books.

- Unban a User (Admin Only)\
  PUT ```/api/users/unban/<int:pk>/```\
  No request body is required.

### Feel free to contribute and improve this project!



