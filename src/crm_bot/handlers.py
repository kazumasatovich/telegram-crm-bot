from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from crm_bot.config import Config
from crm_bot.models import Status
from crm_bot.storage import RequestStorage

router = Router()


def setup_handlers(storage: RequestStorage, config: Config) -> Router:
    @router.message(Command("start"))
    async def cmd_start(message: Message) -> None:
        await message.answer(
            "Привет! Опишите вашу заявку одним сообщением, и мы свяжемся с вами."
        )

    @router.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        await message.answer(
            "Доступные команды:\n"
            "/start — начать\n"
            "/help — справка\n"
            "Просто напишите сообщение, чтобы оставить заявку.\n\n"
            "Для менеджеров:\n"
            "/requests — список заявок\n"
            "/status <id> <статус> — сменить статус"
        )

    @router.message(Command("requests"))
    async def cmd_requests(message: Message) -> None:
        if message.from_user is None:
            return
        if message.from_user.id not in config.manager_ids:
            await message.answer("У вас нет доступа к этой команде")
            return

        requests = storage.get_all()
        if not requests:
            await message.answer("Заявок пока нет")
            return

        lines = []
        for req in requests:
            lines.append(
                f"#{req.id} от {req.username} - {req.status.value}\n"
                f"  {req.text}"
            )
        await message.answer("\n\n".join(lines))

    @router.message(Command("status"))
    async def cmd_status(message: Message) -> None:
        if message.from_user is None:
            return
        if message.from_user.id not in config.manager_ids:
            await message.answer("У вас нет доступа к этой команде")
            return

        if message.text is None:
            return
        parts = message.text.split()
        if len(parts) != 3:
            await message.answer("Формат: /status <id> <новая/в работе/закрыта>")
            return
        try:
            req_id = int(parts[1])
        except ValueError:
            await message.answer("ID должен быть числом")
            return

        status_map = {
            "новая": Status.NEW,
            "в работе": Status.IN_PROGRESS,
            "закрыта": Status.CLOSED,
        }
        status = status_map.get(parts[2].lower())
        if status is None:
            await message.answer("Допустимые статусы: новая, в работе, закрыта")
            return

        req = storage.update_status(req_id, status)
        if req is None:
            await message.answer(f"Заявка #{req_id} не найдена")
            return
        await message.answer(f"Заявка #{req.id} переведена в статус {status.value}")

    @router.message()
    async def handle_request(message: Message) -> None:
        if message.from_user is None or message.text is None:
            return
        req = storage.add(
            user_id=message.from_user.id,
            username=message.from_user.username or "unknown",
            text=message.text,
        )
        await message.answer(f"Заявка #{req.id} принята! Мы свяжемся с вами")

    return router
