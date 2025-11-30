"""Seed data for database initialization.

Creates default player and initial data if database is empty.
"""

from app.database import SessionLocal
from app.models.achievement import PlayerStats
from app.models.player import Player
from app.models.progress import Progress
from app.schemas.progress import ProgressStatus


def seed_default_player():
    """
    Create a default player if database is empty.

    Creates:
    - Demo player with ID 1
    - Initial player stats (all zeros)
    - Progress entry for Module 0, Class 0 (unlocked)
    """
    db = SessionLocal()

    try:
        # Check if any player exists
        existing_player = db.query(Player).first()

        if existing_player:
            print(f"Database already has players. Skipping seed. (Found: {existing_player.username})")
            return

        # Create default player
        print("Creating default demo player...")
        demo_player = Player(
            username="Demo Player",
            avatar="default.png",
            level=1,
            xp=0
        )

        db.add(demo_player)
        db.flush()  # Get player.id without committing yet

        # Create initial player stats
        print("Creating initial player stats...")
        player_stats = PlayerStats(
            player_id=demo_player.id,
            classes_completed=0,
            exercises_completed=0,
            bug_hunt_games_played=0,
            bug_hunt_wins=0,
            current_streak=0,
            longest_streak=0
        )

        db.add(player_stats)

        # Unlock Module 0, Class 0 (starting point)
        print("Unlocking Module 0, Class 0...")
        initial_progress = Progress(
            player_id=demo_player.id,
            module_number=0,
            class_number=0,
            status=ProgressStatus.UNLOCKED,
            exercises_completed=0
        )

        db.add(initial_progress)

        # Commit all changes
        db.commit()

        print(f"✅ Default player created successfully!")
        print(f"   - Username: {demo_player.username}")
        print(f"   - Player ID: {demo_player.id}")
        print(f"   - Initial class unlocked: Module 0, Class 0")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    """Run seed script directly for testing."""
    print("Running seed data script...")
    seed_default_player()
    print("Seed script completed.")
