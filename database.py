import json
import os
from datetime import datetime
import uuid
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        # For now, use a simple JSON file as database for testing
        # Later we'll switch to Supabase
        self.db_file = 'members.json'
        self._ensure_db_file()

    def _ensure_db_file(self):
        """Ensure the database file exists"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)

    def _load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def _save_data(self, data):
        """Save data to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)

    def create_member(self, name, commander_name, phone=None, photo_filename=None):
        """Create a new member in the database"""
        try:
            data = self._load_data()

            # Check if commander name already exists
            for member in data:
                if member['commander_name'].lower() == commander_name.lower():
                    raise ValueError("Commander name already exists")

            new_member = {
                "id": str(uuid.uuid4()),
                "name": name,
                "commander_name": commander_name,
                "phone": phone,
                "photo_filename": photo_filename,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            data.append(new_member)
            self._save_data(data)

            logger.info(f"Member created successfully: {name}")
            return new_member

        except Exception as e:
            logger.error(f"Error creating member: {str(e)}")
            raise e

    def get_all_members(self):
        """Get all members from the database"""
        try:
            data = self._load_data()
            # Sort by created_at descending
            data.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return data

        except Exception as e:
            logger.error(f"Error fetching members: {str(e)}")
            raise e

    def get_member_by_id(self, member_id):
        """Get a specific member by ID"""
        try:
            data = self._load_data()
            for member in data:
                if member['id'] == member_id:
                    return member
            return None

        except Exception as e:
            logger.error(f"Error fetching member {member_id}: {str(e)}")
            raise e

    def check_commander_name_exists(self, commander_name):
        """Check if commander name already exists"""
        try:
            data = self._load_data()
            for member in data:
                if member['commander_name'].lower() == commander_name.lower():
                    return True
            return False

        except Exception as e:
            logger.error(f"Error checking commander name: {str(e)}")
            return False
