"""Doctor Appointment Booking System (console app, Python 3, standard library only).

Run:   python main.py          interactive console
       python main.py --demo   scripted demo of R1-R4
"""
import sys
from datetime import date, time, datetime, timedelta
from enum import Enum
from itertools import count

N = 3  # R4: max upcoming (Pending + Accepted) appointments per patient
_ids = count(1)


class BookingError(Exception):
    pass


class AppointmentStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"


class TimeSlot:
    def __init__(self, slotId, day, startTime, endTime, doctor):
        self.slotId = slotId
        self.date = day
        self.startTime = startTime
        self.endTime = endTime
        self.doctor = doctor
        self.available = True

    def start(self):
        return datetime.combine(self.date, self.startTime)

    def isFree(self):
        return self.available

    def reserve(self):
        self.available = False

    def release(self):
        self.available = True

    def __str__(self):
        return f"[{self.slotId}] {self.date:%a %d %b %Y} {self.startTime:%H:%M}-{self.endTime:%H:%M}"


class Appointment:
    def __init__(self, appointmentId, patient, slot):
        self.appointmentId = appointmentId
        self.patient = patient
        self.slot = slot
        self.status = AppointmentStatus.PENDING

    def accept(self):
        if self.status != AppointmentStatus.PENDING:
            raise BookingError("Only a pending request can be accepted.")
        self.status = AppointmentStatus.ACCEPTED

    def decline(self):
        if self.status != AppointmentStatus.PENDING:
            raise BookingError("Only a pending request can be declined.")
        self.status = AppointmentStatus.DECLINED
        self.slot.release()

    def cancel(self):
        if self.status not in (AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED):
            raise BookingError("This appointment cannot be cancelled.")
        self.status = AppointmentStatus.CANCELLED
        self.slot.release()

    def isUpcoming(self):
        return self.slot.start() > datetime.now()

    def countsTowardLimit(self):
        return self.isUpcoming() and self.status in (
            AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED)

    def __str__(self):
        return (f"#{self.appointmentId} {self.slot.doctor.name} | {self.slot} | "
                f"{self.patient.name} | {self.status.value}")


class Doctor:
    def __init__(self, doctorId, name, specialty):
        self.doctorId = doctorId
        self.name = name
        self.specialty = specialty
        self.slots = []
        self.appointments = []

    def addSlot(self, day, startTime, endTime):
        slot = TimeSlot(f"{self.doctorId}-{len(self.slots) + 1}", day, startTime, endTime, self)
        self.slots.append(slot)
        return slot

    def getAvailableSlots(self):  # R1
        return [s for s in self.slots if s.isFree() and s.start() > datetime.now()]

    def __str__(self):
        return f"{self.name} ({self.specialty})"

    def respond(self, appointment, accept):  # R3
        if appointment.slot.doctor is not self:
            raise BookingError("This request belongs to another doctor.")
        if accept:
            appointment.accept()
        else:
            appointment.decline()


class Patient:
    MAX_UPCOMING = N

    def __init__(self, patientId, name, phone=""):
        self.patientId = patientId
        self.name = name
        self.phone = phone
        self.appointments = []

    def __str__(self):
        return self.name

    def viewAvailability(self, doctor):  # R1
        return doctor.getAvailableSlots()

    def countUpcoming(self):
        return sum(1 for a in self.appointments if a.countsTowardLimit())

    def bookAppointment(self, slot):  # R2 + R4
        if self.countUpcoming() >= self.MAX_UPCOMING:
            raise BookingError(f"Limit reached: at most {self.MAX_UPCOMING} upcoming appointments.")
        if not slot.isFree():
            raise BookingError("This time slot is already taken.")
        slot.reserve()
        appointment = Appointment(next(_ids), self, slot)
        self.appointments.append(appointment)
        slot.doctor.appointments.append(appointment)
        return appointment

    def cancelAppointment(self, appointment):
        if appointment.patient is not self:
            raise BookingError("This is not your appointment.")
        appointment.cancel()


