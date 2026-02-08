"""
Migration Script: JSON to MySQL
Migrates existing user data from users.json to MySQL database
"""

import json
import sys
from database import DatabaseManager
from auth_manager_mysql import AuthManager
import bcrypt
from datetime import datetime

def migrate_json_to_mysql(json_file_path='users.json'):
    """
    Migrate users from JSON file to MySQL database
    
    Args:
        json_file_path: Path to the users.json file
    """
    print("="*60)
    print("JSON to MySQL Migration Tool")
    print("="*60)
    
    # Load JSON data
    try:
        with open(json_file_path, 'r') as f:
            users_data = json.load(f)
        print(f"✓ Loaded {len(users_data)} users from {json_file_path}")
    except FileNotFoundError:
        print(f"✗ Error: {json_file_path} not found")
        return False
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON in {json_file_path}")
        return False
    
    if not users_data:
        print("No users to migrate")
        return True
    
    # Test database connection
    print("\nTesting database connection...")
    if not DatabaseManager.test_connection():
        print("✗ Database connection failed")
        print("Please check your .env configuration")
        return False
    print("✓ Database connection successful")
    
    # Migrate users
    print(f"\nMigrating {len(users_data)} users...")
    print("-"*60)
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    auth = AuthManager()
    
    for username, user_data in users_data.items():
        try:
            # Check if user already exists
            if auth.username_exists(username):
                print(f"⊘ Skipped: {username} (already exists)")
                skipped_count += 1
                continue
            
            # Extract user data
            email = user_data.get('email', '')
            full_name = user_data.get('full_name', '')
            age = user_data.get('age', 0)
            academic_level = user_data.get('academic_level', '')
            password_hash = user_data.get('password_hash', '')
            profile_completed = user_data.get('profile_completed', False)
            assessment_results = user_data.get('assessment_results', {})
            recommendations = user_data.get('recommendations', [])
            
            # Validate required fields
            if not all([email, full_name, age, academic_level]):
                print(f"✗ Error: {username} - Missing required fields")
                error_count += 1
                continue
            
            # Insert user
            query = """
                INSERT INTO users 
                (username, email, password_hash, full_name, age, academic_level, profile_completed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (username, email, password_hash, full_name, age, academic_level, profile_completed)
            user_id = DatabaseManager.execute_query(query, params)
            
            if not user_id:
                print(f"✗ Error: {username} - Failed to insert user")
                error_count += 1
                continue
            
            # Insert assessment results if available
            if assessment_results:
                results_json = json.dumps(assessment_results)
                query = """
                    INSERT INTO assessment_results (user_id, assessment_type, results_json)
                    VALUES (%s, %s, %s)
                """
                DatabaseManager.execute_query(query, (user_id, 'full_assessment', results_json))
            
            # Insert recommendations if available
            if recommendations:
                recommendations_json = json.dumps(recommendations)
                query = """
                    INSERT INTO recommendations (user_id, recommendations_json)
                    VALUES (%s, %s)
                """
                DatabaseManager.execute_query(query, (user_id, recommendations_json))
            
            print(f"✓ Migrated: {username} ({email})")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error: {username} - {str(e)}")
            error_count += 1
    
    # Summary
    print("-"*60)
    print("\nMigration Summary:")
    print(f"  Total users in JSON: {len(users_data)}")
    print(f"  Successfully migrated: {success_count}")
    print(f"  Skipped (already exist): {skipped_count}")
    print(f"  Errors: {error_count}")
    print("="*60)
    
    if error_count == 0:
        print("\n✓ Migration completed successfully!")
        print("\nIMPORTANT: Backup your users.json file before deleting it")
        print(f"Backup command: cp {json_file_path} {json_file_path}.backup")
        return True
    else:
        print("\n⚠ Migration completed with errors")
        print("Please review the errors above")
        return False


def verify_migration():
    """Verify the migrated data"""
    print("\n" + "="*60)
    print("Verifying Migration")
    print("="*60)
    
    try:
        # Count users in database
        query = "SELECT COUNT(*) as count FROM users"
        result = DatabaseManager.execute_query(query, fetch_one=True)
        user_count = result['count'] if result else 0
        
        print(f"\nTotal users in database: {user_count}")
        
        # Show sample users
        query = """
            SELECT username, email, full_name, academic_level, profile_completed, created_at
            FROM users
            LIMIT 5
        """
        users = DatabaseManager.execute_query(query, fetch_all=True)
        
        if users:
            print("\nSample users:")
            print("-"*60)
            for user in users:
                print(f"  {user['username']} | {user['email']} | {user['full_name']}")
                print(f"    Level: {user['academic_level']} | Completed: {user['profile_completed']}")
                print(f"    Created: {user['created_at']}")
                print()
        
        print("="*60)
        print("✓ Verification complete")
        
    except Exception as e:
        print(f"✗ Verification error: {e}")


def main():
    """Main migration function"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Career Guidance App - JSON to MySQL Migration Tool     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # Check for JSON file argument
    json_file = 'users.json'
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    
    print(f"JSON file: {json_file}")
    print()
    
    # Confirm migration
    confirm = input("Do you want to proceed with migration? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Migration cancelled")
        return
    
    # Run migration
    success = migrate_json_to_mysql(json_file)
    
    if success:
        # Verify migration
        verify = input("\nDo you want to verify the migration? (yes/no): ").strip().lower()
        if verify in ['yes', 'y']:
            verify_migration()
    
    print("\nMigration script completed")


if __name__ == "__main__":
    main()
