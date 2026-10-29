# doctor-booking-system
# Doctor Appointment Booking System

Small console application built with the engineering workflow: requirements, use cases, class diagram, sequence diagram, implementation. Python 3, standard library only.

## Team

| Student ID | Full name | Assigned task    | Branch                   | PR link |
|------------|-----------|------------------|--------------------------|---------|
| ________   | ________  | Use Cases        | stage-1-use-cases        | ________ |
| ________   | ________  | Class Diagram    | stage-2-class-diagram    | ________ |
| ________   | ________  | Sequence Diagram | stage-3-sequence-diagram | ________ |
| ________   | ________  | Implementation   | stage-4-implementation   | ________ |

## Repository files

| File | Content |
|------|---------|
| `requirements.txt` | R1-R7 (functional / non-functional) and the chosen N |
| `use_cases.md` | Patient and doctor use cases |
| `use_case_diagram.md` | Use case diagram (Mermaid flowchart) |
| `class_diagram.md` | Class diagram (Mermaid) |
| `sequence_diagram.md` | Booking and accept/decline sequence diagrams (Mermaid) |
| `main.py` | The application |
| `test_main.py` | Unit tests |

## Chosen value of N

**N = 3.** A patient can have at most 3 upcoming appointments. Future **Pending + Accepted** appointments count. Declined, Cancelled and past appointments do not count. In the code: `N` and `Patient.MAX_UPCOMING` in `main.py`.

## How to run

Requires Python 3.9 or newer. No packages to install.

```bash
# Interactive console app
python main.py

# Scripted demo of R1-R4
python main.py --demo

# Unit tests
python -m unittest
```

In the interactive app, choose "I am a patient" to view availability, book and cancel; choose "I am a doctor" to accept or decline pending requests. Sample doctors, patients and time slots are created at start-up and kept in memory.

## Functional requirements in the code (R1-R4)

| Req | Where |
|-----|-------|
| R1 view availability | `Patient.viewAvailability`, `Doctor.getAvailableSlots` |
| R2 book in a free slot | `Patient.bookAppointment` (creates a PENDING appointment, reserves the slot) |
| R3 accept / decline | `Doctor.respond`, `Appointment.accept`, `Appointment.decline` (decline frees the slot) |
| R4 at most N upcoming | `Patient.countUpcoming`, `Appointment.countsTowardLimit` (checked before reserving) |

## Non-functional requirements (design notes, not implemented)

**R5 - Patient medical data only for authorized staff.** Add authentication (login) and role-based access control: patients see only their own data, doctors only the patients who booked with them, administrators only what their role needs. Store medical data in a separate, encrypted table; use HTTPS in transit and encryption at rest; keep an audit log of who read each record.

**R6 - Available times shown within 2 seconds.** Query only free future slots, with a database index on (doctor, date, available). Return one doctor and a date range per request (pagination), and cache the availability list for a short time, invalidating it when a slot is booked or released. Measure with a load test and a response-time alert.

**R7 - Usable on mobile phone screens.** Use a responsive web UI (mobile-first layout, flexible grid, viewport meta tag), touch-sized buttons (about 44 px), readable font sizes, and a simple booking flow with few steps. Test on real phone screen sizes and with browser device emulation.

## Diagrams

All diagrams are Mermaid inside `.md` files and render on GitHub.
