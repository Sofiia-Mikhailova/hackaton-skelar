# Skelar AI: Next-Gen Operational Support & Self-Learning Ecosystem

Це інтелектуальна операційна система для клієнтської підтримки, яка трансформує роботу команди з «реактивної» на «проактивну». Наше рішення не лише автоматизує відповіді, а й **безупинно навчається на діях агентів**, самостійно виконуючи рутинні операції та гарантуючи якість вирішення кожної проблеми.

## Структура проекту

* `src/` — основний вихідний код проекту, включаючи скрипти для аналізу та генерації даних.
* `data/` — директорія, що містить "чисті" (вхідні) дані, які використовуються для обробки та досліджень.
* `utils/` — допоміжні функції та модулі для підтримки архітектури та перевірки детермінізму.

---

## Результати та Вплив (Operational Metrics)

Впровадження системи дозволило досягти конкретних показників ефективності:

* **+11% продуктивності агентів:** AI-агент навчився самостійно виконувати прості Tier-2 завдання, аналізуючи логіку дій людини та логуючи кожен крок.
* **Оптимізація Tier-1:** Автоматизація базових запитів (**50% типів звернень**), що дозволяє максимально розвантажити лінію підтримки.
* **94% точності Intent Recognition:** Правильне визначення справжньої мети користувача (наприклад, *refund_request*) з першого повідомлення.
* **Гарантований Resolution:** Зменшення кількості "забутих" проблем завдяки автоматичному 24-годинному аудиту.

---

##  Ключові технологічні переваги

### 1. Самонавчання на діях людини (Knowledge Base Builder)

В основі системи лежить цикл безперервного вдосконалення. Усі запити, контекст та відповідні дії агентів записуються у **детальні системні логи**.

* Коли завдання (Tier-2) потребує невеликого втручання людини, AI аналізує, яку дію та відповідь обрав агент.
* На основі цих логів модель донавчається, що дозволило нам **покращити показник автономності на 11%**, мінімізуючи повторне втручання людини в аналогічні кейси.

### 2. AI Copilot Interface

Інтерактивне робоче місце агента з інтелектуальним сайдбаром (як продемонстровано на відео):

* **Live Intent Detection:** AI миттєво візуалізує намір клієнта та впевненість у ньому (**94% Confidence Score**).
* **Suggested Operational Actions:** Динамічні кнопки (наприклад, **"Execute Refund"**, **"Upgrade Plan"**), що ініціюють реальні дії в системі одним кліком.
* **Proactive Intelligence Scanner:** Окремий блок, що сигналізує про системні помилки або невдалі платежі ще до того, як клієнт напише в чат.

### 3. Детермінований аналізатор 

* **24h Resolution Check:** Система перевіряє стан тікета через 24 години після його закриття. Якщо за технічними логами проблема не зникла — AI автоматично перевідкриває тікет зі статусом **Urgent (P0)**.
* **Hidden Dissatisfaction:** AI бачить різницю між ввічливим "Thanks" та реально невиконаним запитом.
* **Agent Performance:** Автоматична оцінка базується на точності дій та вирішенні проблеми, а не лише на тоні спілкування.

---

##  Розумна пріоритезація (Priority Logic)

| Рівень пріоритету | Тип запиту (Intent) | Логіка обробки |
| --- | --- | --- |
| **URGENT (P0)** | **Refund / Payment Issue** | Фінансові запити та ризик відтоку (Churn). Миттєве сповіщення. |
| **HIGH (P1)** | **Technical Error** | Критичні баги, що заважають користуванню сервісом. |
| **NORMAL (P2)** | **Pricing / Plan Info** | Загальні питання щодо тарифів та функціоналу продуктів. |
| **LOW(P3)** | **Feedback / Other** |	Відгуки та некритичні пропозиції.|

---

## Шкала оцінювання (Quality Score)

