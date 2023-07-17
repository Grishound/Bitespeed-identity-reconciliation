# Bitespeed-identity-reconciliation
Bitespeed Backend Task: Identity Reconciliation

The app is hosted on Render using their free tier, because of this the app is automatically spun down after 15 minutes of inactivity. When a new request comes in, Render spins it up again so it can process the request.
So first please send a request to : 

https://mayankp-bitespeed.onrender.com
This will give a "Not Found" error page as it is not a valid endpoint but this will spin up the application and then you can send the JSON requests at:

https://mayankp-bitespeed.onrender.com/identify
The first request might take some time. (Approximately 30 seconds). The next requests will work fine as long as the application is not left idle for more than 15 minutes.
Currently the database is empty.
