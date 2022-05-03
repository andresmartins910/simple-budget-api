# Simple Budget API - Doc

Essa API foi construída para a aplicação Simple Budget, no intuito de auxiliar no gerenciamento de gastos financeiros pessoais.

URL base: [https://simple-budget-api.herokuapp.com/](https://simple-budget-api.herokuapp.com/)

# Users

## Rotas sem autenticação

### Cadastro de um novo usuário

`POST /user - FORMATO DA REQUISIÇÃO:`

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

`POST /user - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"name": "Artemis",
	"email": "kenzinho@mail.com",
	"phone": "(27)99999-9999",
	"cpf": "123.123.123-89",
	"birthdate": "Wed, 13 Aug 1997 00:00:00 GMT"
}
```

## Rotas com autenticação

### Listagem de informações do usuário

*É necessário autenticação por Bearer Token.*

`GET /user - FORMATO DA RESPOSTA - STATUS 200`

```json
{
    "id": 1,
    "email": "kenzinho@mail.com",
    "phone": "(27)99999-9999",
    "name": "kenzinho",
    "cpf": "123.123.123-89",
    "birthdate": "13/08/1997"
}
```

### Atualização das informações de usuário

*É necessário autenticação por Bearer Token.* 

`PATCH /user - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "Kenzinho"
}
```

`PATCH /user - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"name": "Kenzinho",
	"email": "kenzinho@mail.com",
	"phone": "(27)99999-9999",
	"cpf": "123.123.123-89",
	"birthdate": "Wed, 13 Aug 1997 00:00:00 GMT"
}
```

### Deletar usuário

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`DELETE /user - REQUISIÇÃO`

`DELETE /user - FORMATO DA RESPOSTA - STATUS 204:`

```json
    "No body returned for response"
```

# Budgets

## Rotas com autenticação

### Criar budgets

*É necessário autenticação por Bearer Token.*

`POST /budgets - FORMATO DA REQUISIÇÃO:`

```json
{
	"month_year": "05/2022",
	"max_value": 3500
}
```

`POST /budgets - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 2,
	"month_year": "05/2022",
	"max_value": "3500.00"
}
```

### Atualizar budgets

*É necessário autenticação por Bearer Token.*

`PATCH /budgets/:id - FORMATO DA REQUISIÇÃO:`

```json
{
	"month_year": "06/2022",
	"max_value": 200
}
```

`PATCH /budgets/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"id": 1,
	"month_year": "06/2022",
	"max_value": "200.00"
}
```

### Obter budgets

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`GET /budgets - REQUISIÇÃO`

`GET /budgets - FORMATO DA RESPOSTA - STATUS 200:`

```json
[
	{
		"id": 1,
		"month_year": "06/2022",
		"max_value": "200.00"
	},
	{
		"id": 3,
		"month_year": "07/2022",
		"max_value": "1200.00"
	}
]
```

### Deletar budgets

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`DELETE /budgets/:id - REQUISIÇÃO`

`DELETE /budgets/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
    "No body returned for response"
```

# Expenses

## Rotas com autenticação

### Criar expense

*É necessário autenticação por Bearer Token.*

`POST /expenses - FORMATO DA REQUISIÇÃO:`

```json
{
	"name": "Pizza Hut",
	"amount": 90,
	"category_id": 1,
	"budget_id": 1
}
```

`POST /expenses - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 1,
	"name": "Pizza hut",
	"description": null,
	"amount": "90.00",
	"created_at": "Tue, 03 May 2022 11:36:08 GMT",
	"category": "Food",
	"budget": "06/2022"
}
```

### Atualizar expense

*É necessário autenticação por Bearer Token.*

`PATCH /expenses/:id - FORMATO DA REQUISIÇÃO:`

```json
{
	"amount": 120,
    "description": "4 cheese pizza"
}
```

`PATCH /expenses/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"id": 1,
	"name": "Pizza hut",
	"description": "4 cheese pizza",
	"amount": "120.00",
	"created_at": "Tue, 03 May 2022 11:36:08 GMT",
	"category": "Food",
	"budget": "06/2022"
}
```

### Obter expenses

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`GET /expenses - REQUISIÇÃO`

`GET /expenses - FORMATO DA RESPOSTA - STATUS 200:`

```json
[
	{
		"id": 2,
		"name": "Uber",
		"description": "To são paulo",
		"amount": "180.00",
		"created_at": "Tue, 03 May 2022 12:26:17 GMT",
		"category": "Transport",
		"budget": "06/2022"
	},
	{
		"id": 3,
		"name": "Pizza hut",
		"description": null,
		"amount": "120.00",
		"created_at": "Tue, 03 May 2022 12:34:09 GMT",
		"category": "Food",
		"budget": "06/2022"
	}
]
```

### Obter expense por id

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`GET /expenses/:id- REQUISIÇÃO`

`GET /expenses/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"id": 2,
	"name": "Uber",
	"description": "To são paulo",
	"amount": "180.00",
	"created_at": "Tue, 03 May 2022 12:26:17 GMT",
	"category": "Transport",
	"budget": "06/2022"
}
```

### Deletar expense

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`DELETE /expenses/:id - REQUISIÇÃO`

`DELETE /expenses/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
"No body returned for response"
```

# Categories

## Rotas com autenticação

### Criar category

*É necessário autenticação por Bearer Token.*

`POST /categories - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "Hobby",
	"description": "Everything related to hobbies"
}
```

`POST /categories - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 1,
	"name": "Hobby",
	"description": "Everything related to hobbies"
}
```

### Atualizar category

*É necessário autenticação por Bearer Token.*

`POST /categories/:id - FORMATO DA REQUISIÇÃO:`

```json
{
    "name": "Hobbies",
	"description": "Everything related to hobbies."
}
```

`POST /categories/:id - FORMATO DA RESPOSTA - STATUS 201:`

```json
{
	"id": 1,
    "name": "Hobbies",
	"description": "Everything related to hobbies."
}
```

### Obter categories

*É necessário autenticação por Bearer Token. Não possui corpo de requisição.*

`GET /categories/:id- REQUISIÇÃO`

`GET /categories/:id - FORMATO DA RESPOSTA - STATUS 200:`

```json
[
	{
		"id": 1,
		"name": "Food",
		"description": "Food related expenses"
	},
	{
		"id": 2,
		"name": "Entertainment",
		"description": "Entertainment related expenses"
	},
	{
		"id": 3,
		"name": "Transport",
		"description": "Transport related expenses"
	},
	{
		"id": 4,
		"name": "Home",
		"description": "Home related expenses"
	},
	{
		"id": 5,
		"name": "Health",
		"description": "Health related expenses"
	}
]
```

### Deletar category

`DELETE /categories/:id - REQUISIÇÃO`

`DELETE /categories/:id - FORMATO DA RESPOSTA - STATUS 204:`

```json
    "No body returned for response"
```

# Reports
