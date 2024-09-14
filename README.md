# Django Project with MongoDB and PostgreSQL

## Pre-requisites

    Docker
    Docker Compose

## Getting Started
Clone the Repository

    git clone https://github.com/yourusername/yourrepository.git

Configure Your Environment

    Create a .env file in the root directory with the necessary environment variables. An example .env file can be provided.

Initialize the Environment

Run the following script to set up the environment for the first time, including creating a superuser:

    bash/init_environment.bat

Start the Environment

For subsequent runs, you can start the environment with:

    bash/start_environment.bat

Apply Migrations

To apply any new migrations, use:

    bash/apply_migrations.bat

Create a Superuser

To create a superuser (if needed), run:

    bash/create_superuser.bat

File Descriptions

init_environment.bat: 
    
    Sets up the environment for the first time, including migrations and superuser creation.

start_environment.bat:

    Starts the Docker containers for subsequent runs.

apply_migrations.bat:
    
    Applies any new migrations to the database.

create_superuser.bat:
    
    Creates a Django superuser.
