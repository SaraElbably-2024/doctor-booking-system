# Use Cases

Actors: **Patient** and **Doctor**. Only the functional requirements (R1-R4) become use cases.
Non-functional requirements (R5-R7) are addressed in the design / README.

Chosen limit: **N = 3** upcoming appointments per patient (Pending + Accepted, future only).

## Use case table

| UC  | Name                          | Actor   | Requirement | Description |
|-----|-------------------------------|---------|-------------|-------------|
| UC1 | View doctor availability      | Patient | R1          | As a Patient I view the days and times when a doctor is available. |
| UC2 | Book appointment              | Patient | R2, R4      | As a Patient I book an appointment in an available time slot. |
| UC3 | Accept or decline request     | Doctor  | R3          | As a Doctor I accept or decline a pending appointment request. |
| UC4 | Check appointment limit       | System  | R4          | The system checks that the patient has fewer than N = 3 upcoming appointments (included in UC2). |
| UC5 | Cancel appointment            | Patient | R4 (status) | As a Patient I cancel an upcoming appointment, which frees the slot and the limit. |

## UC1 - View doctor availability
**Actor:** Patient

**Main flow**
1. Patient selects a doctor.
2. System shows the doctor's available days and times (free slots only).

**Alternative flow**
- 2a. The doctor has no free slots: the system shows "No available times".

## UC2 - Book appointment
**Actor:** Patient (the system performs UC4)

**Preconditions:** The patient has viewed the available slots (UC1).

**Main flow**
1. Patient chooses a free time slot.
2. System checks the appointment limit (UC4).
3. System creates the appointment with status **Pending** and marks the slot as booked.
4. System confirms to the patient that the request was sent to the doctor.

**Alternative flows**
- 2a. The patient already has N = 3 upcoming Pending/Accepted appointments: the system refuses the booking and shows a limit message.
- 1a. The slot was taken meanwhile: the system refuses and asks the patient to choose another slot.

## UC3 - Accept or decline request
**Actor:** Doctor

**Main flow**
1. Doctor views the Pending requests.
2. Doctor selects a request and chooses **Accept**.
3. System sets the status to **Accepted**.

**Alternative flow**
- 3a. Doctor chooses **Decline**: the system sets the status to **Declined** and frees the time slot.

## UC4 - Check appointment limit
**Actor:** System (included in UC2)

**Rule:** count the patient's appointments where the date/time is in the future and the status is Pending or Accepted. If the count is 3 or more, booking is not allowed.

## UC5 - Cancel appointment
**Actor:** Patient

**Main flow**
1. Patient selects one of their upcoming appointments.
2. System sets the status to **Cancelled** and frees the time slot.

## Appointment statuses

| Status    | Counts toward N? |
|-----------|------------------|
| Pending   | Yes (if future)  |
| Accepted  | Yes (if future)  |
| Declined  | No               |
| Cancelled | No               |
| Past appointments | No       |
