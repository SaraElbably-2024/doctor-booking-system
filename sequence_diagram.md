# Sequence Diagram

Every message below is a method from `class_diagram.md`.

## 1. Appointment request / booking (UC1, UC2, UC4 - R1, R2, R4)

```mermaid
sequenceDiagram
    actor Patient
    participant Doctor
    participant TimeSlot
    participant Appointment

    Patient->>Doctor: getAvailableSlots()
    Doctor-->>Patient: free slots

    Patient->>Patient: bookAppointment(slot)
    Patient->>Patient: countUpcoming()

    alt upcoming appointments >= N (3)
        Patient-->>Patient: refuse: limit reached
    else limit not reached
        Patient->>TimeSlot: isFree()
        TimeSlot-->>Patient: true or false
        alt slot is taken
            Patient-->>Patient: refuse: slot taken
        else slot is free
            Patient->>TimeSlot: reserve()
            Patient->>Appointment: create appointment (status PENDING)
            Appointment-->>Patient: appointment
        end
    end
```

## 2. Doctor accepts or declines the request (UC3 - R3)

```mermaid
sequenceDiagram
    actor Doctor
    participant Appointment
    participant TimeSlot

    Doctor->>Doctor: respond(appointment, accept)

    alt accept is true
        Doctor->>Appointment: accept()
        Appointment-->>Doctor: status ACCEPTED
    else accept is false
        Doctor->>Appointment: decline()
        Appointment->>TimeSlot: release()
        Appointment-->>Doctor: status DECLINED
    end
```

## Checks
- The limit check (`countUpcoming`) happens BEFORE the slot is reserved.
- A declined request releases the slot, so it can be booked again and no longer counts toward N.
- Answers are dashed arrows; both the limit branch and the slot-taken branch exist (alt / else).
