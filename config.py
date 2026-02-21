"""
Secure Configuration Module
Handles all environment-based configuration for production deployment
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Base configuration with security best practices"""
    
    # Flask Core
    SECRET_KEY: str
    DEBUG: bool
    ENV: str
    
    # API Keys & Secrets (NEVER hardcode these)
    GEMINI_API_KEY: str
    
    # Database
    DATABASE_URL: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Security
    JSON_SORT_KEYS: bool = False
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        Raises ValueError if required vars are missing.
        """
        required_vars = ['SECRET_KEY', 'GEMINI_API_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please check your .env file and Render environment settings."
            )
        
        env = os.getenv('FLASK_ENV', 'production')
        debug = env == 'development'
        
        return cls(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            DEBUG=debug,
            ENV=env,
            GEMINI_API_KEY=os.getenv('GEMINI_API_KEY'),
            DATABASE_URL=os.getenv('DATABASE_URL', 'sqlite:///guardian_shield.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config() -> Config:
    """Get appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    
    if env == 'development':
        return DevelopmentConfig.from_env()
    return ProductionConfig.from_env()
