#!/usr/bin/env python3
"""Add API usage tracking table to database."""

from sqlalchemy import text
from src.roleradar.database import db_service


def add_table():
    """Create API usage tracking table."""
    print("=" * 70)
    print("Adding API usage tracking table")
    print("=" * 70)

    with db_service.get_session() as session:
        # Check if table already exists
        try:
            session.execute(text("SELECT * FROM api_usage_logs LIMIT 1"))
            print("\n✅ API usage table already exists!")
            return True
        except Exception:
            print("\n📊 Creating API usage tracking table...\n")

        try:
            # Create table
            create_cmd = """
            CREATE TABLE api_usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_name VARCHAR(50) NOT NULL,
                endpoint VARCHAR(255),
                request_count INTEGER NOT NULL DEFAULT 1,
                date DATE NOT NULL,
                hour INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                query TEXT,
                result_count INTEGER,
                error TEXT
            )
            """
            session.execute(text(create_cmd))
            print("✅ Created api_usage_logs table")

            # Create indexes for performance
            index_commands = [
                "CREATE INDEX idx_api_name ON api_usage_logs(api_name)",
                "CREATE INDEX idx_date ON api_usage_logs(date)",
                "CREATE INDEX idx_api_date ON api_usage_logs(api_name, date)",
                "CREATE INDEX idx_hour ON api_usage_logs(hour)",
            ]

            for cmd in index_commands:
                try:
                    session.execute(text(cmd))
                    print(f"✅ {cmd.split('ON')[0].strip()}")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️  {cmd} - {e}")

            session.commit()
            print("\n✅ API tracking table created successfully!")
            return True

        except Exception as e:
            print(f"\n❌ Error creating table: {e}")
            session.rollback()
            return False


if __name__ == "__main__":
    success = add_table()
    print("\n" + "=" * 70)
    if success:
        print("✅ Migration complete! API tracking is ready.")
    else:
        print("⚠️  Migration completed with errors. Check output above.")
    print("=" * 70)
