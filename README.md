# FileShare Hub


A secure web application for storing, organizing, and sharing files built with Streamlit and Supabase.

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Secure Authentication**: User registration and login powered by Supabase Auth
- **File Upload**: Easy drag-and-drop file uploading with preview
- **File Management**: View, download, and delete your files
- **File Preview**: Built-in preview support for images, videos, audio, and PDFs
- **User Folders**: Automatic organization with user-specific folders
- **Usage Statistics**: Track your storage usage and file metrics
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Demo

https://fileshare-app-nx795r34cwfbbkdptqyro9.streamlit.app/


## 💻 Installation

### Prerequisites

- Python 3.7+
- Supabase account
- Git (optional)

### Step 1: Clone the repository

```bash
git clone https://github.com/MohammedAazam/FileShare-Hub.git
cd FileShare-Hub
```

Or download the code as a ZIP file.

### Step 2: Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Supabase Setup

1. Create a Supabase account at [https://supabase.io](https://supabase.io)
2. Create a new project
3. Set up storage:
   - Create a new bucket named `fileuploads`
   - Set appropriate bucket policies (public or private)
4. Enable Email Auth in Authentication settings

### Environment Variables

Create a `.env` file in the project root:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

### supabase_client.py

Make sure you have the `supabase_client.py` file with the following structure:

```python
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client(access_token=None, refresh_token=None):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    # Create basic client
    supabase = create_client(url, key)
    
    # If tokens are provided, set them to make authenticated requests
    if access_token and refresh_token:
        supabase.auth.set_session(access_token, refresh_token)
    
    return supabase
```

## 📋 Required Dependencies

Create a `requirements.txt` file with the following:

```
streamlit>=1.20.0
python-dotenv>=0.19.0
supabase>=0.7.1
```

## 🔧 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

### User Guide

1. **Sign Up/Login**:
   - Use the sidebar to create an account or log in
   - Verify your email if required

2. **Upload Files**:
   - Go to the "Upload Files" tab
   - Drag and drop files or click to browse
   - Click the "Upload File" button

3. **View and Manage Files**:
   - Go to the "My Files" tab to see all your uploaded files
   - Use the download button to get files
   - Use the delete button to remove files
   - Click "Preview" to view file contents when supported

4. **View Statistics**:
   - Go to the "Stats" tab to see your storage usage

## 🏗️ Architecture

### Components

- **Streamlit**: Frontend and application logic
- **Supabase Auth**: User authentication and session management
- **Supabase Storage**: File storage and management

### File Structure

```
fileshare-hub/
│
├── app.py                # Main application file
├── supabase_client.py    # Supabase connection helper
├── .env                  # Environment variables (not tracked in git)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🔐 Security

- All user authentication is handled by Supabase Auth
- Files are stored in user-specific folders based on email
- Access tokens are stored in session state
- Password requirements follow Supabase defaults

## 🌟 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

If you have any questions or feedback, please contact:
mohammedaazam757@outlook.com

---

Made with ❤️ by Mohammed Aazam
