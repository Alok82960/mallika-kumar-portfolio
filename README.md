# Dr. Mallika Kumar Portfolio

This is a complete, secure, and production-ready full-stack web application for Dr. Mallika Kumar's portfolio.

## Tech Stack
- **Frontend**: Vanilla HTML/CSS/JS (Securely interacts with the backend API)
- **Backend**: Node.js + Express
- **Database**: MongoDB (via Mongoose)
- **Security**: JWT Authentication, bcrypt password hashing, Helmet

## Features Added for Security & Deployment
1. **Real Backend**: Replaced insecure browser `localStorage` with a robust Node.js API.
2. **Database Integration**: Portfolio state and contact messages are securely saved in MongoDB.
3. **Secure Authentication**: Admin login uses bcrypt for password hashing and JSON Web Tokens (JWT) for secure session management.
4. **File Uploads**: Base64 strings are replaced by actual file uploads using `multer`. Images are saved in the `backend/uploads/` directory.

## Local Development Setup

1. **Install Dependencies**
   Navigate to the project root and install the required npm packages:
   ```bash
   npm install
   ```

2. **Configure Environment Variables**
   Open the `.env` file in the project root and set the following:
   - `MONGO_URI`: The connection string for your MongoDB database (e.g., MongoDB Atlas URI).
   - `PORT`: The port the server will run on (default 5000).
   - `JWT_SECRET`: A long, random string used to sign session tokens.
   - `ADMIN_PASSWORD`: The password you want to use to access the admin panel.

3. **Start the Server**
   ```bash
   npm start
   ```
   The application will be accessible at `http://localhost:5000`.

## Deployment Guide

To deploy this application to a service like Render, Heroku, or Vercel:

1. Connect your GitHub repository to your chosen hosting provider.
2. Set the **Build Command** to `npm install`.
3. Set the **Start Command** to `node backend/server.js`.
4. In the hosting provider's dashboard, add all the environment variables from your `.env` file (especially your `MONGO_URI` and `JWT_SECRET`).
5. Ensure your MongoDB Atlas cluster allows incoming connections from anywhere (`0.0.0.0/0`) if you are deploying to a cloud provider with dynamic IPs.
