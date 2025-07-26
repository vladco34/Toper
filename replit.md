# Telegram Bot for Movie/Anime Content Management

## Overview

This is a Telegram bot built with aiogram framework that manages and distributes movie, anime, and drama content through unique codes. The bot supports partner channels for subscription verification and includes admin functionality for content management.

## User Preferences

- Preferred communication style: Simple, everyday language (Russian)
- Admin username: @Vladco34vlad 
- Bot token: 8324176530:AAHUQ0Eze7_5Jhbe3yTtIUDogHVFCFiFNeU
- Prefers button-based interaction without commands
- Wants beautiful, user-friendly message formatting

## System Architecture

### Frontend Architecture
- **Telegram Bot Interface**: The bot serves as the primary user interface using aiogram's inline keyboards and callback queries
- **State Management**: FSM (Finite State Machine) approach using aiogram's built-in state management for handling multi-step user interactions
- **Keyboard Navigation**: Custom inline keyboards for different user roles (regular users, admins) and different contexts

### Backend Architecture
- **Event-Driven Architecture**: Built on aiogram's router system with separate handlers for user and admin functionality
- **Modular Design**: Clear separation of concerns with dedicated modules for:
  - Configuration management (`config.py`)
  - Data operations (`data_manager.py`)
  - State definitions (`states.py`)
  - UI components (`keyboards.py`)
  - Business logic handlers (`handlers/`)

### Data Storage
- **File-Based Storage**: JSON files for data persistence (in root directory)
  - `movies.json`: Stores movie/content information with unique codes
  - `partners.json`: Manages partner channel information
- **In-Memory State**: Uses aiogram's MemoryStorage for temporary state management during user interactions

## Key Components

### 1. Bot Core (`main.py`)
- Bot initialization and configuration
- Router registration for user and admin handlers
- Logging setup and error handling
- Polling-based message processing

### 2. Data Management (`data_manager.py`)
- Centralized data operations for movies and partners
- JSON file handling with error recovery
- CRUD operations for content management
- Type hints and proper error handling

### 3. User Interface (`keyboards.py`)
- Dynamic keyboard generation based on context
- Support for different user roles and permissions
- Navigation between different bot sections

### 4. State Management (`states.py`)
- User states for content search workflow
- Admin states for content management operations
- Partner management states

### 5. Handler Modules (Flat Structure)
- **user_handlers.py**: Content search, partner verification, help system
- **admin_handlers.py**: Content CRUD operations, partner management, statistics

## Data Flow

### User Content Search Flow
1. User starts bot → Check partner subscriptions
2. If subscriptions valid → Show main menu
3. User selects search → Enter waiting_for_code state
4. User provides code → Query data_manager for content
5. Display content with episodes or error message

### Admin Content Management Flow
1. Admin uses /admin command → Verify admin permissions
2. Show admin menu with management options
3. For adding content: Multi-step state flow (code → title → poster → episodes)
4. Update JSON data files through data_manager
5. Provide confirmation feedback

### Partner Management Flow
1. Load partners from JSON file
2. Display partner links to users for subscription
3. Admin can add/remove partners through admin interface
4. Subscription verification (currently simplified)

## External Dependencies

### Core Framework
- **aiogram**: Modern async Telegram Bot API framework
  - Handles webhook/polling communication with Telegram
  - Provides FSM, keyboards, and routing capabilities
  - Built-in parsing and validation

### Python Standard Library
- **json**: Data serialization and file operations
- **os**: Environment variable access and file system operations
- **asyncio**: Asynchronous programming support
- **logging**: Application logging and debugging
- **typing**: Type hints for better code quality

## Deployment Strategy

### Environment Setup
- Bot token stored in environment variable `BOT_TOKEN`
- Fallback hardcoded token for development (should be removed in production)
- Admin username configured via constant

### File Structure Requirements
- All files in root directory (no subdirectories)
- JSON storage files in project root
- Automatic file creation on startup
- UTF-8 encoding for international content support
- Optimized for GitHub deployment

### Security Considerations
- Admin access controlled by username verification
- Bot token should be properly secured in production
- Partner subscription verification needs implementation

### Scalability Notes
- Current JSON file storage suitable for small to medium datasets
- Can be migrated to database (PostgreSQL/SQLite) for larger scale
- Memory storage for states - consider Redis for production clustering

## Notable Architectural Decisions

### Choice of File-Based Storage
- **Problem**: Need persistent storage for content and partner data
- **Solution**: JSON files with custom data manager
- **Rationale**: Simple deployment, no database setup required, suitable for expected data volume
- **Trade-offs**: Limited concurrent access, manual backup needs

### State Management Approach
- **Problem**: Multi-step user interactions (adding content, searching)
- **Solution**: aiogram's FSM with defined state groups
- **Rationale**: Built-in framework feature, type-safe, easy to maintain
- **Trade-offs**: Memory-based storage, states lost on restart

### Modular Handler Architecture
- **Problem**: Separation between user and admin functionality
- **Solution**: Separate router modules with permission checks
- **Rationale**: Clear separation of concerns, easier testing and maintenance
- **Trade-offs**: Slight complexity increase, but better organization