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
    supabase_url = 'https://bmoicuppczldcjqotnuw.supabase.co'
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJtb2ljdXBwY3psZGNqcW90bnV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzNzI5ODcsImV4cCI6MjA1Nzk0ODk4N30.dqJsgStt0HeTE5mA6IJ__bTJbei9D2OnOo0B2rgE0T4"
    
    # Create the base client
    client = create_client(supabase_url, supabase_key)
    
    # If we have both tokens, set the session for authenticated requests
    if access_token and refresh_token:
        client.auth.set_session(access_token, refresh_token)
    
    return client