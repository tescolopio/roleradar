"""Add transparency tracking columns to search_results table."""

from sqlalchemy import text
from src.roleradar.database import db_service

def add_columns():
    """Add new columns for transparency tracking."""
    with db_service.get_session() as session:
        # Check if columns exist before adding
        try:
            # Try to select from the new columns
            session.execute(text("SELECT processed_date FROM search_results LIMIT 1"))
            print("✅ Columns already exist")
            return
        except Exception:
            # Columns don't exist, add them
            print("Adding transparency tracking columns...")
            
            commands = [
                "ALTER TABLE search_results ADD COLUMN processed_date TIMESTAMP",
                "ALTER TABLE search_results ADD COLUMN extracted_company VARCHAR(255)",
                "ALTER TABLE search_results ADD COLUMN extracted_job_title VARCHAR(255)",
                "ALTER TABLE search_results ADD COLUMN extracted_role_type VARCHAR(100)",
                "ALTER TABLE search_results ADD COLUMN extracted_location VARCHAR(255)",
                "ALTER TABLE search_results ADD COLUMN extracted_keywords TEXT",
                "ALTER TABLE search_results ADD COLUMN detected_signal BOOLEAN DEFAULT FALSE",
                "ALTER TABLE search_results ADD COLUMN signal_type VARCHAR(100)",
                "ALTER TABLE search_results ADD COLUMN signal_confidence FLOAT",
                "ALTER TABLE search_results ADD COLUMN signal_description TEXT",
                "ALTER TABLE search_results ADD COLUMN processing_error TEXT"
            ]
            
            for cmd in commands:
                try:
                    session.execute(text(cmd))
                    print(f"✅ {cmd.split('ADD COLUMN')[1].split()[0]}")
                except Exception as e:
                    print(f"⚠️  {cmd.split('ADD COLUMN')[1].split()[0]} - {e}")
            
            session.commit()
            print("\n✅ Database schema updated successfully!")

if __name__ == "__main__":
    add_columns()
