# Welcome To My Online Drug Store app!

This is a personal project that I am currently developing to test and improve my abilities as a developer!

On this website, you can:

- Search and browse for drugs
- Add drugs to your cart and (pretend to) buy them
- Match a drug based on your symptoms using an AI-powered tool
- Register and log in as a user
- View your cart and purchase history
- See detailed product information, including tags and images
- Enjoy a modern, responsive UI built with Next.js and Tailwind CSS

> **Note:** This project is for learning and demonstration purposes only. No real purchases or deliveries are made.

---

## Features

- **Product Catalog:** Browse a wide range of medications with detailed descriptions, prices, and tags.
- **AI Symptom Matcher:** Enter your symptoms to get suggested diseases and related drugs using a machine learning model.
- **User Authentication:** Register, log in, and manage your account securely.
- **Cart & Purchase History:** Add products to your cart, update quantities, and view your purchase history.
- **Admin Controls:** (Planned) Admins can add, update, unlist, or delete products.
- **Modern UI:** Clean, responsive design with custom theming and animations.
- **API-Driven:** All data is served via a Django REST API.

---

## Tech Stack

### Server

- **Language:** Python
- **Framework:** Django
- **AI/ML:** scikit-learn, joblib (RandomForestClassifier for disease prediction)
- **Database:** SQLite

### Client

- **Language:** TypeScript
- **Framework:** Next.js (App Router)
- **Styling:** Tailwind CSS + custom CSS
- **State Management:** React hooks

---

## Project Structure

```
/Backend
    manage.py
    Backend/         # Django project settings
    DrugStore/       # Django app: models, views, utils, migrations
    media/           # Uploaded product images
    db.sqlite3       # Database

/Frontend/drug_store_frontend
    src/             # Next.js app source code
    lib/             # Shared components, API, and utilities
    public/          # Static assets
    .env.local       # Environment variables
    next.config.ts   # Next.js config
```

---

## Getting Started

### Backend

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
3. **Start the server:**
   ```bash
   python manage.py runserver
   ```

### Frontend

1. **Install dependencies:**
   ```bash
   npm install
   ```
2. **Start the development server:**
   ```bash
   npm run dev
   ```
3. **Open [http://localhost:3000](http://localhost:3000) in your browser.**

---

## AI Symptom Matcher

- The backend uses a trained RandomForestClassifier to predict diseases based on user symptoms.
- Data source: [Disease and Symptoms Dataset](https://data.mendeley.com/datasets/2cxccsxydc/1)

---

## Contributing

Pull requests and suggestions are welcome! Please open an issue or submit a PR.

---

## License

This project is for educational purposes only and is not intended for real-world medical or pharmaceutical use.