| Бал | Статус | Критерії |
| --- | --- | --- |
| **5** | **Solved** | Проблема вирішена, SLA дотримано, клієнт задоволений. |
| **3** | **Partially Solved** | Відповідь надана, але технічна проблема може вимагати повторного звернення. |
| **1** | **Failed** | **Проблема не вирішена через 24 години**, або грубе порушення протоколу. |

---

##  Технічний запуск

1. **Встановити залежності:** `pip install -r requirements.txt`
2. **Запустити інтерфейс оператора (Streamlit):** `py -m streamlit run app.py`
3. **Запустити аналіз якості та пріоритетів:** `python src/analyze.py`

# English version
# Skelar AI: Next-Gen Operational Support & Self-Learning Ecosystem

**Skelar AI** is an intelligent operating system for customer support that transforms team workflows from "reactive" to "proactive." Our solution doesn't just automate responses; it continuously learns from human agent behavior, independently executes routine operations, and guarantees the resolution quality of every ticket.

---

##  Impact & Operational Metrics

The implementation of Skelar AI drives measurable efficiency:

* **+11% Agent Productivity**: AI autonomously handles simple Tier-2 tasks by analyzing and replicating human decision-making logic.
* **Tier-1 Optimization**: Automated 50% of basic inquiry types, significantly offloading the support line.
* **94% Intent Recognition**: High-precision identification of the user's true goal (e.g., `refund_request`) from the first message.
* **Guaranteed Resolution**: Automated 24-hour audits ensure no ticket is "forgotten" if the technical issue persists.

---

##  Key Technological Features

### 1. Self-Learning Knowledge Base Builder
The system utilizes a continuous improvement loop. All requests, contexts, and agent actions are recorded in detailed system logs.
* **Logic Analysis**: When a human resolves a Tier-2 task, the AI analyzes the chosen action.
* **Autonomous Evolution**: The model fine-tunes itself based on these logs, minimizing future human intervention for similar cases.

### 2. AI Copilot Interface
An interactive workspace featuring an intelligent sidebar:
* **Live Intent Detection**: Real-time visualization of customer intent and confidence scores.
* **Suggested Operational Actions**: Dynamic buttons (e.g., "Execute Refund", "Upgrade Plan") that trigger real-world system actions in one click.
* **Proactive Intelligence Scanner**: Flags system errors or failed payments before the customer even reaches out.

### 3. Deterministic Analyzer
* **24h Resolution Check**: Automatically re-opens tickets as **Urgent (P0)** if logs show the technical problem wasn't actually fixed.
* **Hidden Dissatisfaction**: Differentiates between a polite "Thanks" and a technically unresolved request.
* **Performance Tracking**: Scores agents based on resolution accuracy rather than just conversational tone.

---

## Logic & Scoring

### Priority Matrix
| Level | Intent (Type) | Processing Logic |
| :--- | :--- | :--- |
| **URGENT (P0)** | Refund / Payment | Financial risks & Churn prevention. Immediate alert. |
| **HIGH (P1)** | Technical Error | Critical bugs affecting core service usage. |
| **NORMAL (P2)** | Pricing / Plan Info | General product functionality and tariff inquiries. |
| **LOW (P3)** | Feedback / Other | General feedback and non-critical suggestions. |

### Quality Score (QS)
| Score | Status | Criteria |
| :--- | :--- | :--- |
| **5** | **Solved** | Problem resolved, SLA met, customer satisfied. |
| **3** | **Partially Solved** | Response sent, but technical root cause might recur. |
| **1** | **Failed** | Problem unresolved after 24h or protocol violation. |

---

##  Project Structure

* `src/` — Core source code (data analysis, generation scripts, and model logic).
* `data/` — Raw input datasets used for processing and research.
* `utils/` — Helper functions for architecture support and determinism validation.

---

##  Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

```

2. **Launch the Operator Interface (Streamlit):**
```bash
python -m streamlit run app.py

```


3. **Run Quality and Priority Analysis:**
```bash
python src/analyze.py
