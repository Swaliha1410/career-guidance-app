"""
Database Connection Manager for Career Guidance Application
Handles MySQL database connections with connection pooling
"""

import mysql.connector
from mysql.connector import pooling, Error
from typing import Optional
import logging
from db_config import DB_CONFIG, POOL_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages MySQL database connections using connection pooling"""
    
    _pool = None
    
    @classmethod
    def initialize_pool(cls):
        """Initialize the connection pool"""
        try:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name=POOL_CONFIG['pool_name'],
                pool_size=POOL_CONFIG['pool_size'],
                pool_reset_session=POOL_CONFIG['pool_reset_session'],
                **DB_CONFIG
            )
            logger.info("Database connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._pool is None:
            cls.initialize_pool()
        
        try:
            connection = cls._pool.get_connection()
            return connection
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
    
    @classmethod
    def test_connection(cls) -> bool:
        """Test database connection"""
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            logger.info("Database connection test successful")
            return True
        except Error as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    @classmethod
    def execute_query(cls, query: str, params: Optional[tuple] = None, fetch_one: bool = False, fetch_all: bool = False):
        """
        Execute a database query
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
            fetch_one: Whether to fetch one result
            fetch_all: Whether to fetch all results
            
        Returns:
            Query result or None
        """
        conn = None
        cursor = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid if cursor.lastrowid else None
            
            conn.commit()
            return result
            
        except Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @classmethod
    def close_pool(cls):
        """Close all connections in the pool"""
        if cls._pool:
            # Connection pools don't have a direct close method
            # Connections are automatically closed when program exits
            logger.info("Database pool cleanup initiated")


# Initialize pool on module import
try:
    DatabaseManager.initialize_pool()
except Exception as e:
    logger.warning(f"Could not initialize database pool on import: {e}")
    logger.warning("Pool will be initialized on first connection attempt")
