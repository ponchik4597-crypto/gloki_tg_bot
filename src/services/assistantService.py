import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

# import aiosqlite


class AssistantService:
    def __init__(
        self, chat_service, rate_limiter, msg_repository, search_engine, mail_service
    ):
        self.chat_service = chat_service
        self.rate_limiter = rate_limiter
        self.msg_repository = msg_repository
        self.search_engine = search_engine
        self.mail_service = mail_service

    def initialize(self, documents: List[str]):
        """Загружает документы в SearchEngine при старте"""
        self.search_engine.add_documents(documents)

    async def process_message(self, user_id: str, chat_id: str, message: str) -> str:
        pass

    async def process_user_reaction(self):
        pass


class RateLimiter:
    """Проверяет лимиты пользователя: длину сообщения и частоту запросов"""

    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings
        self._user_requests = defaultdict(list)
        self.max_message_length = settings.get("max_message_length", 1000)
        self.limits = settings.get(
            "limits",
            {
                "second": 5,
                "minute": 30,
                "day": 1000,
            },
        )

    def check_limits(self, user_id: str, message: str) -> Tuple[bool, Optional[str]]:
        """Проверяет не превышены ли лимиты"""
        if len(message) > self.max_message_length:
            return False, f"Сообщение превышает {self.max_message_length} символов"

        now = time.time()
        # удалить записи, если им больше 1 дня
        self._user_requests[user_id] = [
            t for t in self._user_requests[user_id] if now - t < 86400
        ]

        for period, limit in self.limits.items():
            window = {"second": 1, "minute": 60, "day": 86400}.get(period, 60)
            count = sum(1 for t in self._user_requests[user_id] if now - t < window)
            if count >= limit:
                return False, f"Превышен лимит. {limit} запросов за период {period}"
        return True, None

    def record_request(self, user_id):
        """Добавляет timestamp после успешного запросы"""
        self._user_requests[user_id].append(time.time())


class MessageRepository:
    """это для работы с базой данных, для хранения истории, получения контекста и сохранения реакций
    атрибуты:
    db_path - путь к SQLite-файлу
    методы:
    initialize() - создает таблицы
    get_chat_context(chat_id, limit) -> List[Dict] - возвращает посление N сообщений
    save_interaction(user_id, chat_id, user_msg, bot_response) -> int - сохраняет пару пользователь-бот, вернет ID
    save_user_feedback(interaction_id, feedback_type) - лайк/дизлайк"""

    pass


class SearchEngine:
    """Индексирует набор текстовых документов и позволяет выполнять по ним поиск по ключевым словам"""

    def __init__(self):
        self.documents: List[str] = []  # Каждый элемент - один документ

    """принимает список строк и добавляет их в список documents"""

    def add_documents(self, document: List[str]):
        self.documents.extend(document)

    """возвращает документы со словами из поиска, если запрос пустой - возвращает пустой список"""

    def search_documents(self, query: str, top_k: int = 3) -> List[str]:
        if not query.strip():
            return []
        query_words = set(query.lower().split())
        result = []
        for doc in self.documents:
            doc_words = set(doc.lower().split())
            if query_words.issubset(doc_words):
                result.append(doc)
                if len(result) >= top_k:
                    break
        return result
