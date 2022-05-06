# Simple Budget API - Doc

Essa API foi construída para a aplicação Simple Budget, no intuito de auxiliar no gerenciamento de gastos financeiros pessoais.

URL base: [https://simple-budget-api.herokuapp.com/](https://simple-budget-api.herokuapp.com/)

# User

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

### Autenticação do usuário

`POST /user - FORMATO DA REQUISIÇÃO:`

```json
{
	"email": "kenzinho@mail.com",
	"password": "123456"
}
```

`POST /user - FORMATO DA RESPOSTA - STATUS 200:`

```json
{
	"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTY2Nzk1NiwianRpIjoiZmQwOGJjNzItNzQxMC00NmIxLWFhN2EtMjYxZmQ4YTY2YjUxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MTQsIm5hbWUiOiJKb2huIERvZSIsImVtYWlsIjoiam9obmRvZTRAZW1haWwuY29tIiwicGhvbmUiOiIoMDApMTExMTEtMTExMSIsImNwZiI6IjAwMC4wMDAuMDAwLTAwIiwiYmlydGhkYXRlIjoiTW9uLCAwMSBKYW4gMTkwMCAwMDowMDowMCBHTVQifSwibmJmIjoxNjUxNjY3OTU2LCJleHAiOjE2NTE3NTQzNTZ9.lmiQWveq8vFw5gLikkTkxIjKhwKLrT9S3Rzy2dlcwjc"
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
*É necessário autenticação por Bearer Token em TODAS as rotas de reports. Não possui corpo de requisição.*
*Filtragem de reports através de query params*


# Envio de relatórios PDF por email.

#

# *Gráfico e tabela*

## Obter relatório dos gastos por ano.
*Recebe o ano que deseja gerar o relatório.*
`GET /reports/pdf_to_mail?year=2021 - REQUISIÇÃO`



## Obter relatório dos gastos por categoria.
*Recebe o id da categoria que deseja gerar o relatório.*

`GET /reports/pdf_to_mail?category_id=3 - REQUISIÇÃO`



## Obter relatório dos gastos por período.

`GET /reports/pdf_to_mail?initial_date=01/01/2021&final_date=06/05/2022 - REQUISIÇÃO`



## Obter relatório dos gastos por ano e categoria específicos.
*Recebe o ano e o id da categoria que deseja gerar o relatório.*

`GET /reports/pdf_to_mail?year=2022&category_id=5 - REQUISIÇÃO`



## Obter relatório dos gastos por budget.
*Recebe o id do budget que deseja gerar o relatório.*

`GET /reports/pdf_to_mail/1 - REQUISIÇÃO`


# *Apenas tabela*

## Obter relatório dos gastos por ano.
*Recebe o ano que deseja gerar o relatório.*
`GET /reports/xls_to_mail?year=2021 - REQUISIÇÃO`



## Obter relatório dos gastos por categoria.
*Recebe o id da categoria que deseja gerar o relatório.*

`GET /reports/xls_to_mail?category_id=3 - REQUISIÇÃO`



## Obter relatório dos gastos por período.

`GET /reports/xls_to_mail?initial_date=01/01/2021&final_date=06/05/2022 - REQUISIÇÃO`



## Obter relatório dos gastos por ano e categoria específicos.
*Recebe o ano e o id da categoria que deseja gerar o relatório.*

`GET /reports/xls_to_mail?year=2022&category_id=5 - REQUISIÇÃO`



## Obter relatório dos gastos por budget.
*Recebe o id do budget que deseja gerar o relatório.*

`GET /reports/xls_to_mail/1 - REQUISIÇÃO`

#

# Download de relatórios.
## *Gráfico*

## Obter relatório dos gastos por ano.
*Recebe o ano que deseja gerar o relatório.*
`GET /reports/pdf?year=2021 - REQUISIÇÃO`



## Obter relatório dos gastos por categoria.
*Recebe o id da categoria que deseja gerar o relatório.*

`GET /reports/pdf?category_id=3 - REQUISIÇÃO`



## Obter relatório dos gastos por período.

`GET /reports/pdf?initial_date=01/01/2021&final_date=06/05/2022 - REQUISIÇÃO`



## Obter relatório dos gastos por ano e categoria específicos.
*Recebe o ano e o id da categoria que deseja gerar o relatório.*

`GET /reports/pdf?year=2022&category_id=5 - REQUISIÇÃO`



## Obter relatório dos gastos por budget.
*Recebe o id do budget que deseja gerar o relatório.*

`GET /reports/pdf/1 - REQUISIÇÃO`


## *Tabela*

## Obter relatório dos gastos por ano.
*Recebe o ano que deseja gerar o relatório.*
`GET /reports/xls?year=2021 - REQUISIÇÃO`



## Obter relatório dos gastos por categoria.
*Recebe o id da categoria que deseja gerar o relatório.*

`GET /reports/xls?category_id=3 - REQUISIÇÃO`



## Obter relatório dos gastos por período.

`GET /reports/xls?initial_date=01/01/2021&final_date=06/05/2022 - REQUISIÇÃO`



## Obter relatório dos gastos por ano e categoria específicos.
*Recebe o ano e o id da categoria que deseja gerar o relatório.*

`GET /reports/xls?year=2022&category_id=5 - REQUISIÇÃO`


#

## *Retorno das Rotas que foram Aceitas*

`FORMATO DA RESPOSTA - 204`


```json
	"No body returned for response"
```

#

## *Retorno das Rotas que foram Recusadas*

`FORMATO DA RESPOSTA - 204`


```json
{
	"error": "Insufficient data"
}
```
