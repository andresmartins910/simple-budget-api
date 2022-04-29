<p align="center">
    Essa API foi contruída para a aplicação Simple Budget, no intuito de auxiliar no gerenciamento de gastos financeiros pessoais.
</p>

<p align="center">
   Url base da API: https://simple-budget-api.herokuapp.com/
</p>

<h2 align ='center'> Users </h2>
<h3 align ='center'> Cadastro de um novo usuário </h3>

`POST /users - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "artemis",
    "email": "kenzinho@mail.com",
	"phone": "(27)99999-9999",
    "password": "123456",
    "cpf": "123.123.123-89",
    "birthdate": "13/08/1997"
}
```

`POST /users - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"name": "Artemis",
	"email": "kenzinho@mail.com",
	"phone": "(27)99999-9999",
	"cpf": "123.123.123-89",
	"birthdate": "Wed, 13 Aug 1997 00:00:00 GMT"
}
```

<h3 align ='center'> Atualização das informações de usuário </h3>

`PATCH /users/:id - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "Kenzinho"
}
```

`PATCH /users/:id - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"name": "Kenzinho",
	"email": "kenzinho@mail.com",
	"phone": "(27)99999-9999",
	"cpf": "123.123.123-89",
	"birthdate": "Wed, 13 Aug 1997 00:00:00 GMT"
}
```

<h3 align ='center'> Deletar Usuário </h3>

<blockquote>
  O usuário autenticado pode deletar sua conta.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`DELETE /users/:id - REQUISIÇÃO`


`DELETE /users/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
"No body returned for response"
```

<h3 align ='center'> Listagem de informações do usuário </h3>

<blockquote>
  O usuário autenticado pode ver suas informações.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`GET /users - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": 1,
    "email": "kenzinho@mail.com",
    "phone": "(27)99999-9999",
    "name": "kenzinho",
    "cpf": "123.123.123-89",
    "birthdate": "13/08/1997"
  }
]
```

<h2 align ='center'> Login </h2>

`POST /login - FORMATO DA REQUISIÇÃO:`

```json
{
  "email": "kenzinho@mail.com",
  "password": "123456"
}
```

`POST /login - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImluZ3JpZHlAbWFpbC5jb20iLCJpYXQiOjE2NDMwMzEzNjQsImV4cCI6MTY0MzAzNDk2NCwic3ViIjoiMSJ9.-ZpZEy_ZkpyDjizo8JEZF6gRIfOKMS6yWBHfdVGTSN4"
}
```

<h2 align ='center'> Budgets </h2>
<h3 align ='center'> Criar Budgets </h3>

<blockquote>
  O usuário autenticado pode criar novos budgets.
</blockquote>

`POST /budgets - FORMATO DA REQUISIÇÃO:`

```json
{
	"month": "janeiro",
	"year": "2022",
	"max_value": 3000.00
}
```

`POST /budgets - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 1,
	"month": "Janeiro",
	"year": "2022",
	"max_value": "3000.00",
	"user_id": 1
}
```
<h3 align ='center'> Atualizar Budgets </h3>

<blockquote>
  O usuário autenticado pode atualizar seus budgets.
</blockquote>

`PATCH /budgets/:id - FORMATO DA REQUISIÇÃO:`

```json
{
	"max_value": 1000.00
}
```

`PATCH /budgets/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"id": 1,
	"month": "Janeiro",
	"year": "2022",
	"max_value": "1000.00",
	"user_id": 1
}
```

<h3 align ='center'> Deletar Budgets </h3>

<blockquote>
  O usuário autenticado pode deletar seus budgets.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`DELETE /budgets/:id - REQUISIÇÃO`


`DELETE /budgets/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
"No body returned for response"
```

<h3 align ='center'> Consultar Budgets </h3>

<blockquote>
  O usuário autenticado pode ver a lista dos seus budgets.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`GET /budgets - FORMATO DA RESPOSTA - STATUS 200:`

```json
[
    {
	    "id": 1,
	    "month": "Janeiro",
	    "year": "2022",
	    "max_value": "1000.00",
	    "user_id": 1
    },
    {
	    "id": 2,
	    "month": "Fevereiro",
	    "year": "2022",
	    "max_value": "3000.00",
	    "user_id": 1
    }
]
```

<h2 align ='center'> Expenses </h2>
<h3 align ='center'> Criar Expenses </h3>

<blockquote>
  O usuário autenticado pode criar novas expenses.
</blockquote>

`POST /expenses - FORMATO DA REQUISIÇÃO:`

```json
{
	"name": "Consulta",
	"description": "Exame cardiológico",
	"amount": 400.00,
}
```

`POST /expenses - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 1,
	"name": "Consulta",
	"description": "Exame cardiológico",
	"amount": "400.00",
    "created_at": "Wed, 16 Fev 2022 10:20:49 GMT",
    "budget_id": 2,
	"user_id": 1
}
```

<h3 align ='center'> Atualizar Expense </h3>

<blockquote>
  O usuário autenticado pode atualizar suas expenses.
</blockquote>

`PATCH /expenses/:id - FORMATO DA REQUISIÇÃO:`

```json
{
    "description": "Exame cardiológico com Dr. Strauss",
	"amount": 450.00
}
```

`PATCH /expenses/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"id": 1,
	"name": "Consulta",
	"description": "Exame cardiológico com Dr. Strauss",
	"amount": "450.00",
    "created_at": "Wed, 16 Fev 2022 10:20:49 GMT",
    "budget_id": 2,
	"user_id": 1
}
```

<h3 align ='center'> Deletar Expenses </h3>

<blockquote>
  O usuário autenticado pode deletar suas expenses.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`DELETE /expenses/:id - REQUISIÇÃO`


`DELETE /expenses/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
"No body returned for response"
```

<h3 align ='center'> Consultar Expenses </h3>

<blockquote>
  O usuário autenticado pode ver a lista de suas expenses.
  Obs: não possui corpo de requisição, mas nessecita do token no headers para acesso.
</blockquote>

`GET /expenses/:budget_id - FORMATO DA RESPOSTA - STATUS 200:`

```json
[
    {
	    "id": 1,
	    "name": "Consulta",
	    "description": "Exame cardiológico",
	    "amount": "400.00",
        "created_at": "Wed, 16 Fev 2022 10:20:49 GMT",
        "budget_id": 2,
	    "user_id": 1
    },
    {
	    "id": 2,
	    "name": "Compras",
	    "description": "Festa de aniversário da Nezuko",
        "created_at": "Sat, 19 Fev 2022 10:20:49 GMT",
	    "amount": "700.00",
        "budget_id": 2,
	    "user_id": 1
    }
]
```