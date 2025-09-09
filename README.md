# 272MicroservicesArchitectureAssignment
It contains two independent services:

- **User Service** (`user_service.py`) – Manages users.
- **Order Service** (`order_service.py`) – Manages orders and communicates with the User Service.

Each service runs independently and communicates via HTTP requests.

Download the repository to your desired directory

CD to the directory you have downloaded the repository to
Create the virtual environment
python -m venv .venv

![Setup venv]<img width="521" height="22" alt="image" src="https://github.com/user-attachments/assets/b2e79700-d6c3-476e-a3c1-46ef98a9b540" />

Activate the virtual environment(windows)
.\.venv\Scripts\Activate.ps1
<img width="621" height="25" alt="image" src="https://github.com/user-attachments/assets/790a5297-9834-4ab1-a40c-759c41fdb3cd" />

Activate the virtual environment(Mac/Linux)
source .venv/bin/activate

Install the dependencies
pip install flask requests
<img width="676" height="20" alt="image" src="https://github.com/user-attachments/assets/99cb041a-0c38-44ec-abd1-1342b85b4785" />

Now, to start the User service, open a new terminal and CD to the directory
Activate the Virtual service
.\.venv\Scripts\Activate.ps1
<img width="611" height="27" alt="image" src="https://github.com/user-attachments/assets/5e5d8870-cd2f-41e3-bffd-f5c0cc4462a9" />
Then run the User service with
python .\user_service\user_service.py
<img width="1079" height="296" alt="image" src="https://github.com/user-attachments/assets/da209261-19a3-4502-b8f8-c95c675f32db" />
The User service runs on http://localhost:5001

Now, to start the order service, open a new terminal and CD to the directory
Activate the Virtual service
.\.venv\Scripts\Activate.ps1
Then run the User service with
python .\user_service\user_service.py
<img width="1097" height="201" alt="image" src="https://github.com/user-attachments/assets/8864ffda-3b64-4346-80ed-bf50efb13a35" />

Now you can test by curling a user

curl http://localhost:5001/users/1

<img width="1063" height="432" alt="image" src="https://github.com/user-attachments/assets/619f1e90-2307-47a9-8533-ea6dc2c90496" />
Which you can see on http://localhost:5001/users/1
<img width="322" height="152" alt="image" src="https://github.com/user-attachments/assets/b8bc4584-f521-4477-9a1d-3617c0a42f7b" />

You can do the same to get the user
Get a User: curl http://localhost:5001/users/1

To create an order on windows
curl.exe -X POST -H "Content-Type: application/json" `
-d "{\"user_id\":1,\"product\":\"Tablet\"}" `
http://localhost:5002/orders
<img width="924" height="163" alt="image" src="https://github.com/user-attachments/assets/5bda23f8-3403-4169-a0e0-f2f90b144c01" />

And then to Get an Order: curl http://localhost:5002/orders/1
<img width="1047" height="401" alt="image" src="https://github.com/user-attachments/assets/d83c5efe-eddf-480c-9de9-bee246be3043" />

<img width="617" height="135" alt="image" src="https://github.com/user-attachments/assets/58808b87-fb19-456c-a350-9e7350d41a60" />



