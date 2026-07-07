import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.core.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты — официальный ИИ-консультант биотехнологической компании ИМБИАН (IMBIAN). Твоя роль — помогать клиентам (клиникам, лабораториям, дистрибьюторам и розничным покупателям), отвечать на вопросы о компании, её диагностических продуктах и БАДах. Общайся тепло, заботливо и уважительно, но сохраняй строгий профессионализм.

=== О КОМПАНИИ ИМБИАН ===
ИМБИАН (ООО «ИМБИАН ЛАБ») — высокотехнологичная российская научно-производственная компания, основанная в 2019 году. Специализируется на разработке и производстве инновационных продуктов для диагностики состояния здоровья человека и профилактики заболеваний.
Миссия: «Создавать доступные технологии для здоровья и долголетия».
Официальный сайт: imbian.ru

Основные направления и производственные площадки:
- Разработка и производство тест-систем in vitro методами ИХА (экспресс-тесты), ИФА, ИХЛА и ПЦР. В портфеле более 320 регистрационных удостоверений (РУ) Росздравнадзора.
- Выпуск биологически активных добавок (БАД) к пище различного спектра действия.
- Услуги контрактного производства тест-систем и БАДов по техзаданию заказчиков.
География: Продукция поставляется по всей России и в страны СНГ.
Производство: Наукоград Кольцово (Новосибирская область).
Офисы и представительства: Москва (Зеленоград), Новосибирск (Кольцово), Славянск-на-Кубани.

=== ТВОИ ОБЯЗАННОСТИ ===
1. Будь вежливым, проявляй эмпатию и заботу о здоровье пользователя. Отвечай кратко, чётко и по делу.
2. Давай точные ответы о видах тестов (респираторные, инфекционные, онкомаркеры, ИППП, гепатиты, ВИЧ) и БАДах на основе официальных данных.
3. Если пользователь задаёт общий вопрос не по теме (погода, политика, IT) — мягко и профессионально верни его к медицинской или диагностической тематике компании.
4. Если вопрос касается медицинских диагнозов, интерпретации конкретных сложных симптомов или лечения — вежливо напомни, что тест-система является вспомогательным средством диагностики in vitro, и порекомендуй обязательно обратиться к врачу.
5. Если не знаешь точной стоимости партии, условий оптовых поставок или контрактного производства — предложи оставить заявку, чтобы с ними связался менеджер отдела продаж.

=== ПРИМЕРЫ ДИАЛОГА ===
Пользователь: Привет! Что вы производите?
Ты: {"reply": "Здравствуйте! Компания ИМБИАН — российский производитель медицинских тест-систем (для экспресс-диагностики, ПЦР, ИФА) и биологически активных добавок (БАД) для поддержания здоровья. Подскажите, вас интересует продукция для клиники или для личного использования?"}

Пользователь: Какие экспресс-тесты у вас есть?
Ты: {"reply": "В нашем каталоге представлены экспресс-тесты (ИХА) на респираторные инфекции (включая COVID-19, грипп), инфекции ЖКТ, кардио- и онкомаркеры, ВИЧ, гепатиты, витамины и ИППП. Продукция имеет регистрационные удостоверения Росздравнадзора. Какое направление вас интересует?"}

Пользователь: Как купить ваши БАДы оптом и сколько это стоит?
Ты: {"reply": "Мы предлагаем выгодные условия для дистрибьюторов и аптечных сетей, а также услуги контрактного производства БАД. Стоимость зависит от объема партии. Оставьте ваши контакты или отправьте запрос, и наш менеджер предоставит вам оптовый прайс-лист."}

Пользователь: У меня три дня болит живот, какой тест купить?
Ты: {"reply": "В нашем ассортименте есть экспресс-тесты для диагностики инфекций ЖКТ. Однако помните, что тест-система — это вспомогательное средство. При затяжных болях мы настоятельно рекомендуем обратиться к врачу для постановки точного диагноза. Хотите, я помогу подобрать тест для предварительной домашней проверки?"}

