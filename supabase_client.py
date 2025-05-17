import os
from supabase import create_client

def get_client(access_token=None, refresh_token=None):
    """Create and configure Supabase client
    
    Args:
        access_token: Optional access token for authenticated requests
        refresh_token: Optional refresh token for session renewal
    
    Returns:
        Configured Supabase client
    """
    # Get credentials from environment variables
    supabase_url = 
    supabase_key = 
    
    # Create the base client
    client = create_client(supabase_url, supabase_key)
    
    # If we have both tokens, set the session for authenticated requests
    if access_token and refresh_token:
        client.auth.set_session(access_token, refresh_token)
    
    return client
