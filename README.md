
# **Maor Geter - User Management API**

**Recommendation:**

I recommend watching **Explanition.mov** for a clear walkthrough of the setup and how everything works. It’ll help you understand the system better.

I'm not able to upload it to GitHub due to file size limitations, but you can watch it here: [Google drive](https://drive.google.com/file/d/1x11J7CT0T9UEjLQmC-SCKmC-61O1TKOk/view?usp=sharing)

## **Overview**

This is a **Flask-based User Management Application** integrated with MongoDB, Prometheus, Grafana, and JWT authentication. The UI allows users to view the user list, but all modifications (create, update, delete) require authentication.

## **Features**

- **Flask Backend** - Chosen due to familiarity and prior experience, making development structured and efficient. Flask is a lightweight and flexible framework, well-suited for small applications with  **easy API handling** .

* **MongoDB** - Selected for its  **seamless integration with Flask and Python** , along with its flexibility as a NoSQL database. It allows dynamic schema modifications, making it  **adaptable for evolving application requirements** .
* **Prometheus & Grafana** - Prometheus  **collects real-time metrics** , while Grafana **visualizes performance data** with structured dashboards. This combination helps in  **monitoring API health and detecting issues quickly** .
* **Swagger UI** - A powerful API documentation tool that integrates well with Flask, making API  **testing and interaction more user-friendly** .
* **JWT Security** - Implements **authentication and authorization** to protect API endpoints. Only  **read operations (viewing users) are public** , while modifications (create, update, delete) require  **valid authentication** .

## Installation

```
git clone https://github.com/maorgeter/be.git
cd be
```

first run will be run with --build flag:

```
docker compose up --build -d
```

## Important links

* **User Management UI** : [http://localhost:5001/]()
* **Grafana Dashboard** : [http://localhost:3000/]()
* **Swagger API Docs** : [http://localhost:5000/apidocs]()

## Important Configuration Details

* **Admin Credentials**
  * In `app.py`, the admin credentials are  **hardcoded** :
    * **Email:** `maor@geter.com`
    * **Password:** `smartech`
  * These credentials are used to generate a **JWT token** for authentication.
* **MongoDB Connection**
  * The `database.py` file contains two MongoDB URIs for different environments:
    * **Docker Running:** `mongodb://mongo:27017`
    * **Local Running:** `mongodb://localhost:27017`
  * The application uses the correct  **URI based on the environment** .
* **Test Environment**
  * The `test_app.py` file is designed to run  **only in a local environment** .
  * Tests authenticate using the **hardcoded admin credentials** and interact with a local MongoDB instance.
  * **Ensure MongoDB is running locally before running tests.**
