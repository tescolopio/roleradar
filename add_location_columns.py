#!/usr/bin/env python3
"""Add location-based ranking columns to database."""

from sqlalchemy import text
from src.roleradar.database import db_service


def add_columns():
    """Add geocoding columns to companies and opportunities tables."""
    print("=" * 70)
    print("Adding location-based ranking columns")
    print("=" * 70)

    with db_service.get_session() as session:
        # Check if columns already exist
        try:
            session.execute(text("SELECT latitude FROM companies LIMIT 1"))
            print("\n✅ Location columns already exist in the database!")
            return True
        except Exception:
            print("\n📍 Location columns not found, creating them...\n")

        commands = [
            ("companies", "latitude FLOAT"),
            ("companies", "longitude FLOAT"),
            ("companies", "geocoded_at TIMESTAMP"),
            ("opportunities", "latitude FLOAT"),
            ("opportunities", "longitude FLOAT"),
            ("opportunities", "geocoded_at TIMESTAMP"),
        ]

        for table, column_def in commands:
            cmd = f"ALTER TABLE {table} ADD COLUMN {column_def}"
            try:
                session.execute(text(cmd))
                print(f"✅ {table}: Added {column_def.split()[0]}")
            except Exception as e:
                error_msg = str(e).lower()
                # SQLite "column already exists" error
                if "duplicate column" in error_msg or "already exists" in error_msg:
                    print(f"⚠️  {table}: Column {column_def.split()[0]} already exists")
                else:
                    print(f"❌ {table}: Error adding {column_def.split()[0]} - {e}")

        try:
            session.commit()
            print("\n✅ Database schema updated successfully!")
            return True
        except Exception as e:
            print(f"\n❌ Error committing changes: {e}")
            session.rollback()
            return False


if __name__ == "__main__":
    success = add_columns()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete! Location columns are ready.")
    else:
        print("⚠️  Migration completed with warnings. Check output above.")
    print("=" * 70)
