# Skelar AI: Next-Gen Operational Support & Self-Learning Ecosystem

Це інтелектуальна операційна система для клієнтської підтримки, яка трансформує роботу команди з «реактивної» на «проактивну». Наше рішення не лише автоматизує відповіді, а й **безупинно навчається на діях агентів**, самостійно виконуючи рутинні операції та гарантуючи якість вирішення кожної проблеми.

## Результати та Impact (Operational Metrics)

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

---

# English Version

# Skelar AI: Next-Gen Operational Support & Self-Learning Ecosystem

##  Impact Metrics

* **+11% Agent Efficiency Boost:** Achieved by the AI agent learning to autonomously handle Tier-2 tasks by observing and logging human decision-making.
* **Tier-1 Optimization:** Automated handling of **50+ basic query types**, significantly reducing initial support load.
* **94% Intent Accuracy:** Precision in identifying user goals from the very first interaction.
* **Guaranteed Resolution:** Drastic reduction in unresolved issues via the automated 24-hour verification pipeline.

##  Key Features

### 1. Continuous Learning & Action Logging

Every interaction and agent action is recorded in **comprehensive logs**.

* For Tier-2 tasks requiring minor human intervention, the AI observes the agent’s choices.
* By learning from these real-world actions, the AI automates repetitive workflows, resulting in an **11% increase in overall agent productivity**.

### 2. AI Copilot Sidebar 

Our advanced agent workspace, as seen in the demo, includes:

* **Real-time Intent Intelligence:** Displays user goals and AI confidence levels instantly (**94% confidence**).
* **Operational Action Buttons:** Contextual buttons (e.g., "Execute Refund") that trigger actual system-level actions directly from the sidebar.
* **Proactive Scanner:** Alerts agents to system failures or payment errors before the customer even reports them.
* **Unified History:** Displays cross-product context for all 12 Skelar brands to eliminate redundant questions.

### 3. Deterministic Analysis 

* **24h Resolution Audit:** We verify results, not just timestamps. 24 hours after a ticket is closed, the AI re-evaluates logs. If the issue persists, the system autonomously reopens the ticket with **Urgent (P0)** priority.
* **Hidden Dissatisfaction Detection:** Identifies cases where a customer is polite but their technical issue remains open.
* **Agent Performance:** Scoring (1-5) is based on action accuracy and problem resolution, not just sentiment.
