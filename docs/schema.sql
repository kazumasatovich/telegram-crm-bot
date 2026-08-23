-- Прототип схемы находится в docs, а не в migrations, чтобы после внедрения Alembic единственным источником правды остались миграции
-- Сама схема олицетворяет фиксированное проектное решение
CREATE TABLE users (
    id bigint PRIMARY KEY,
    username text NOT NULL,
    last_message_time timestamptz NOT NULL
);

CREATE TABLE requests (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint NOT NULL REFERENCES users(id),
    status text NOT NULL CHECK (status IN ('new', 'in_progress','done')),
    created_at timestamptz NOT NULL,
    request_text text NOT NULL
);
