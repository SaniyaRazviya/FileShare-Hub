import streamlit as st
from supabase_client import get_client
import os
import time
import base64
import mimetypes
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="FileShare Hub",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size:  3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .file-card {
        border-radius: 8px;
        background-color: #000000;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #eee;
        transition: all 0.3s;
    }
    .file-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-color: #ccc;
    }
    .file-name {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 5px;
        color: #ffffff;
    }
    .file-info {
        font-size: 14px;
        color: #ffffff;
    }
    .file-actions {
        display: flex;
        gap: 10px;
    }
    .stButton button {
        border-radius: 20px;
    }
    .upload-area {
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .preview-image {
        max-width: 100%;
        max-height: 200px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .sidebar-title {
        font-weight: 700;
        color: #1E88E5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #000000;
        border-radius: 4px 4px 0px 0px;
        gap: 6px;
        padding-top: 10px;
        padding-right: 10px;
        padding-left: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0077FF;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize basic client for auth operations
supabase = get_client()

# -------------------------
# Helper Functions
# -------------------------

def get_file_icon(mime_type):
    """Return an appropriate icon for file type"""
    if mime_type.startswith('image/'):
        return "🖼️"
    elif mime_type.startswith('video/'):
        return "🎬"
    elif mime_type.startswith('audio/'):
        return "🎵"
    elif mime_type.startswith('text/'):
        return "📝"
    elif 'pdf' in mime_type:
        return "📑"
    elif 'word' in mime_type or 'document' in mime_type:
        return "📄"
    elif 'excel' in mime_type or 'spreadsheet' in mime_type:
        return "📊"
    elif 'presentation' in mime_type or 'powerpoint' in mime_type:
        return "📽️"
    elif 'zip' in mime_type or 'compressed' in mime_type:
        return "🗜️"
    else:
        return "📁"

def format_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.1f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.1f} GB"

def get_file_preview(file_url, mime_type, file_name):
    """Generate preview HTML based on file type"""
    if mime_type.startswith('image/'):
        return f'<img src="{file_url}" class="preview-image" alt="{file_name}">'
    elif mime_type.startswith('video/'):
        return f'<video controls width="100%" height="200"><source src="{file_url}" type="{mime_type}">Your browser does not support video preview.</video>'
    elif mime_type.startswith('audio/'):
        return f'<audio controls style="width:100%"><source src="{file_url}" type="{mime_type}">Your browser does not support audio preview.</audio>'
    elif mime_type == 'application/pdf':
        return f'<iframe src="{file_url}" width="100%" height="200" style="border:none;"></iframe>'
    else:
        # For other file types, show a simple icon
        return f'<div style="text-align:center; font-size:64px;">{get_file_icon(mime_type)}</div>'

# -------------------------
# Sidebar Authentication
# -------------------------
if "user" not in st.session_state:
    with st.sidebar:
        st.markdown('<p class="sidebar-title">🔑 Authentication</p>', unsafe_allow_html=True)
        
        action = st.radio("", ["Sign In", "Sign Up"], horizontal=True, label_visibility="collapsed")
        
        with st.form(key="auth_form"):
            email = st.text_input("📧 Email", placeholder="youremail@example.com")
            password = st.text_input("🔒 Password", type="password", placeholder="********")
            submit_btn = st.form_submit_button("Login" if action == "Sign In" else "Register", use_container_width=True)
            
            if submit_btn:
                if action == "Sign Up":
                    try:
                        result = supabase.auth.sign_up({"email": email, "password": password})
                        st.success("✅ Check your email to confirm registration.")
                    except Exception as e:
                        st.error(f"❌ Registration error: {str(e)}")
                else:  # Sign In
                    try:
                        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        if auth_response.session:
                            # Store both user info and session tokens for later use
                            st.session_state["user"] = auth_response.user
                            st.session_state["access_token"] = auth_response.session.access_token
                            st.session_state["refresh_token"] = auth_response.session.refresh_token
                            st.success("✅ Logged in successfully!")
                            time.sleep(1)
                             # Rerun to refresh the page with the new user
                        else:
                            st.error("❌ Invalid credentials")
                    except Exception as e:
                        st.error(f"❌ Login error: {str(e)}")
        
        st.markdown("""
        ### Welcome to FileShare Hub
        
        A secure platform for storing and sharing your files.
        
        ✨ Features:
        - 🔒 Secure authentication
        - 📤 Easy file uploads
        - 📥 Convenient downloads
        - 👀 File previews
        """)
else:
    # If logged in, only show minimal sidebar with user info and logout
    with st.sidebar:
        user = st.session_state["user"]
        st.markdown(f"""
        <div style="text-align:center; padding: 10px; background-color:#000000; border-radius:10px; margin-bottom:20px;">
            <div style="font-size:40px;">👤</div>
            <div style="font-weight:bold; font-size:18px; color:#ffffff;">{user.email}</div>
            <div style="font-size:12px; color:#666;">Logged in since {datetime.now().strftime('%H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            try:
                supabase.auth.sign_out()
            except:
                pass  # Ignore errors during logout
            
            # Clear session state
            for key in ["user", "access_token", "refresh_token"]:
                if key in st.session_state:
                    st.session_state.pop(key)
            
            st.success("Logged out successfully!")
            time.sleep(1)
            
        
        # Add some useful info
        st.markdown("""
        ### 💡 Tips
        
        - Files are organized in your personal folder
        - Preview supported for images, audio, video and PDF
        - Click on file names to view details
        
        Need help? Contact support@fileshare.com
        """)

# -------------------------
# App Logic After Login
# -------------------------
if "user" in st.session_state:
    user = st.session_state["user"]
    
    # IMPORTANT: Get an authenticated Supabase client using both tokens
    authenticated_supabase = get_client(
        access_token=st.session_state["access_token"],
        refresh_token=st.session_state["refresh_token"]
    )

    # Main content
    st.markdown('<h1 class="main-header">📁 FileShare Hub</h1>', unsafe_allow_html=True)
    
    # Create tabs for upload and view functionality
    tabs = st.tabs(["📤 Upload Files", "📋 My Files", "📊 Stats"])
    
    with tabs[0]:  # Upload Files tab
        st.markdown('<p class="sub-header">Upload New Files</p>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Choose a file to upload", accept_multiple_files=False, label_visibility="collapsed")
            
            if uploaded_file:
                file_details = {
                    "Filename": uploaded_file.name,
                    "File size": format_size(uploaded_file.size),
                    "File type": uploaded_file.type if uploaded_file.type else "Unknown"
                }
                
                # Display file details
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"<div style='font-size:50px; text-align:center;'>{get_file_icon(uploaded_file.type)}</div>", unsafe_allow_html=True)
                
                with col2:
                    for key, value in file_details.items():
                        st.markdown(f"**{key}:** {value}")
                
                # Upload button
                if st.button("📤 Upload File", type="primary", use_container_width=True):
                    try:
                        # Create a folder path using the user's email
                        user_folder = user.email.split('@')[0]  # Use username part of email
                        path_on_supabase = f"{user_folder}/{uploaded_file.name}"

                        # Read file content
                        file_data = uploaded_file.read()

                        # Upload to Supabase with authenticated client
                        result = authenticated_supabase.storage.from_("fileuploads").upload(
                            path_on_supabase,
                            file=file_data,
                            file_options={"content-type": uploaded_file.type}
                        )
                        
                        st.success("✅ File uploaded successfully!")
                        time.sleep(1)  # Give a moment for the success message to be seen
                         # Refresh to update file list
                        
                    except Exception as e:
                        st.error(f"❌ Error uploading file: {str(e)}")
            else:
                st.markdown("""
                    <div style="text-align:center; padding:30px;">
                        <div style="font-size:40px; margin-bottom:20px;">🔽</div>
                        <div style="color:#666;">Drag and drop your files here or click to browse</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
                
    
    with tabs[1]:  # My Files tab
        st.markdown('<p class="sub-header">My Files</p>', unsafe_allow_html=True)
        try:
            # Get user folder name from email (same logic as when uploading)
            user_folder = user.email.split('@')[0]
            
            # Create a button to refresh the file list
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 Refresh", use_container_width=True):
                    file_list = authenticated_supabase.storage.from_("fileuploads").list(user_folder)
            
            if not file_list:
                st.info("📂 You haven't uploaded any files yet.")
                st.markdown("""
                    <div style="text-align:center; padding:50px; color:#666;">
                        <div style="font-size:60px;">🗂️</div>
                        <div style="margin-top:20px;">Your files will appear here after upload</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Define a safer format_size function in case the original is causing issues
                def safe_format_size(size_bytes):
                    """
                    A safer version that ensures we're working with integers
                    """
                    try:
                        # Make sure we have an integer
                        if not isinstance(size_bytes, (int, float)):
                            try:
                                size_bytes = int(float(str(size_bytes).strip()))
                            except (ValueError, TypeError):
                                size_bytes = 0
                        
                        # Now format the size
                        if size_bytes < 1024:
                            return f"{size_bytes} B"
                        elif size_bytes < 1024 * 1024:
                            return f"{size_bytes/1024:.1f} KB"
                        elif size_bytes < 1024 * 1024 * 1024:
                            return f"{size_bytes/(1024*1024):.1f} MB"
                        else:
                            return f"{size_bytes/(1024*1024*1024):.1f} GB"
                    except Exception as e:
                        print(f"Error in safe_format_size: {e}")
                        return "0 B"

                # Display files with download and delete options
                for file_info in file_list:
                    try:
                        file_name = file_info['name']
                        
                        # More robust size handling
                        try:
                            file_size_value = file_info.get('metadata', {}).get('size', 0)
                            if file_size_value is None:
                                file_size_value = 0
                            
                            # Try using our safer function
                            file_size = safe_format_size(file_size_value)
                        except Exception as e:
                            print(f"Error processing file size for {file_name}: {e}")
                            file_size = "Unknown"
                        
                        file_path = f"{user_folder}/{file_name}"
                        
                        # Safer timestamp handling
                        try:
                            created_at = file_info.get("Added on", 0)
                            if created_at is None:
                                created_at = 0
                            
                            # Convert string timestamp to integer if needed
                            if isinstance(created_at, str):
                                created_at = int(float(created_at))
                            elif not isinstance(created_at, (int, float)):
                                created_at = 0
                                
                            last_modified = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M")
                        except Exception as e:
                            print(f"Error processing timestamp for {file_name}: {e}")
                            last_modified = "Unknown date"
                        
                        # Guess the mime type from file extension
                        mime_type, _ = mimetypes.guess_type(file_name)
                        mime_type = mime_type if mime_type else "application/octet-stream"
                        
                        # Create a container for each file with actions
                        with st.container():
                            st.markdown(f'<div class="file-card">', unsafe_allow_html=True)
                            
                            # File name and basic info
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                st.markdown(f'<div class="file-name">{get_file_icon(mime_type)} {file_name}</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="file-info">Size: {file_size} • Last modified: {last_modified}</div>', unsafe_allow_html=True)
                            
                            with col2:
                                # Generate a download URL
                                file_url = authenticated_supabase.storage.from_("fileuploads").get_public_url(file_path)
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown(f'<a href="{file_url}" target="_blank"><button style="border-radius:20px; padding:2px 10px; background-color:#2E7D32; color:white; border:none; width:100%;">📥</button></a>', unsafe_allow_html=True)
                                
                                with col_b:
                                    # Create a unique key for each delete button
                                    delete_key = f"delete_{file_name}"
                                    
                                    # Create a session state key for each file's delete confirmation
                                    confirm_key = f"confirm_delete_{file_name}"
                                    if confirm_key not in st.session_state:
                                        st.session_state[confirm_key] = False
                                    
                                    if st.session_state[confirm_key]:
                                        if st.button("✓", key=f"confirm_{delete_key}", help="Confirm deletion"):
                                            authenticated_supabase.storage.from_("fileuploads").remove([file_path])
                                            st.success(f"✅ Deleted {file_name}")
                                            st.session_state[confirm_key] = False
                                            time.sleep(1)
                                            
                                        if st.button("✗", key=f"cancel_{delete_key}", help="Cancel deletion"):
                                            st.session_state[confirm_key] = False
                                            
                                    else:
                                        if st.button("🗑️", key=delete_key, help="Delete file"):
                                            st.session_state[confirm_key] = True
                                            
                            
                            # File preview
                            with st.expander("Preview"):
                                file_url = authenticated_supabase.storage.from_("fileuploads").get_public_url(file_path)
                                st.markdown(get_file_preview(file_url, mime_type, file_name), unsafe_allow_html=True)
                                st.markdown(f'<a href="{file_url}" target="_blank" style="text-decoration:none;"><button style="margin-top:10px; width:100%; padding:5px; background-color:#1976D2; color:white; border:none; border-radius:4px;">Open in New Tab</button></a>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error processing file {file_info.get('name', 'unknown')}: {e}")
                        print(f"Detailed error for file: {e}")
                        continue  # Skip to the next file if there's an error
                        
                        with col2:
                            # Generate a download URL
                            file_url = authenticated_supabase.storage.from_("fileuploads").get_public_url(file_path)
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown(f'<a href="{file_url}" target="_blank"><button style="border-radius:20px; padding:2px 10px; background-color:#2E7D32; color:white; border:none; width:100%;">📥</button></a>', unsafe_allow_html=True)
                            
                            with col_b:
                                # Create a unique key for each delete button
                                delete_key = f"delete_{file_name}"
                                
                                # Create a session state key for each file's delete confirmation
                                confirm_key = f"confirm_delete_{file_name}"
                                if confirm_key not in st.session_state:
                                    st.session_state[confirm_key] = False
                                
                                if st.session_state[confirm_key]:
                                    if st.button("✓", key=f"confirm_{delete_key}", help="Confirm deletion"):
                                        authenticated_supabase.storage.from_("fileuploads").remove([file_path])
                                        st.success(f"✅ Deleted {file_name}")
                                        st.session_state[confirm_key] = False
                                        time.sleep(1)
                                        
                                    if st.button("✗", key=f"cancel_{delete_key}", help="Cancel deletion"):
                                        st.session_state[confirm_key] = False
                                        
                                else:
                                    if st.button("🗑️", key=delete_key, help="Delete file"):
                                        st.session_state[confirm_key] = True
                                        
                        
                        # File preview
                        with st.expander("Preview"):
                            file_url = authenticated_supabase.storage.from_("fileuploads").get_public_url(file_path)
                            st.markdown(get_file_preview(file_url, mime_type, file_name), unsafe_allow_html=True)
                            st.markdown(f'<a href="{file_url}" target="_blank" style="text-decoration:none;"><button style="margin-top:10px; width:100%; padding:5px; background-color:#1976D2; color:white; border:none; border-radius:4px;">Open in New Tab</button></a>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating statistics: {str(e)}")        
    
    with tabs[2]:  # Stats tab
        st.markdown('<p class="sub-header">Storage Statistics</p>', unsafe_allow_html=True)
        
        try:
            # Get user folder name from email
            user_folder = user.email.split('@')[0]
            
            # List files in the user's folder
            file_list = authenticated_supabase.storage.from_("fileuploads").list(user_folder)
            
            # Calculate statistics
            total_files = len(file_list)
            total_size = sum(file_info.get('metadata', {}).get('size', 0) for file_info in file_list)
            
            # Display statistics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    <div style="background-color:#000000; padding:20px; border-radius:10px; text-align:center;">
                        <div style="font-size:30px;">📁</div>
                        <div style="font-size:36px; font-weight:bold;">{}</div>
                        <div style="color:#666;">Total Files</div>
                    </div>
                """.format(total_files), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                    <div style="background-color:#000000; padding:20px; border-radius:10px; text-align:center;">
                        <div style="font-size:30px;">💾</div>
                        <div style="font-size:36px; font-weight:bold;">{}</div>
                        <div style="color:#666;">Storage Used</div>
                    </div>
                """.format(format_size(total_size)), unsafe_allow_html=True)
            
            with col3:
                # Sample file type distribution
                if total_files > 0:
                    file_types = {}
                    for file_info in file_list:
                        file_name = file_info['name']
                        ext = os.path.splitext(file_name)[1].lower()
                        file_types[ext] = file_types.get(ext, 0) + 1
                    
                    most_common_type = max(file_types.items(), key=lambda x: x[1])[0] if file_types else "None"
                    type_display = most_common_type if most_common_type else "None"
                else:
                    type_display = "None"
                
                st.markdown("""
                    <div style="background-color:#000000; padding:20px; border-radius:10px; text-align:center;">
                        <div style="font-size:30px;">📊</div>
                        <div style="font-size:36px; font-weight:bold;">{}</div>
                        <div style="color:#666;">Most Common Type</div>
                    </div>
                """.format(type_display), unsafe_allow_html=True)
            
            
        except Exception as e:
            st.error(f"Error generating statistics: {str(e)}")

else:
    # Welcome screen for non-logged in users
    st.markdown('<p class="main-header">Welcome to FileShare Hub</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; padding:30px; margin:20px 0;">
        <div style="font-size:80px;">📂</div>
        <div style="font-size:24px; margin:20px 0;">Your secure file storage solution</div>
        <div style="color:#666;">Please log in using the sidebar to access your files.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features display 
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color:#ffffff; padding:20px; border-radius:10px; text-align:center; color:#000000;">
            <div style="font-size:40px;">🔒</div>
            <div style="font-weight:bold; margin:10px 0;">Secure Storage</div>
            <div>Your files are encrypted and securely stored</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:#ffffff; padding:20px; border-radius:10px; text-align:center; color:#000000; ">
            <div style="font-size:40px;">👁️</div>
            <div style="font-weight:bold; margin:10px 0;">File Preview</div>
            <div>Preview images, audio, video, and more</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color:#ffffff; padding:20px; border-radius:10px; text-align:center; color:#000000;">
            <div style="font-size:40px;">📊</div>
            <div style="font-weight:bold; margin:10px 0;">Usage Analytics</div>
            <div>Track your storage usage and file metrics</div>
        </div>
        """, unsafe_allow_html=True)