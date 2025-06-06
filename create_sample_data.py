#!/usr/bin/env python3
"""
Script para criar dados de exemplo para o gnS (Genius) Member Directory
"""

from database import Database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_members():
    """Create sample members for testing"""
    db = Database()
    
    sample_members = [
        {
            'name': 'João Silva',
            'commander_name': 'JoaoCommander',
            'phone': '(11) 99999-1234',
            'photo_filename': None
        },
        {
            'name': 'Maria Santos',
            'commander_name': 'MariaBattler',
            'phone': '(21) 98888-5678',
            'photo_filename': None
        },
        {
            'name': 'Pedro Oliveira',
            'commander_name': 'PedroWarrior',
            'phone': None,
            'photo_filename': None
        },
        {
            'name': 'Ana Costa',
            'commander_name': 'AnaStrategist',
            'phone': '(31) 97777-9012',
            'photo_filename': None
        },
        {
            'name': 'Carlos Ferreira',
            'commander_name': 'CarlosLeader',
            'phone': '(41) 96666-3456',
            'photo_filename': None
        },
        {
            'name': 'Lucia Rodrigues',
            'commander_name': 'LuciaDefender',
            'phone': None,
            'photo_filename': None
        },
        {
            'name': 'Roberto Lima',
            'commander_name': 'RobertoTactical',
            'phone': '(51) 95555-7890',
            'photo_filename': None
        },
        {
            'name': 'Fernanda Alves',
            'commander_name': 'FernandaSniper',
            'phone': '(61) 94444-2345',
            'photo_filename': None
        }
    ]
    
    created_count = 0
    for member_data in sample_members:
        try:
            # Check if commander name already exists
            if not db.check_commander_name_exists(member_data['commander_name']):
                member = db.create_member(
                    name=member_data['name'],
                    commander_name=member_data['commander_name'],
                    phone=member_data['phone'],
                    photo_filename=member_data['photo_filename']
                )
                if member:
                    created_count += 1
                    logger.info(f"Created member: {member_data['name']} ({member_data['commander_name']})")
            else:
                logger.info(f"Member already exists: {member_data['commander_name']}")
                
        except Exception as e:
            logger.error(f"Error creating member {member_data['name']}: {str(e)}")
    
    logger.info(f"Sample data creation completed. Created {created_count} new members.")
    return created_count

def main():
    """Main function"""
    print("Creating sample data for gnS (Genius) Member Directory...")
    created_count = create_sample_members()
    print(f"✅ Sample data created successfully! Added {created_count} members.")
    print("You can now test the application with sample data.")

if __name__ == '__main__':
    main()
