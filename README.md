# Привет, я Матвей (`axstiz`) 👋

📍 Екатеринбург · ✉️ litsummer@mail.ru · 💬 [@Litsummer](https://t.me/Litsummer)

AI-инженер, студент УрФУ (топ-трек «Алгоритмы ИИ»).
Проектирую AI-пайплайны с LLM, RAG и агентными архитектурами.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Apache Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)](https://kafka.apache.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/axstiz)

---

## 🔥 Проекты

### WaveScan — on-premise AI-анализатор логов кибербезопасности
*Проектный практикум УрФУ (реальный заказчик)*

Спроектировал AI-ядро пайплайна потокового анализа логов. Система читает логи через Vector → Kafka → LangGraph DAG → Postgres. Впервые совместил LLM-анализ с сигнатурными движками YARA/Sigma в одном графе.

- **8-узловой LangGraph StateGraph** с параллельными AI и детерминированными ветками
- **Гибридный RAG** (ChromaDB + BM25 + LLM re-rank) для 88 техник MITRE ATT&CK
- **Anti-hallucination**: кросс-валидация YARA (8 правил) + Sigma (9 правил)
- **F1 = 0.82** · CI/CD · Docker Compose (5 сервисов) · 16 тестов

[→ Репозиторий (личный форк)](https://github.com/axstiz/AI-CyberLogAgent)

---

## 🎓 Образование

**УрФУ, ИРИТ-РТФ** — Алгоритмы искусственного интеллекта (2025–2029)  
**Яндекс.Практикум** — Backend-разработчик (2025–2026)

---

## 🛠 Стек

| Категория | Технологии |
| --------- | ---------- |
| **Языки** | Python (asyncio, FastAPI, Pydantic, Pandas) |
| **AI / LLM** | LangGraph, LangChain, RAG, ChromaDB, Ollama, промптинг |
| **Инфраструктура** | PostgreSQL, Kafka, Docker, Git, CI/CD (GitHub Actions) |

---

## 📈 Алгоритмика

220 задач на LeetCode (78 medium, 28 hard)

![LeetCode Stats](leetcode-stats.svg)

---

## 📬 Контакты

[![Telegram](https://img.shields.io/badge/@Litsummer-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Litsummer)
[![Email](https://img.shields.io/badge/litsummer@mail.ru-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:litsummer@mail.ru)
[![GitHub](https://img.shields.io/badge/axstiz-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/axstiz)
[![Gitverse](https://img.shields.io/badge/axstiz-333?style=for-the-badge&logo=git&logoColor=white)](https://gitverse.ru/axstiz)
