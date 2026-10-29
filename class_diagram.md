# Class Diagram

```mermaid
classDiagram
    class Patient {
        -String patientId
        -String name
        -String phone
        +int MAX_UPCOMING
        +viewAvailability(doctor) List~TimeSlot~
        +bookAppointment(slot) Appointment
        +cancelAppointment(appointment) void
        +countUpcoming() int
    }

    class Doctor {
        -String doctorId
        -String name
        -String specialty
        +getAvailableSlots() List~TimeSlot~
        +respond(appointment, accept) void
    }

    class TimeSlot {
        -String slotId
        -Date date
        -Time startTime
        -Time endTime
        -boolean available
        +isFree() boolean
        +reserve() void
        +release() void
    }

    class Appointment {
        -String appointmentId
        -AppointmentStatus status
        +accept() void
        +decline() void
        +cancel() void
        +isUpcoming() boolean
        +countsTowardLimit() boolean
    }

    class AppointmentStatus {
        <<enumeration>>
        PENDING
        ACCEPTED
        DECLINED
        CANCELLED
    }

    Doctor "1" *-- "0..*" TimeSlot : offers
    Patient "1" --> "0..*" Appointment : books
    Doctor "1" --> "0..*" Appointment : receives
    Appointment "0..1" --> "1" TimeSlot : reserves
    Appointment --> AppointmentStatus : has
```

## Notes
- **Doctor to TimeSlot is composition**: a slot cannot exist without its doctor.
- **N = 3** is stored as `Patient.MAX_UPCOMING`. `countsTowardLimit()` is true only for future Pending/Accepted appointments (R4).
- `viewAvailability` / `getAvailableSlots` cover R1, `bookAppointment` covers R2, `respond` / `accept` / `decline` cover R3.
