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

---

### Phase 2: User Authentication and Core Models

This phase focuses on establishing the foundational user management system and defining the core data models required for the platform's functionalities.

- **Goal 1: Define Custom User Model with UUID, Role-Based IDs, and Detailed Profiles**

  - **Description:** Create a custom Django `User` model with common user attributes and a universally unique identifier (UUID). Implement separate profile models for `Student`, `Tutor`, and `Admin` to store role-specific information, including a structured approach for tutors to submit required documents and an `is_verified` status for admin approval. We will also implement a mechanism for generating role-based IDs.

  - **Explanation: `AbstractUser` vs. `CustomUser`**

    - **`AbstractUser`**: This is Django's built-in abstract base class for user models. It provides the core user functionalities like `username`, `password`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `is_superuser`, and `date_joined`. It's designed to be extended.
    - **`CustomUser`**: When you need to add custom fields or modify the behavior of Django's default user model (e.g., adding `phone`, `gender`, `role`), you should inherit from `AbstractUser` (or `AbstractBaseUser` for more advanced customization). By creating a `CustomUser` model and setting `AUTH_USER_MODEL` in `settings.py`, you tell Django to use your custom model instead of its default `User` model. This allows you to tailor the user model to your application's specific needs without modifying Django's core code.

  - **Explanation: Data Types and Validation**

    - **`first_name`, `last_name`**: These will be `CharField`s. Django's forms and model fields provide basic validation (e.g., `max_length`). For stricter validation (e.g., allowing only alphabetic characters), we will implement custom validators in Django forms during the registration/profile management phase.
    - **`email`**: This will be an `EmailField`. Django's `EmailField` automatically validates that the input is a valid email address format (e.g., `user@example.com`).
    - **`phone`**: This will be a `CharField`. To ensure only numbers are entered, we will use a `RegexValidator` in the corresponding Django form.
    - **Other fields**: Similar validation strategies will be applied using Django's form system to ensure data integrity.

  - **Explanation: Role-Based IDs (e.g., S-001, T-005, A-003)**

    - Django's default `User` model (which `CustomUser` inherits from) automatically provides an auto-incrementing integer `id` as its primary key. We will add a `uuid` field to `CustomUser` for a universally unique identifier.
    - For role-based IDs like `S-001`, `T-005`, `A-003`, we can implement a method within the `CustomUser` model or its associated profile models that generates these IDs dynamically based on the user's role and their `id` or `uuid`. For example, a `get_role_id()` method could return `'S-' + str(self.id).zfill(3)` for students. This approach keeps the primary key simple while providing the desired display format.

  - **Steps:**

    1.  Modify `users/models.py` to define the `CustomUser` model inheriting from `AbstractUser`.
    2.  Add a `uuid` field to `CustomUser`: `uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)`. (Requires importing `uuid`).
    3.  Add common user fields to `CustomUser`: `phone` (CharField), `gender` (CharField with choices, e.g., 'Male', 'Female', 'Other'), `address` (CharField), `profile_pic` (ImageField).
    4.  Implement a `role` field (e.g., `CharField` with choices: 'Student', 'Tutor', 'Admin').
    5.  Create a `StudentProfile` model with `OneToOneField` to `CustomUser`, including `preferred_learning_mode` (CharField) and `education_level` (CharField).
    6.  Create a `TutorProfile` model with `OneToOneField` to `CustomUser`. Add fields:
        - `is_verified` (BooleanField, default `False`) - for admin verification.
        - `cv` (FileField)
        - `resume` (FileField)
        - `proof_of_identity` (FileField)
        - `personal_statement_or_teaching_philosophy` (TextField)
    7.  Create a `TutorEducation` model with `ForeignKey` to `TutorProfile`. This model will store educational documents. - Fields: `document_type` (CharField with choices: 'High School Diploma', 'College Degree', 'Masters', 'PhD'), `file` (FileField).
        <!-- 8.  Create a `TutorRecommendation` model with `ForeignKey` to `TutorProfile`. This model will store recommendation letters. skiped not needed-->
            - Fields: `file` (FileField), `description` (TextField, optional).
    8.  Create a `TutorCertification` model with `ForeignKey` to `TutorProfile`. This model will store optional subject-specific certifications.
        - Fields: `name` (CharField), `file` (FileField, optional).
    9.  Create an `AdminProfile` model with `OneToOneField` to `CustomUser`. (Initially, this might be empty or contain specific admin-related fields if needed later).
    10. Update `settings.py` to point `AUTH_USER_MODEL` to `users.CustomUser`.
    11. Run `makemigrations` and `migrate` to apply database changes.

  - **Tutor Registration Workflow Note:** The `is_verified` field in `TutorProfile` will be crucial for the tutor registration workflow. Upon initial registration, a tutor's `is_verified` status will be `False`. Admin will then review submitted documents and update this status. Email notifications ("your profile is pending", "welcome to our online school", "unfortunately you have not fulfilled the requirements") will be implemented as part of the user registration/login and admin dashboard features (Goals 2 and Phase 5).

  - **Mermaid Diagram: User and Profile Models (Detailed)**

    ```mermaid
    classDiagram
        class AbstractUser {
            +id: AutoField (PK)
            +username
            +password
            +email
            +first_name
            +last_name
            +is_staff
            +is_active
            +date_joined
        }
        class CustomUser {
            +id: AutoField (PK)
            +uuid: UUIDField (Unique)
            +role: CharField (Student, Tutor, Admin)
            +phone: CharField
            +gender: CharField
            +address: CharField
            +profile_pic: ImageField
        }
        class StudentProfile {
            +preferred_learning_mode: CharField
            +education_level: CharField
        }
        class TutorProfile {
            +is_verified: BooleanField
            +cv: FileField
            +resume: FileField
            +proof_of_identity: FileField
            +personal_statement_or_teaching_philosophy: TextField
        }
        class TutorEducation {
            +document_type: CharField (Diploma, Degree, Masters, PhD)
            +file: FileField
        }
        class TutorRecommendation {
            +file: FileField
            +description: TextField
        }
        class TutorCertification {
            +name: CharField
            +file: FileField
        }
        class AdminProfile {
            -- No specific fields yet --
        }

        AbstractUser <|-- CustomUser : inherits
        CustomUser "1" -- "0..1" StudentProfile : has
        CustomUser "1" -- "0..1" TutorProfile : has
        CustomUser "1" -- "0..1" AdminProfile : has
        TutorProfile "1" -- "*" TutorEducation : has
        TutorProfile "1" -- "*" TutorRecommendation : has
        TutorProfile "1" -- "*" TutorCertification : has
    ```