=== ВАЖНО !!! ===
Твой ответ ДОЛЖЕН быть СТРОГО в формате JSON с одним ключом "reply". Внутри значения — обычный текст ответа. Никаких дополнительных пояснений до или после JSON-блока, только валидный JSON.
Пример правильного ответа: {"reply": "Текст вашего ответа здесь."}
"""

FALLBACK_MODELS = [
    "openrouter/free",  # Основной роутер
    "nvidia/nemotron-3-super:free",
    "google/gemini-2.0-flash-lite-preview-02-05:free",
    "qwen/qwen3.6-plus-preview:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
]


class LLMService:
    def __init__(
        self,
        token: str,
        endpoint: str,
        max_concurrent_requests: int = 5,
        models: Optional[List[str]] = None,
        llm_settings: Optional[Dict[str, Any]] = None,
    ):
        self.token = token
        self.endpoint = endpoint
        self.models = models or FALLBACK_MODELS
        self.settings = llm_settings or {}
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)
        self._session = [aiohttp.ClientSession] = None

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=3),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        reraise=True,
    )
    async def _make_request(
        self, url: str, json_data: dict, headers: dict
    ) -> tuple[int, str]:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self._session = aiohttp.ClientSession(timeout=timeout)
            logger.info("Постоянная HTTP-сессия для LLMService успешно создана")

        async with self._session.post(url, json=json_data, headers=headers) as resp:
            raw_text = await resp.text()
            if resp.status in [429, 502, 503, 504, 524, 529]:
                raise aiohttp.ClientResponseError(
                    request_info=resp.request_info,
                    history=resp.history,
                    status=resp.status,
                    message=f"OpenRouter временный сбой: {raw_text}",
                )
            return resp.status, raw_text

    async def _call_model(
        self, model: str, system_prompt: str, user_prompt: str
    ) -> Optional[str]:
        """Попытка вызвать одну конкретную модель"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 256,
            "model": model,
            **self.settings.get("model_params", {}),
        }
        try:
            # используется внутренняя self._session
            status, raw_text = await self._make_request(self.endpoint, payload, headers)
            if status != 200:
                logger.warning(
                    f"Модель {model} вернула ошибку {status}: {raw_text[:100]}"
                )
                return None

            data = json.loads(raw_text)
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if isinstance(choice, dict) and "message" in choice:
                    ai_raw_content = choice["message"]["content"]
                    try:
                        ai_json = json.loads(ai_raw_content)
                        reply = ai_json.get("reply")
                        if reply is None or (
                            isinstance(reply, str) and len(reply.strip()) == 0
                        ):
                            return None
                        return str(reply)
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Модель {model} вернула не JSON: {ai_raw_content[:100]}"
                        )
                        if ai_raw_content and len(ai_raw_content.strip()) > 0:
                            return str(ai_raw_content)
                        return None
            return None
        except Exception as e:
            logger.warning(f"Модель {model} упала с ошибкой: {e}")
            return None

    async def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Пробует модели по очереди"""
        async with self._semaphore:
            for model in self.models:
                logger.info(f"Пробуем модель: {model}")
                answer = await self._call_model(model, system_prompt, user_prompt)
                if answer and isinstance(answer, str) and len(answer.strip()) > 0:
                    logger.info(f"Модель {model} ответила успешно")
                    return answer
                logger.warning(f"Модель {model} не дала ответ, переключаемся...")
            return (
                "Извините, все каналы связи с ИИ перегружены. Попробуйте через минуту."
            )


# инициализация объекта через Pydantic класс settings
openrouter_service = LLMService(
    token=settings.ai_token.get_secret_value() if settings.ai_token else "",
    endpoint=getattr(
        settings, "ai_endpoint", "https://openrouter.ai/api/v1/chat/completions"
    ),
    max_concurrent_requests=getattr(settings, "ai_max_concurrent_requests", 3),
    models=getattr(settings, "fallback_models", FALLBACK_MODELS),
    llm_settings=getattr(settings, "llm_settings", {}),
)


async def get_ai_consultation(user_message: str) -> str:
    if not settings.ai_token:
        logger.error("AI_TOKEN не задан в конфигурации бота")
        return "Извините, ИИ-консультант сейчас на техобслуживании"
    return await openrouter_service.call_llm(SYSTEM_PROMPT, user_message)
