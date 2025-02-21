DROP TABLE IF EXISTS "reaction_events";

CREATE TABLE "reaction_events" (
    -- айди чата для того, чтобы для каждого чата было уникальный буллинг
    "chat_id" BIGINT NOT NULL,
    -- айди пользователя для буллинга
    "user_id" BIGINT NOT NULL,
    -- какой эмодзи будет ставить
    "emoji" VARCHAR(255) NOT NULL,
    -- сколько по времени бот будет ставить реакции на этого пользователя
    "event_duration" INTERVAL NOT NULL,
    -- со скольки данный ивент начался
    "event_start" TIMESTAMP NOT NULL,
    PRIMARY KEY("chat_id", "user_id")
);