def seed():
    """Sample data: 2 doctors with slots on the next 3 days, 2 patients."""
    doctors = [Doctor("D1", "Dr. Mona Adel", "Cardiology"),
               Doctor("D2", "Dr. Omar Hassan", "Dermatology")]
    base = date.today() + timedelta(days=1)
    for doc in doctors:
        for d in range(3):
            for h in (9, 10, 11):
                doc.addSlot(base + timedelta(days=d), time(h, 0), time(h, 30))
    patients = [Patient("P1", "Sara Ahmed", "0100000001"),
                Patient("P2", "Ali Samir", "0100000002")]
    return doctors, patients


def pick(items, label):
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    try:
        return items[int(input(f"{label}: ")) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return None


def patient_menu(patient, doctors):
    while True:
        print(f"\n--- Patient: {patient.name} (upcoming {patient.countUpcoming()}/{N}) ---")
        print("1 View doctor availability\n2 Book appointment\n3 My appointments\n"
              "4 Cancel appointment\n0 Back")
        choice = input("> ").strip()
        try:
            if choice == "1":
                doc = pick(doctors, "Doctor")
                if doc:
                    slots = patient.viewAvailability(doc)
                    print("\n".join(f"  {s}" for s in slots) or "  No available times")
            elif choice == "2":
                doc = pick(doctors, "Doctor")
                slots = patient.viewAvailability(doc) if doc else []
                if doc and not slots:
                    print("  No available times")
                slot = pick(slots, "Slot") if slots else None
                if slot:
                    print("Request sent:", patient.bookAppointment(slot))
            elif choice == "3":
                print("\n".join(f"  {a}" for a in patient.appointments) or "  None")
            elif choice == "4":
                appt = pick([a for a in patient.appointments if a.countsTowardLimit()], "Appointment")
                if appt:
                    patient.cancelAppointment(appt)
                    print("Cancelled.")
            elif choice == "0":
                return
        except BookingError as e:
            print("Error:", e)


def doctor_menu(doctor):
    while True:
        print(f"\n--- {doctor.name} ---\n1 Pending requests\n2 Accept/decline a request\n"
              "3 All appointments\n0 Back")
        choice = input("> ").strip()
        pending = [a for a in doctor.appointments if a.status == AppointmentStatus.PENDING]
        try:
            if choice == "1":
                print("\n".join(f"  {a}" for a in pending) or "  None")
            elif choice == "2":
                appt = pick(pending, "Request")
                if appt:
                    accept = input("Accept? (y/n): ").strip().lower() == "y"
                    doctor.respond(appt, accept)
                    print("Done:", appt)
            elif choice == "3":
                print("\n".join(f"  {a}" for a in doctor.appointments) or "  None")
            elif choice == "0":
                return
        except BookingError as e:
            print("Error:", e)


def interactive():
    doctors, patients = seed()
    while True:
        print("\n=== Doctor Appointment Booking ===\n1 I am a patient\n2 I am a doctor\n0 Exit")
        choice = input("> ").strip()
        if choice == "1":
            p = pick(patients, "Patient")
            if p:
                patient_menu(p, doctors)
        elif choice == "2":
            d = pick(doctors, "Doctor")
            if d:
                doctor_menu(d)
        elif choice == "0":
            return


def demo():
    doctors, patients = seed()
    doc, sara, ali = doctors[0], patients[0], patients[1]
    slots = sara.viewAvailability(doc)
    print(f"R1: {doc.name} has {len(slots)} free slots, first: {slots[0]}")

    booked = [sara.bookAppointment(slots[i]) for i in range(3)]
    print(f"R2: Sara booked 3 slots -> {[a.status.value for a in booked]}")

    try:
        sara.bookAppointment(slots[3])
    except BookingError as e:
        print("R4: 4th booking refused ->", e)

    doc.respond(booked[0], True)
    doc.respond(booked[1], False)
    print(f"R3: accepted #{booked[0].appointmentId}, declined #{booked[1].appointmentId}")
    print(f"R4: Sara upcoming now {sara.countUpcoming()}/{N} (declined does not count)")

    sara.bookAppointment(slots[3])
    print("R4: Sara can book again after a decline ->", sara.countUpcoming(), "/", N)

    try:
        ali.bookAppointment(slots[0])
    except BookingError as e:
        print("Slot taken ->", e)


if __name__ == "__main__":
    demo() if "--demo" in sys.argv else interactive()
