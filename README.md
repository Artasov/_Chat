# CHAT APP

## **Project deployment**

1. Install `Docker`.
2. In the `terminal` (Windows/Linux).

    ```
    git clone https://github.com/Artasov/Chat.git
    cd Chat
    docker-compose up --build
    ```
3. Go to:
    - http://localhost:8000/ - to get started(login).
    - http://localhost:8000/signup/ - registrate.
    - http://localhost:8000/admin - Admin Panel.
    - http://localhost:8000/rooms/ - Choose or create a room.
    - http://localhost:8000/room/<slug> - Room with a name <slug>.

4. Automatically created users:
    ```
    admin - adminadmin:adminadmin
    user1 - user1:user1
    user2 - user2:user2
    ```

5. The environment variables are specified in the .env file.
    ```
    POSTGRES_NAME="adminadmin"
    POSTGRES_USER="adminadmin"
    POSTGRES_PASSWORD="adminadmin"
    POSTGRES_PORT="5432"
    DJANGO_SUPERUSER_USERNAME="adminadmin"
    DJANGO_SUPERUSER_PASSWORD="adminadmin"
    DJANGO_SUPERUSER_EMAIL="adminadmin@admin.admin"
    DEBUG="1"
    ```
   
    Использовать Postgres при больших объемах не эффективно, 
    если бы это был реальный проект я бы посмотрел на nosql бд.
    Пагинация реализована.