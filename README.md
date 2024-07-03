# Sustainability Tips API

An API for retrieving, adding, and managing sustainability tips across various categories.

## Overview

The Sustainability Tips API provides a platform to access and manage tips related to sustainability. Users can retrieve tips, add new tips, search for tips based on keywords, and delete tips (admin access required).

## Features

- Retrieve all tips or search tips by title, content, or category.
- Add new tips with customizable title, content, category, and author.
- Delete tips by ID (admin authentication required).

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/lululululu5/nature_appreciation.git
   cd nature_appreciation

   ```

2. **Install dependencies:**

   pip install -r requirements.txt

3. **Set up the databases:**

   python db.py
   python test_db.py

4. **Run the application:**

   flask --app main run --debug