- **Goal 2: Implement User Registration and Login**

  - **Description:** Develop views and templates for user registration (signup) and login, ensuring users are assigned the correct role upon registration. This will also include initial validation for user input.
  - **Steps:**
    1.  Create `users/forms.py` for `UserRegistrationForm` (including validation for `email`, `phone`, etc.) and `AuthenticationForm`.
    2.  Create `users/views.py` for `register_view` and `login_view`.
    3.  Create `users/urls.py` to define URL patterns for registration and login.
    4.  Include `users.urls` in the main `online_school/urls.py`.
    5.  Create basic HTML templates for `register.html` and `login.html`.
    6.  Implement role assignment logic during registration, and for tutors, set `is_verified` to `False` initially.
    7.  Implement basic email notification for tutor registration ("your profile is pending").
  - **Mermaid Diagram: Authentication Flow**
    ```mermaid
    graph TD
        A[User] --> B{Access Registration/Login Page};
        B -- Registration --> C[RegisterForm (with validation)];
        C -- Submit --> D{RegisterView};
        D -- Tutor Registration --> D1[Set is_verified=False];
        D1 -- Send Pending Email --> D2[Email Service];
        D -- Success --> E[Login Page];
        B -- Login --> F[LoginForm];
        F -- Submit --> G{LoginView};
        G -- Success --> H[Dashboard (Role-based)];
        G -- Failure --> F;
    ```

- **Goal 3: Set up Basic Dashboard Views (Placeholder)**
  - **Description:** Create placeholder views and templates for Admin, Tutor, and Student dashboards. These will initially be simple pages that confirm successful login and display the user's role. For tutors, access to their dashboard will be conditional on `is_verified` status.
  - **Steps:**
    1.  Create `users/views.py` functions: `admin_dashboard_view`, `tutor_dashboard_view`, `student_dashboard_view`.
    2.  Implement a decorator or middleware to restrict access to dashboards based on user role and `is_verified` status for tutors.
    3.  Create corresponding HTML templates: `admin_dashboard.html`, `tutor_dashboard.html`, `student_dashboard.html`.
    4.  Add URL patterns for these dashboards in `users/urls.py`.
    5.  Implement redirection logic after login based on the user's role and verification status.
  - **Mermaid Diagram: Dashboard Redirection**
    ```mermaid
    graph TD
        A[LoginView] --> B{Check User Role};
        B -- Admin --> C[AdminDashboardView];
        B -- Tutor --> D{Check Tutor is_verified};
        D -- Verified --> E[TutorDashboardView];
        D -- Not Verified --> F[Tutor Pending Page];
        B -- Student --> G[StudentDashboardView];
    ```

---

### Subsequent Phases (High-Level Overview):

- **Phase 3: Student Dashboard Features:** Implement course search, session booking, payment, exams, ratings, and chat.
- **Phase 4: Tutor Dashboard Features:** Implement session management, profile updates, material uploads, attendance tracking, and chat.
- **Phase 5: Admin Dashboard Features:** Implement user management, tutor verification, notifications, booking/schedule management, and payment/ratings oversight.
