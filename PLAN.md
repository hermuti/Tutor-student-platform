# Detailed Plan for Online School Website Development

This document outlines the detailed plan for developing the online school website with Admin, Tutor, and Student roles, including user dashboards, login, basic information submission, and initial tutor verification.

**Technology Stack:**

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django (Python)
- **Database:** MySQL Workbench 8.0

---

### Phase 1: Project Initialization & Core Setup

- **Goal 1: Initialize Django Project and App Structure**
  - Create a new Django project (e.g., `online_school`).
  - Create a new Django app (e.g., `users`) to manage user authentication and profiles.
  - Configure `settings.py` to include the new app and set up static/media files.
- **Goal 2: Set up MySQL Database Connection**
  - Ensure MySQL Workbench 8.0 is running and a database is created for the project.
  - Configure `settings.py` to connect Django to the MySQL database.
  - Run initial Django migrations to create necessary database tables.

### Phase 2: User Management & Authentication

- **Goal 3: Define Custom User Models**
  - Create a custom `User` model by extending Django's `AbstractUser`. This model will include common fields such as `user_id` (auto-generated or custom), `phone_no`, `gender`, `status` (e.g., 'active', 'inactive', 'pending_verification'), `profile_pic`, and `created_at`.
  - Create `AdminProfile`, `TutorProfile`, and `StudentProfile` models. Each will have a `OneToOneField` relationship with the custom `User` model.
  - The `TutorProfile` model will include additional fields for documents (e.g., `document_url1`, `document_url2`) and a `is_verified` boolean field (defaulting to `False`).
- **Goal 4: Implement User Registration and Login**
  - Develop Django forms (`UserCreationForm`, `AuthenticationForm`) for user registration (signup) and login.
  - Create Django views (`register_view`, `login_view`) to handle user registration and authentication logic.
  - Design basic HTML templates for the registration and login pages, allowing users to input their basic information.
  - Upon successful registration, create the corresponding `AdminProfile`, `TutorProfile`, or `StudentProfile` based on the user type selected during signup.
- **Goal 5: Basic Information Submission on Login/Registration**
  - Ensure the registration forms collect all specified basic information: `userid`, `username`, `first_name`, `last_name`, `email`, `password`, `phone_no`, `gender`, `status`, `profile_pic`, `created_at`.
  - For tutors, the registration process will also include fields for submitting additional documents, which will be stored and marked as pending verification.

### Phase 3: Dashboard Creation & Initial Features

- **Goal 6: Create User Dashboards (HTML/CSS/JS)**
  - Develop a base HTML template (`base_dashboard.html`) for a consistent dashboard layout, including navigation and common elements.
  - Create separate HTML templates for `admin_dashboard.html`, `tutor_dashboard.html`, and `student_dashboard.html`.
  - Implement basic CSS for styling the dashboards and simple JavaScript for any client-side interactions (e.g., dynamic content loading, form validation).
  - Each dashboard will initially display the logged-in user's basic profile information.
- **Goal 7: Implement Admin Dashboard Features (Initial)**
  - Create a Django view (`admin_dashboard_view`) to render the Admin dashboard.
  - Display initial counts of registered tutors, students, and available courses (these will be placeholder values initially, later populated from the database).
  - Add a prominent link or section on the Admin dashboard to "Verify Tutors".
- **Goal 8: Implement Tutor Verification Workflow (Initial)**
  - Create a Django view (`tutor_verification_view`) accessible only by Admins. This view will list all tutors whose `is_verified` status is `False`.
  - For each unverified tutor, display their submitted basic information and links to their uploaded documents.
  - Implement actions (e.g., buttons) for the Admin to "Accept" or "Deny" a tutor's verification. Accepting will set `is_verified` to `True` for the `TutorProfile`, while denying might update their `status` to 'rejected' or similar.
- **Goal 9: Implement Student Dashboard Features (Initial)**
  - Create a Django view (`student_dashboard_view`) to render the Student dashboard.
  - Initially, this dashboard will contain placeholder sections or links for actions like "Book Session", "Search Course", "View Attendance", etc.
- **Goal 10: Implement Tutor Dashboard Features (Initial)**
  - Create a Django view (`tutor_dashboard_view`) to render the Tutor dashboard.
  - Crucially, this view will check the `is_verified` status of the logged-in tutor. If `False`, it will display a message indicating that their account is pending admin verification and restrict access to full dashboard features.
  - If `True`, it will display placeholder sections or links for actions like "Conduct Session", "View Profile", "Upload Material", etc.

---

### Workflow Diagram

```mermaid
graph TD
    A[Start] --> B{Project Setup};
    B --> C[Configure Django & MySQL];
    C --> D[Define Custom User Model];
    D --> E[Create Profile Models (Admin, Tutor, Student)];
    E --> F[Implement Registration & Login Forms/Views];
    F --> G[User Registers/Logs In];
    G --> H{User Type?};
    H -- Admin --> I[Admin Dashboard];
    H -- Tutor --> J{Tutor Verified?};
    H -- Student --> K[Student Dashboard];
    I --> L[View Tutors for Verification];
    L --> M[Verify/Deny Tutor];
    J -- Yes --> N[Access Tutor Dashboard Features];
    J -- No --> O[Display Pending Verification Message];
    K --> P[Access Student Dashboard Features];
    N --> Q[End (Phase 1 Complete)];
    P --> Q;
    M --> Q;
    O --> Q;
```
