# Insurance_agent
AI-powered Insurance Sales Agent built for Inya Buildathon 2025. Qualifies prospects, recommends life/health/motor/term policies, explains benefits &amp; exclusions, handles objections, upsells ethically, supports English &amp; Hindi on voice/chat/SMS, logs actions, and hands off to humans.

Features:
🔹 Policy Catalog – 24 mock policies (Health, Life, Term, Motor) exposed via /policies.
🔹 Quote API – Recommends policies based on customer profile.
🔹 Policy Comparison – Compare multiple policies side by side.
🔹 Rider Management – Add riders to selected policies.
🔹 Conversation Summary – Generates a summary of user profile & selected plan.
🔹 Inya.ai Integration – Sends SMS via Twilio.
🔹 PDF Support – Can serve static PDFs (e.g., policy documents).

Tech Stack:

Frameworks & Libraries:
FastAPI – Web framework for APIs
Uvicorn – ASGI server
Pydantic – Data validation
Starlette – Toolkit used under-the-hood by FastAPI

Cloud & Tools:
Render – Deployment platform
GitHub – Code hosting
Inya.ai – No-code orchestration

Integrations:
Twilio – SMS sending
