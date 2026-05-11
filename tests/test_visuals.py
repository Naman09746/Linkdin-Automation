import pytest
from src.core.visuals import VisualManager
from src.core.database import db_manager

def test_visual_pipeline():
    manager = VisualManager()
    sb = db_manager.get_supabase()
    
    # 1. Get a draft that needs a visual
    res = sb.table("drafts").select("*").limit(1).execute()
    if not res.data:
        print("No drafts found to test visuals.")
        return

    draft = res.data[0]
    print(f"Testing visual generation for draft: {draft['id']}")
    
    # 2. Generate prompt
    prompt = manager.generate_image_prompt(draft['content'])
    print(f"Generated Prompt: {prompt}")
    
    # 3. Generate image
    image_bytes = manager.generate_image(prompt)
    assert image_bytes is not None
    print("Successfully generated image bytes.")
    
    # 4. Upload
    url = manager.upload_asset(image_bytes, f"test_{draft['id']}.png")
    assert url is not None
    print(f"Success! Image available at: {url}")

if __name__ == "__main__":
    test_visual_pipeline()
