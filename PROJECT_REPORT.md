# HostelEase — Smart Hostel Management System

## 1. Abstract
HostelEase is a web-based mini-project prototype intended to make common hostel administration tasks easier to organize. It provides a single interface for student accounts, room records, hostel fee records, complaints, visitor entries and notices. The React frontend communicates with a Python Flask REST API, while MongoDB stores the application records. The prototype demonstrates how a modern web application can separate presentation, business logic and persistent data storage.

## 2. Problem Statement
Hostel information may be maintained in separate registers or files, making it harder to find current room availability, fee status, unresolved complaints and visitor details. HostelEase explores a centralized digital approach to keeping these records organized and accessible through a web interface.

## 3. Objectives
- Provide a simple interface for hostel-related records.
- Allow students to register and log in.
- Maintain room availability records.
- Record total and paid fees and calculate pending balances.
- Register complaints and track their status.
- Record visitor entries/exits and hostel notices.
- Demonstrate frontend-backend communication and database CRUD operations.

## 4. Scope and Modules
1. **Authentication:** student registration and login; newly registered passwords are hashed.
2. **Dashboard:** displays summary counts for students, rooms, pending fee records, complaints and visitors.
3. **Room Management:** add room number, capacity and availability status.
4. **Fee Management:** record total fee, paid amount and due date; calculate pending amount and status.
5. **Complaint Management:** record complaint title/description and track Open/Resolved status.
6. **Visitor Register:** record visitor name, phone and purpose, then update entry/exit status.
7. **Notice Board:** create hostel announcements.
8. **Student Profile:** display registered student details.

## 5. Technology Used
| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Vite | Interactive user interface and development server |
| Routing | React Router | Navigation between pages and modules |
| Styling | CSS | Responsive layout and visual design |
| Backend | Python + Flask | REST endpoints, validation and application logic |
| Database driver | PyMongo | Communication between Flask and MongoDB |
| Database | MongoDB | Persistent storage of users and module records |

## 6. System Architecture
The browser renders the React frontend. When a user submits a form, the frontend sends an HTTP request to the Flask API. Flask validates the request and reads or writes records in MongoDB through PyMongo. The API returns a JSON response, and React updates the page accordingly.

**Flow:** Student/Admin browser → React frontend → Flask REST API → MongoDB → JSON response → React UI.

## 7. Data Collections
- `users`: name, email, phone, student ID, room number, hashed password, role and creation time.
- `rooms`: room number, capacity, status and creation time.
- `fees`: student email, total amount, paid amount, pending amount, due date, status and creation time.
- `complaints`: student email, title, description, status and creation time.
- `visitors`: student email, visitor details, purpose, date and status.
- `notices`: title, description and creation time.

## 8. Testing Plan
| Test | Expected result |
|---|---|
| Open `/api/health` | Backend returns JSON status `ok` |
| Open `/api/db-test` with MongoDB running | Database check returns status `ok` |
| Register a unique student email | Account is created and password is hashed |
| Register the same email again | API rejects the duplicate email |
| Login with correct details | Login succeeds and profile data is returned without password |
| Add a room | Room record appears in the room list |
| Add fee with total ₹10,000 and paid ₹4,000 | Pending is ₹6,000 and status is Partial |
| Add a complaint | Complaint appears with Open status |
| Mark complaint resolved | Status changes to Resolved |
| Add a visitor | Visitor appears with entry status |

## 9. Limitations
This is a college demonstration prototype. It does not implement production-grade token/session authentication, administrator authorization, a payment gateway, email/SMS alerts, or cloud deployment. Module pages should not be exposed to public users without additional authorization and security controls.

## 10. Future Scope
- Role-based admin and student access.
- Secure session/JWT authentication and authorization checks on every API.
- Online fee payment integration and downloadable receipts.
- Room allocation conflict checks and occupancy reports.
- Complaint notifications and service-level tracking.
- Email/SMS notices, audit logs, backups and deployment to a secure cloud environment.

## 11. Conclusion
HostelEase demonstrates a full-stack web application using React, Flask and MongoDB. It brings several common hostel record-management tasks into one interface and provides a foundation for further development with stronger authentication, administration controls and deployment practices.
