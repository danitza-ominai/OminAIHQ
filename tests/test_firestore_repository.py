
"""Pruebas exhaustivas para el Adaptador de Firestore (PZ-014A, H12)."""
import unittest

import app.firestore_repository as firestore_repository


class TestFirestoreRepository(unittest.TestCase):
    def setUp(self):
        self.repo = firestore_repository.FirestoreRepository(project_id="test-proj")

    def test_save_and_get_mission(self):
        mission_data = {
            "mission_id": "MSN-CLOUD-001",
            "version": 1,
            "status": "BORRADOR",
            "user_id": "niko@ominai.ai",
        }
        self.repo.save_mission(mission_data)
        fetched = self.repo.get_mission("MSN-CLOUD-001")
        self.assertEqual(fetched, mission_data)

    def test_events_immutability_and_ordering(self):
        ev1 = {"event_id": "EV1", "mission_id": "MSN-01", "timestamp": "2026-01-01T00:00:00Z", "action": "initiate"}
        ev2 = {"event_id": "EV2", "mission_id": "MSN-01", "timestamp": "2026-01-01T00:01:00Z", "action": "approve"}
        self.repo.save_event(ev1)
        self.repo.save_event(ev2)
        evs = self.repo.list_events("MSN-01")
        self.assertEqual(len(evs), 2)
        self.assertEqual(evs[0]["event_id"], "EV1")
        self.assertEqual(evs[1]["event_id"], "EV2")


if __name__ == "__main__":
    unittest.main()
