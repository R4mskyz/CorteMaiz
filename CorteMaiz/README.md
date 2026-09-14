# Sistema de agendamento para barbearia

## Como executar

No terminal, dentro desta pasta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000 no navegador. A documentação da API fica em http://127.0.0.1:8000/docs.

O sistema cria o banco SQLite persistente em `data/barbearia.db` e dados de teste (1 cliente, 2 barbeiros e 3 serviços) automaticamente no primeiro início. Agendamentos já gravados nunca são removidos ao reiniciar a aplicação.

As datas disponíveis vão de hoje até o último dia do próximo mês. Esse limite é validado pela tela e pela API.
