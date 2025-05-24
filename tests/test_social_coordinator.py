from utils.social_coordinator import SocialIntegrationCoordinator
from utils.database import Database
from utils.social_api import SocialAPIClient, PLATFORMS

class DummyClient(SocialAPIClient):
    def get_post_metrics(self, post_id: str):
        return {"views": 1, "likes": 1, "comments": 0, "shares": 0}

    def get_post_text(self, post_id: str) -> str:
        return stored_tag

    def get_post_time(self, post_id: str) -> float:
        return 0.0

PLATFORMS["coord_dummy"] = DummyClient

db = Database(":memory:", pool_size=1)
coordinator = SocialIntegrationCoordinator(db)
stored_tag = coordinator.create_tag("sub1", "miner1", 0.0)

def test_process_post():
    metrics = coordinator.process_post("sub1", "p1", "coord_dummy", 0.0)
    assert metrics["views"] == 1.0
    conn = db.connect()
    row = conn.execute("SELECT valid FROM social_posts WHERE post_id='p1'").fetchone()
    db.release(conn)
    assert row is not None and row[0] == 1

