# Connection with Deta database

- this is a feature branch to test the connection with a Deta database
- in this db, there's a collection with the following item definition:
  - `key`: string, also identified as `username`
  - `created_at`: string
  - `password`: string
  - `name`: string
```
{
	"key": "test",
	"created_at": "2023-08-12 14:47:16.553886",
	"email": "test@gmail.com",
	"name": "test",
	"password": hashed_password
}
```
- there's a local `stauth` (streamlit_authenticator) repo because the one in the initial repo has a very weak check on email validity
- password is encrypted by streamlit_authenticator, using `bcrypt`
- how to run: `streamlit run main.py --server.headless true`