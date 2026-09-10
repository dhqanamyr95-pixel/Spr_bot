import aiosqlite

from config import DATABASE_NAME


async def init_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                invite_link TEXT NOT NULL,
                active INTEGER DEFAULT 1
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT,
                file_id TEXT,
                caption TEXT,
                duration INTEGER,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                video_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()


# =========================
# Users
# =========================

async def add_user(user_id, username=None, first_name=None):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
            INSERT OR IGNORE INTO users
            (user_id, username, first_name)
            VALUES (?, ?, ?)
        """, (
            user_id,
            username,
            first_name
        ))

        await db.commit()


async def get_user_count():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        result = await cursor.fetchone()

        return result[0]


# =========================
# Channels
# =========================

async def add_channel(channel_id, title, invite_link):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
            INSERT OR REPLACE INTO channels
            (channel_id, title, invite_link, active)
            VALUES (?, ?, ?, 1)
        """, (
            channel_id,
            title,
            invite_link
        ))

        await db.commit()


async def get_channels():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute("""
            SELECT id, channel_id, title, invite_link
            FROM channels
            WHERE active = 1
            ORDER BY id
        """)

        return await cursor.fetchall()


async def remove_channel(channel_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
            UPDATE channels
            SET active = 0
            WHERE channel_id = ?
        """, (channel_id,))

        await db.commit()


# =========================
# Videos
# =========================

async def add_video(
    source_url,
    file_id,
    caption,
    duration
):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute("""
            INSERT INTO videos
            (source_url, file_id, caption, duration)
            VALUES (?, ?, ?, ?)
        """, (
            source_url,
            file_id,
            caption,
            duration
        ))

        await db.commit()

        return cursor.lastrowid


async def get_video(video_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute("""
            SELECT
                id,
                source_url,
                file_id,
                caption,
                duration
            FROM videos
            WHERE id = ?
            AND active = 1
        """, (video_id,))

        return await cursor.fetchone()


async def
