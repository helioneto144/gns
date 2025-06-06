import json
import os
from datetime import datetime
import uuid
from config import Config
import logging

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Supabase, fallback to JSON if not available
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
    logger.info("Supabase library available")
except ImportError:
    SUPABASE_AVAILABLE = False
    logger.warning("Supabase not available, using JSON fallback")

class Database:
    def __init__(self):
        self.use_supabase = SUPABASE_AVAILABLE and hasattr(Config, 'SUPABASE_URL') and Config.SUPABASE_URL

        if self.use_supabase:
            try:
                self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
                logger.info("Connected to Supabase database")
            except Exception as e:
                logger.error(f"Failed to connect to Supabase: {str(e)}")
                self.use_supabase = False
                self._init_json_fallback()
        else:
            self._init_json_fallback()

    def _init_json_fallback(self):
        """Initialize JSON file fallback"""
        self.db_file = 'members.json'
        self._ensure_db_file()
        logger.info("Using JSON file database")

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
            if self.use_supabase:
                return self._create_member_supabase(name, commander_name, phone, photo_filename)
            else:
                return self._create_member_json(name, commander_name, phone, photo_filename)
        except Exception as e:
            logger.error(f"Error creating member: {str(e)}")
            raise e

    def _create_member_supabase(self, name, commander_name, phone=None, photo_filename=None):
        """Create member using Supabase"""
        # Check if commander name already exists
        if self.check_commander_name_exists(commander_name):
            raise ValueError("Commander name already exists")

        data = {
            "name": name,
            "commander_name": commander_name,
            "phone": phone,
            "photo_filename": photo_filename
        }

        result = self.supabase.table("members").insert(data).execute()
        logger.info(f"Member created successfully in Supabase: {name}")
        return result.data[0] if result.data else None

    def _create_member_json(self, name, commander_name, phone=None, photo_filename=None):
        """Create member using JSON file"""
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

        logger.info(f"Member created successfully in JSON: {name}")
        return new_member

    def get_all_members(self):
        """Get all members from the database"""
        try:
            if self.use_supabase:
                result = self.supabase.table("members").select("*").order("created_at", desc=True).execute()
                return result.data if result.data else []
            else:
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
            if self.use_supabase:
                result = self.supabase.table("members").select("*").eq("id", member_id).execute()
                return result.data[0] if result.data else None
            else:
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
            if self.use_supabase:
                result = self.supabase.table("members").select("id").eq("commander_name", commander_name).execute()
                return len(result.data) > 0 if result.data else False
            else:
                data = self._load_data()
                for member in data:
                    if member['commander_name'].lower() == commander_name.lower():
                        return True
                return False

        except Exception as e:
            logger.error(f"Error checking commander name: {str(e)}")
            return False
