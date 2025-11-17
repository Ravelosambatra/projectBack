import os
from supabase import create_client, Client
import uuid

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET: str = os.environ.get("SUPABASE_BUCKET_NAME", "media")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file):
    """
    Upload un fichier vers Supabase Storage et retourne son URL publique
    """
    file_ext = file.name.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"

    file_bytes = file.read()

    res = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=file_name,
        file=file_bytes,
        file_options={"content-type": file.content_type},
    )

    if "error" in res:
        raise Exception(res["error"])

    url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)
    return url
