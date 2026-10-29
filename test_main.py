import unittest
from main import (Patient, Doctor, BookingError, AppointmentStatus, seed)


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.doctors, self.patients = seed()
        self.doc = self.doctors[0]
        self.sara, self.ali = self.patients
        self.slots = self.doc.getAvailableSlots()

    def test_view_availability(self):
        self.assertEqual(len(self.sara.viewAvailability(self.doc)), 9)

    def test_book_creates_pending_and_reserves_slot(self):
        a = self.sara.bookAppointment(self.slots[0])
        self.assertEqual(a.status, AppointmentStatus.PENDING)
        self.assertFalse(self.slots[0].isFree())

    def test_slot_taken(self):
        self.sara.bookAppointment(self.slots[0])
        with self.assertRaises(BookingError):
            self.ali.bookAppointment(self.slots[0])

    def test_limit_is_three(self):
        for i in range(3):
            self.sara.bookAppointment(self.slots[i])
        with self.assertRaises(BookingError):
            self.sara.bookAppointment(self.slots[3])

    def test_declined_and_cancelled_do_not_count(self):
        a = [self.sara.bookAppointment(self.slots[i]) for i in range(3)]
        self.doc.respond(a[0], False)
        self.sara.cancelAppointment(a[1])
        self.assertEqual(self.sara.countUpcoming(), 1)
        self.sara.bookAppointment(self.slots[3])

    def test_accept_and_decline(self):
        a = self.sara.bookAppointment(self.slots[0])
        self.doc.respond(a, True)
        self.assertEqual(a.status, AppointmentStatus.ACCEPTED)
        b = self.sara.bookAppointment(self.slots[1])
        self.doc.respond(b, False)
        self.assertEqual(b.status, AppointmentStatus.DECLINED)
        self.assertTrue(self.slots[1].isFree())

    def test_other_doctor_cannot_respond(self):
        a = self.sara.bookAppointment(self.slots[0])
        with self.assertRaises(BookingError):
            self.doctors[1].respond(a, True)


if __name__ == "__main__":
    unittest.main()
